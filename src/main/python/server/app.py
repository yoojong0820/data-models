import pandas as pd
from flask import Flask, request, jsonify

from feature_extractor.feature_extractor import FeatureExtractor
from model.logistic_regression import LogisticRegressionModel


def main():
    app = Flask(__name__)

    bucket_name = 'team00-test-bucket'
    column_transformer = FeatureExtractor.load_from_s3(bucket_name, 'titanic/column_transformer.pkl')
    model = LogisticRegressionModel.load_from_s3(bucket_name, 'titanic/model.pkl')

    @app.route('/predict', methods=['POST'])
    def predict():
        data = request.get_json(force=True)
        mapped = {k: [v] for k, v in data.items()}
        df = pd.DataFrame.from_dict(mapped, orient="columns")
        transformed = column_transformer.transform(df)
        prediction = model.predict_proba(transformed)
        return jsonify(
            label_zero_estimate=prediction[0][0],
            label_one_estimate=prediction[0][1]
        )

    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
