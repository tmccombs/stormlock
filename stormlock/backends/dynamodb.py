"Dynamodb backend"
import secrets
from datetime import datetime, timedelta
from time import time
from typing import Dict, Optional, Tuple

import boto3  # type: ignore
from boto3.dynamodb.conditions import Attr  # type: ignore

from stormlock.backend import Backend, Lease, LockExpiredException, LockHeldException


def _aws_session(config: dict) -> boto3.session.Session:
    return boto3.session.Session(
        region_name=config.get("region"),
        aws_access_key_id=config.get("aws_access_key_id"),
        aws_secret_access_key=config.get("aws_secret_access_key"),
        profile_name=config.get("profile_name"),
    )


def _parse_tags(tags: str) -> Dict[str, str]:
    taglist = tags.split(",")

    def tag_pair(tag: str) -> Tuple[str, str]:
        res = tag.split("=", 1)
        if len(res) == 1:
            return (tag, "")
        return (res[0], res[1])

    return dict(tag_pair(tag) for tag in taglist)


MAX_RETRIES = 3


class DynamoDB(Backend):
    "Stormlock backend that uses DynamoDB as a data store."

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
        super().__init__()
        session = boto3.session.Session(
            profile_name=profile,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        self._table = session.resource(
            "dynamodb", endpoint_url=endpoint, region_name=region
        ).Table(table)
        exceptions = self._table.meta.client.exceptions
        # pylint: disable=C0103
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

        condition = Attr("resource").not_exists() or Attr("expires").lte(
            item["created"]
        )
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
                ExpressionAttributeValues={":exp": int(expire.timestamp())},
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
        return None
