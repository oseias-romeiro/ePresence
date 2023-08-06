import datetime
users = [
    {"register": 100000000, "name": "John Smith", "password": "1234", "role": "PROFESSOR"},
    {"register": 200000000, "name": "Emily Johnson", "password": "1234", "role": "PROFESSOR"},
    {"register": 111111111, "name": "John Doe", "password": "1234", "role": "STUDENT"},
    {"register": 222222222, "name": "Emma Williams", "password": "1234", "role": "STUDENT"}
]

classes = [
    {"name": "Mathematics", "slug": "mathematics"},
    {"name": "History", "slug": "history"},
]

userclass = [
    {"register": 100000000, "slug": "mathematics"},
    {"register": 111111111, "slug": "mathematics"},
    {"register": 222222222, "slug": "mathematics"},
    {"register": 200000000, "slug": "history"},
    {"register": 111111111, "slug": "history"},
]

rollscall = [
    {"date": datetime.datetime(2023, 1, 1), "slug": "mathematics", "coordinate": "-0.4312401,51.5281798"},
    {"date": datetime.datetime(2023, 1, 2), "slug": "history", "coordinate": "-74.3093351,40.6970193"},
]

frequencies = [
    {"register": 111111111, "id_call": 1, "coordinate": "-0.4312401,51.5281798"},
    {"register": 111111111, "id_call": 2, "coordinate": "-0.4312401,51.5281798"},
]
