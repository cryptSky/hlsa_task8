import requests
from faker import Faker
from faker.providers import date_time
import json

fake = Faker()
fake.add_provider(date_time)

for i in range(40000000):
    user = {
        'name': fake.name(),
        'email': fake.email(),
        'birthdate': fake.date()
    }

    response = requests.post('http://localhost:8000/users', json=json.dumps(user))

    if response.ok:
        if i % 100000 == 0:
            user_id = response.json()['id']
            print("User {0} added".format(user_id))
    else:
        print("Error")