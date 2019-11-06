from io import StringIO

import pandas as pd

from utils.aws import build_s3
from utils.display import pandas_df_display_setting


class S3Reader:
    def __init__(self, bucket_name, key):
        """
        This reader can only read CSV file from AWS S3 - read & turn it into pandas data frame
        TODO: Add capability to process other formats (i.e. json, text, avro, parquet, etc.)
        :param bucket_name: AWS S3 bucket name
        :param key: AWS S3 key to locate the CSV file
        """
        self.s3 = build_s3()
        self.bucket_name = bucket_name
        self.key = key

    def fetch_objects(self):
        df = pd.DataFrame()
        filtered = list(self.s3.Bucket(self.bucket_name).objects.filter(Prefix=self.key))

        if len(filtered) > 0:
            ls = StringIO(filtered[0].get()['Body'].read().decode('utf-8'))
            df = pd.read_csv(ls, header=0)

        return df

    def execute(self):
        pandas_df_display_setting()
        return self.fetch_objects()
