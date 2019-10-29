from s3.reader import S3Reader


def main():
    r = S3Reader()
    training, test = r.execute()
    print(training)
    print(test)


if __name__ == '__main__':
    main()
