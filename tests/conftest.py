import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.settings import TEST_DB_URL
from models import *
from services.services import get_from_file

test_engine = create_engine(TEST_DB_URL)
# test_engine = create_engine(TEST_DB_URL, echo=True)
test_session = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="class", autouse=True)
# @pytest.fixture(scope="session", autouse=True)
# @pytest.fixture(scope="module", autouse=True)
def db_session():
    """Fixture to connect with DB for tests.
    Deletes all tables left and creates new for every TestClass in test_db.py"""
    conn = test_engine.connect()
    session = test_session(bind=conn)
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    try:
        yield session
    finally:
        session.close()


# @pytest.fixture
# def json_problems():
#     json_data = get_from_file('test_problems.json')
#     return json_data


@pytest.fixture
def json_problems():
    json_data = {
        "status": "OK",
        "result": {
            "problems": [
                {
                    "contestId": 11111111111,
                    "index": "A",
                    "name": "TEST1",
                    "type": "PROGRAMMING",
                    "tags": [
                        "tag1"
                    ]
                },
                {
                    "contestId": 222222222222,
                    "index": "B",
                    "name": "TEST2",
                    "type": "PROGRAMMING",
                    "tags": [
                        "tag1"
                    ]
                },
                {
                    "contestId": 33333333333,
                    "index": "C",
                    "name": "TEST3",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag1", "tag2", "tag3"
                    ]
                }
            ],
            "problemStatistics": [
                {
                    "contestId": 11111111111,
                    "index": "A",
                    "solvedCount": 11
                },
                {
                    "contestId": 222222222222,
                    "index": "B",
                    "solvedCount": 22
                },
                {
                    "contestId": 33333333333,
                    "index": "C",
                    "solvedCount": 33
                }
            ]
        }
    }
    return json_data


# @pytest.fixture
# def json_problems_updated():
#     json_data = get_from_file('test_problems_updated.json')
#     return json_data


@pytest.fixture
def json_problems_updated():
    json_data = {
        "status": "OK",
        "result": {
            "problems": [
                {
                    "contestId": 11111111111,
                    "index": "A",
                    "name": "TEST1_upd",
                    "type": "PROGRAMMING",
                    "tags": [
                        "tag1"
                    ]
                },
                {
                    "contestId": 222222222222,
                    "index": "B",
                    "name": "TEST2",
                    "type": "PROGRAMMING",
                    "tags": [
                        "tag1"
                    ]
                },
                {
                    "contestId": 33333333333,
                    "index": "C",
                    "name": "TEST3",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag1", "tag2", "tag3"
                    ]
                }
            ],
            "problemStatistics": [
                {
                    "contestId": 11111111111,
                    "index": "A",
                    "solvedCount": 11
                },
                {
                    "contestId": 222222222222,
                    "index": "B",
                    "solvedCount": 2222
                },
                {
                    "contestId": 33333333333,
                    "index": "C",
                    "solvedCount": 33
                }
            ]
        }
    }
    return json_data


# @pytest.fixture
# def json_problems_11_items():
#     json_data = get_from_file('test_problems_11.json')
#     return json_data


@pytest.fixture
def json_problems_11_items():
    json_data = {
        "status": "OK",
        "result": {
            "problems": [
                {
                    "contestId": 1,
                    "index": "A",
                    "name": "TEST1",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 2,
                    "index": "B",
                    "name": "TEST2",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 3,
                    "index": "C",
                    "name": "TEST3",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 4,
                    "index": "A",
                    "name": "TEST4",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 5,
                    "index": "B",
                    "name": "TEST5",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 6,
                    "index": "C",
                    "name": "TEST6",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 7,
                    "index": "A",
                    "name": "TEST7",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 8,
                    "index": "B",
                    "name": "TEST8",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 9,
                    "index": "C",
                    "name": "TEST9",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 10,
                    "index": "C",
                    "name": "TEST9",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                },
                {
                    "contestId": 11,
                    "index": "C",
                    "name": "TEST9",
                    "type": "PROGRAMMING",
                    "rating": 800,
                    "tags": [
                        "tag11"
                    ]
                }
            ],
            "problemStatistics": [
                {
                    "contestId": 1,
                    "index": "A",
                    "solvedCount": 11
                },
                {
                    "contestId": 2,
                    "index": "B",
                    "solvedCount": 2222
                },
                {
                    "contestId": 3,
                    "index": "C",
                    "solvedCount": 33
                },
                {
                    "contestId": 4,
                    "index": "A",
                    "solvedCount": 11
                },
                {
                    "contestId": 5,
                    "index": "B",
                    "solvedCount": 2222
                },
                {
                    "contestId": 6,
                    "index": "C",
                    "solvedCount": 33
                },
                {
                    "contestId": 7,
                    "index": "A",
                    "solvedCount": 11
                },
                {
                    "contestId": 8,
                    "index": "B",
                    "solvedCount": 2222
                },
                {
                    "contestId": 9,
                    "index": "C",
                    "solvedCount": 33
                },
                {
                    "contestId": 10,
                    "index": "C",
                    "solvedCount": 33
                },
                {
                    "contestId": 11,
                    "index": "C",
                    "solvedCount": 33
                }
            ]
        }
    }
    return json_data


# @pytest.fixture
# def json_problems_another_rating():
#     json_data = get_from_file('test_problems_rating.json')
#     return json_data

@pytest.fixture
def json_problems_another_rating():
    json_data = {
        "status": "OK",
        "result": {
            "problems": [
                {
                    "contestId": 12,
                    "index": "A",
                    "name": "TEST12",
                    "type": "PROGRAMMING",
                    "rating": 1100,
                    "tags": [
                        "tag11"
                    ]
                }
            ],
            "problemStatistics": [
                {
                    "contestId": 12,
                    "index": "A",
                    "solvedCount": 11
                }
            ]
        }
    }
    return json_data
