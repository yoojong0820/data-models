from titanic_pipeline.model_pipeline import TitanicModelPipeline


# Execute this pipeline offline to update feature extractors & model in AWS S3
def main():
    pipeline = TitanicModelPipeline(
        bucket_name='team00-test-bucket',
        training_data_key='titanic/train.csv',
        test_data_key='titanic/test.csv'
    )
    pipeline.process()


if __name__ == '__main__':
    main()
