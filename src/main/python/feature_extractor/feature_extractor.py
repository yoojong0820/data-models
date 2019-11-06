import tempfile

from joblib import dump, load
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from utils.aws import build_s3


class FeatureExtractor:
    def __init__(self, x_train, x_test):
        """
        This class will provide a vectorized form of training data
        :param x_train: raw training data frame
        :param x_test: raw test data frame
        """
        self.x_train = x_train
        self.x_test = x_test

        numeric_features = ['Age', 'Fare']
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])

        categorical_features = ['Embarked', 'Sex', 'Pclass']
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        self.column_transformer = ColumnTransformer(transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

        self.s3 = build_s3()

    def fit(self):
        return self.column_transformer.fit(self.x_train)

    def transform(self):
        self.fit()
        train = self.column_transformer.transform(self.x_train)
        test = self.column_transformer.transform(self.x_test)
        return train, test

    def save(self):
        dump(self.column_transformer, 'column_transformer.bin', compress=True)

    def save_to_s3(self, bucket_name, key):
        with tempfile.TemporaryFile() as fp:
            dump(self.column_transformer, fp)
            fp.seek(0)
            self.s3.Bucket(bucket_name).put_object(Body=fp.read(), Bucket=bucket_name, Key=key)
            fp.close()

    @staticmethod
    def load_from_s3(s3, bucket_name, key):
        with tempfile.TemporaryFile() as fp:
            s3.Bucket(bucket_name).download_fileobj(Fileobj=fp, Key=key)
            fp.seek(0)
            column_transformer = load(fp)
            fp.close()
        return column_transformer

