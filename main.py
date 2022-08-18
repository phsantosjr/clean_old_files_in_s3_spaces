import os
import boto3
from environs import Env
from datetime import datetime, date

from .exceptions import (
    PrefixNameFolderNotFoundException,
    MonthInformedIsNotIntException,
)

env = Env()
env.read_env()
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_ENDPOINT_URL = env("AWS_ENDPOINT_URL")
REGION_NAME = env("REGION_NAME")

s3_client = boto3.client(
    "s3",
    AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY,
)


def get_folders(path: str) -> list:
    """ Get a list of all folders in a bucket """
    result = s3_client.list_objects(
        Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=path, Delimiter="/"
    )
    return [o.get("Prefix") for o in result.get("CommonPrefixes")]


def get_items_in_folder(folder: str) -> list:
    """ Get all items in bucket using a folder as filter """
    return AWS_STORAGE_BUCKET_NAME.objects.filter(Prefix=folder)


def age_in_years(birthdate: datetime) -> int:
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    )


def age_in_months(birthdate: datetime) -> int:
    today = date.today()
    return (
        today.year
        - birthdate.year
        - ((today.month, today.day) < (birthdate.month, birthdate.day))
    ) * 12


def delete_object(key: str):
    """ Remove the object from bucket """
    s3_client.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=key)


def main():
    prefix = input("What's the prefix/folder you would like to search and delete ?")
    if not prefix:
        raise PrefixNameFolderNotFoundException

    month_to_cut = input("How many months you would like to consider to delete?")
    if isinstance(month_to_cut, int):
        raise MonthInformedIsNotIntException

    month_to_cut = int(month_to_cut)
    itens_deleted = 0

    folders = get_folders(f"{prefix}/")
    for folder in folders:
        items = get_items_in_folder(folder)

        for item in items:
            if folder != item.key:
                if age_in_months(item.last_modified) >= month_to_cut:
                    delete_object(item.key)
                    itens_deleted += 1

    print(f"We could deleted {itens_deleted} files in this process")


if __name__ == "__main__":
    main()
