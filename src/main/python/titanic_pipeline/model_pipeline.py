from feature_extractor.pipeline import FeatureExtractionPipeline
from model.logistic_regression import LogisticRegressionModel
from utils.aws import build_s3

import pandas as pd


class TitanicModelPipeline:
    def __init__(self, bucket_name, training_data_key, test_data_key):
        self.s3 = build_s3()
        self.bucket_name = bucket_name
        self.training_data_key = training_data_key
        self.test_data_key = test_data_key

    def process(self):
        # extract features
        feature_extractor = FeatureExtractionPipeline(self.bucket_name, self.training_data_key, self.test_data_key)
        train_x, train_y, test_x = feature_extractor.process(self.bucket_name)

        # fit model
        model = LogisticRegressionModel(train_x, train_y)
        model.fit()

        # make batch predictions
        predictions = model.predict(test_x)
        test_y = pd.DataFrame({'label_zero_estimate': predictions[:, 0], 'label_one_estimate': predictions[:, 1]})
        LogisticRegressionModel.save_predictions_to_s3(test_y, self.bucket_name, 'titanic/predictions.csv')

        # save model
        model.save_to_s3(self.bucket_name, 'titanic/model.pkl')
