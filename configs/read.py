# read data from data source specified in config

# imports

import io
import os

import boto3
import pandas as pd


# functions

def csv(fp):
    '''read in csv to dataframe
    '''

    return pd.read_csv(fp)


def s3(bucket, key):
    '''read in csv from S3 url to dataframe
    '''

    # initialize S3 client
    client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
    obj = client.get_object(Bucket=bucket, Key=key)
    return pd.read_csv(io.BytesIO((obj['Body'].read())))


def query(sql, db):
    '''read in result of sql query ato dataframe
    '''

    return pd.read_sql(sql, db.connect())
