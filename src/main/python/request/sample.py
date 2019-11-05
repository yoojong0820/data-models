import numpy as np
import pandas as pd

from feature_extractor.feature_extractor import FeatureExtractor
from model.logistic_regression import LogisticRegressionModel
from utils.display import numpy_array_display_setting


def main():
    numpy_array_display_setting()

    # Single sample request coming from back-end
    sample_test_data = pd.DataFrame([
        [892, 3, 'Kelly, Mr.James', 'male', 34.5, 0, 0, 330911, 7.8292, np.NaN, 'Q']
    ], columns=[
        'PassengerId', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked'
    ])

    # Point to the correct bucket to load feature extractors and model
    bucket_name = 'team00-test-bucket'

    # Load feature extractors and model
    column_transformer = FeatureExtractor.load_from_s3(bucket_name, 'titanic/column_transformer.pkl')
    model = LogisticRegressionModel.load_from_s3(bucket_name, 'titanic/model.pkl')

    # Extract features
    transformed = column_transformer.transform(sample_test_data)

    # Get predictions
    estimate = model.predict_proba(transformed)
    print(estimate)


if __name__ == '__main__':
    main()
