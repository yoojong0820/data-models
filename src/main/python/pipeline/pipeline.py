from pipeline.sample import SampleTitanicModel
from utils.display import numpy_array_display_setting


def main():
    numpy_array_display_setting()
    pipeline = SampleTitanicModel(
        bucket_name='team00-test-bucket',
        training_data_key='titanic/train.csv',
        test_data_key='titanic/test.csv'
    )
    pipeline.process()


if __name__ == '__main__':
    main()
