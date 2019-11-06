import tempfile

from joblib import dump, load
from sklearn.linear_model import LogisticRegression

from utils.aws import build_s3


class LogisticRegressionModel:
    def __init__(self, x_train, y_train):
        self.s3 = build_s3()
        self.model = LogisticRegression(solver='lbfgs')
        self.x_train = x_train
        self.y_train = y_train

    def fit(self, sample_weight=None):
        self.model.fit(self.x_train, self.y_train, sample_weight)

    def predict(self, test_x):
        return self.model.predict_proba(test_x)

    def score(self):
        return self.model.score(self.x_train, self.y_train)

    def save_to_s3(self, bucket_name, key):
        with tempfile.TemporaryFile() as fp:
            dump(self.model, fp)
            fp.seek(0)
            self.s3.Bucket(bucket_name).put_object(Body=fp.read(), Bucket=bucket_name, Key=key)
            fp.close()

    @staticmethod
    def load_from_s3(s3, bucket_name, key):
        with tempfile.TemporaryFile() as fp:
            s3.Bucket(bucket_name).download_fileobj(Fileobj=fp, Key=key)
            fp.seek(0)
            model = load(fp)
            fp.close()
        return model

    @staticmethod
    def save_predictions_to_s3(df, bucket_name, key):
        df.to_csv(f's3://{bucket_name}/{key}', index=False)
