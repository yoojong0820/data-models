import json

import requests


def main():
    # Single sample request coming from back-end
    sample_test_data = {
        'PassengerId': 892,
        'Pclass': 3,
        'Name': 'Kelly, Mr.James',
        'Sex': 'male',
        'Age': 34.5,
        'SibSp': 0,
        'Parch': 0,
        'Ticket': 330911,
        'Fare': 7.8292,
        'Cabin': 'NULL',
        'Embarked': 'Q'
    }
    json_test_data = json.dumps(sample_test_data)

    url = 'http://localhost:5000/api'
    r = requests.post(url, json=json_test_data)
    print(r.json())


if __name__ == '__main__':
    main()
