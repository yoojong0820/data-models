from feature_extractor.feature_extractor import FeatureExtractor
from s3.reader import S3Reader


class SampleTitanicFeatureExtractor:
    def __init__(self, bucket_name, training_data_key, test_data_key):
        self.bucket_name = bucket_name

        # Load data from S3
        r = S3Reader(bucket_name, training_data_key, test_data_key)
        self.training, self.test = r.execute()

        # Subset to only contain X data
        self.x_training = self.training.drop('Survived', axis=1)
        self.x_test = self.test

    def process(self):
        feature_extractor = FeatureExtractor(self.x_training, self.x_test)
        train, test = feature_extractor.transform()
        feature_extractor.save_to_s3(self.bucket_name, 'titanic/column_transformer.pkl')
        return train, self.training['Survived']
