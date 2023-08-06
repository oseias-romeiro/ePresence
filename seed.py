import datetime
users = [
    {"register": 100000000, "name": "prof1", "password": "1234", "role": "PROFESSOR"},
    {"register": 200000000, "name": "prof2", "password": "1234", "role": "PROFESSOR"},
    {"register": 111111111, "name": "student1", "password": "1234", "role": "STUDENT"},
    {"register": 222222222, "name": "student2", "password": "1234", "role": "STUDENT"}
]

classes = [
    {"name": "Math", "slug": "class01"},
    {"name": "Science", "slug": "class02"},
]

userclass = [
    {"register": 100000000, "slug": "class01"},
    {"register": 111111111, "slug": "class01"},
    {"register": 222222222, "slug": "class01"},
    {"register": 200000000, "slug": "class02"},
    {"register": 111111111, "slug": "class02"},
]

rollscall = [
    {"date": datetime.datetime(2023, 1, 1), "slug": "class01", "coordinate": "-0.4312401,51.5281798"},
    {"date": datetime.datetime(2023, 1, 2), "slug": "class02", "coordinate": "-74.3093351,40.6970193"},
    {"date": datetime.datetime(2023, 1, 3), "slug": "class01", "coordinate": "-0.4312401,51.5281798"},
    {"date": datetime.datetime(2023, 1, 4), "slug": "class02", "coordinate": "-74.3093351,40.6970193"},
]

# TODO: call, frequency
