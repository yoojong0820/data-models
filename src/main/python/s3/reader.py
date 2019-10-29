import boto3
import pandas as pd

from io import StringIO
from utils.display import pandas_df_display_setting


class S3Reader:
    def __init__(self):
        session = boto3.Session(profile_name='default')
        self.s3 = session.resource('s3')
        self.bucket_name = 'team00-test-bucket'
        self.training_data_key = 'titanic/train.csv'
        self.test_data_key = 'titanic/test.csv'

    def fetch_objects(self):
        training = pd.DataFrame()
        test = pd.DataFrame()

        filtered_training = list(self.s3.Bucket(self.bucket_name).objects.filter(Prefix=self.training_data_key))
        filtered_test = list(self.s3.Bucket(self.bucket_name).objects.filter(Prefix=self.test_data_key))

        if len(filtered_training) > 0:
            ls = StringIO(filtered_training[0].get()['Body'].read().decode('utf-8'))
            training = pd.read_csv(ls, header=0)

        if len(filtered_test) > 0:
            ls = StringIO(filtered_test[0].get()['Body'].read().decode('utf-8'))
            test = pd.read_csv(ls, header=0)

        return training, test

    def execute(self):
        pandas_df_display_setting()
        return self.fetch_objects()
