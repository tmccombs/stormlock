from datetime import datetime, timedelta
import secrets
from time import time
from typing import Optional

import boto3
from boto3.dynamodb.conditions import Attr

from stormlock.backend import Backend, Lease, LockHeldException, LockExpiredException


def _aws_session(config: dict) -> boto3.session.Session:
    return boto3.session.Session(
        region_name=config.get("region"),
        aws_access_key_id=config.get("aws_access_key_id"),
        aws_secret_access_key=config.get("aws_secret_access_key"),
        profile_name=config.get("profile_name"),
    )


def _parse_tags(tags: str) -> list:
    taglist = tags.split(",")
    return {k: v for (k, v) in (tag.split("=", 1) for tag in taglist)}


class DynamoDB(Backend):
    def __init__(
        self,
        *,
        table: str = "stormlock",
        endpoint: Optional[str] = None,
        region: Optional[str] = None,
        profile: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None,
    ):
        session = boto3.session.Session(
            profile_name=profile,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self._table = session.resource(
            "dynamodb", endpoint_url=endpoint, region_name=region
        ).Table(table)
        exceptions = self._table.meta.client.exceptions
        self._ConditionFailedException = exceptions.ConditionalCheckFailedException

    def lock(self, resource: str, principal: str, ttl: timedelta):
        # FIXME: use uuid?
        lease_id = secrets.token_bytes(16).hex()
        created = datetime.now()
        expires = created + ttl
        item = {
            "resource": resource,
            "principal": principal,
            "created": int(created.timestamp()),
            "lease": lease_id,
            "expires": int(expires.timestamp()),
        }

        condition = Attr("resource").not_exists() or Attr("expires").le(item["created"])
        try:
            self._table.put_item(Item=item, ConditionExpression=condition)
            return lease_id
        except self._ConditionFailedException:
            raise LockHeldException(resource, self.current(resource))

    def unlock(self, resource: str, lease_id: str):
        try:
            self._table.delete_item(
                Key={"resource": resource},
                ConditionExpression=Attr("lease").eq(lease_id),
            )
        except self._ConditionFailedException:
            pass

    def renew(self, resource: str, lease_id: str, ttl: timedelta):
        now = datetime.now()

        condition = Attr("lease").eq(lease_id) and Attr("expires").gt(
            int(now.timestamp())
        )
        expire = now + ttl

        try:
            self._table.update_item(
                Key={"resource": resource},
                UpdateExpression="SET expires = :exp",
                ConditionExpression=condition,
                ExpressionAttributeValues={":exp": int(expire.timestamp()),},
            )
        except self._ConditionFailedException:
            raise LockExpiredException(resource)

    def current(self, resource: str) -> Optional[Lease]:
        item = self._table.get_item(
            Key={"resource": resource},
            ConsistentRead=True,
            ProjectionExpression="principal,created,lease,expires",
        ).get("Item")
        if item:
            if item["expires"] <= time():
                return None
            created = datetime.fromtimestamp(item["created"])
            return Lease(item["principal"], created, item["lease"])
