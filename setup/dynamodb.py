#!/usr/bin/env python3

import sys
from typing import Optional, Any

import boto3  # type: ignore


def create_lock_table(
    table_name: str = "stormlock",
    endpoint: Optional[str] = None,
    billing_mode: str = "PAY_PER_REQUEST",
    read_capacity: Optional[int] = None,
    write_capacity: Optional[int] = None,
    sse: Optional[str] = None,
    sse_key_id: Optional[str] = None,
    tags: dict = {},
    region: Optional[str] = None,
    profile: Optional[str] = None,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
):
    session = boto3.session.Session(
        region_name=region,
        profile_name=profile,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
    client = session.client("dynamodb", endpoint_url=endpoint)

    config_args: dict[str, Any] = {}
    if billing_mode != "PAY_PER_REQUEST":
        config_args["ProvisionedThroughput"] = {
            "ReadCapacityUnits": read_capacity,
            "WriteCapacityUnits": write_capacity,
        }
    if sse:
        config_args["SSESpecification"] = {
            "Enabled": True,
            "SSEType": sse,
            "KMSMasterKeyId": sse_key_id,
        }

    client.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "resource", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "resource", "AttributeType": "S"}],
        BillingMode=billing_mode,
        Tags=[{"Key": k, "Value": v} for (k, v) in tags.items()],
        **config_args
    )
    # client.get_waiter('table_exists').wait(TableName=table_name)
    client.update_time_to_live(
        TableName=table_name,
        TimeToLiveSpecification={"Enabled": True, "AttributeName": "expires"},
    )


def test_setup(endpoint="http://localhost:8000"):
    create_lock_table(
        aws_access_key_id="test",
        aws_secret_access_key="test",
        endpoint=endpoint,
        region="us-east-1",
    )


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            test_setup()
        elif sys.argv[1] == "ci":
            test_setup("http://dynamodb:8000")
    else:
        # TODO: parse CLI flags
        create_lock_table()
