import boto3

from feature_extractor.sample import SampleTitanicFeatureExtractor
from model.logistic_regression import LogisticRegressionModel
from utils.aws import get_session


class SampleTitanicModel:
    def __init__(self, bucket_name, training_data_key, test_data_key):
        self.bucket_name = bucket_name
        self.feature_extractor = SampleTitanicFeatureExtractor(bucket_name, training_data_key, test_data_key)

        session = get_session()
        self.s3 = session.resource('s3')

    def process(self):
        train_x, train_y = self.feature_extractor.process()
        model = LogisticRegressionModel(train_x, train_y)
        model.fit()
        model.save_to_s3(self.bucket_name, 'titanic/model.pkl')
