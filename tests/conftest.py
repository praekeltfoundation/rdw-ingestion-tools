import os


def pytest_sessionstart(session):
    os.environ["AAQV2_API_KEY"] = "key"
    os.environ["AAQV2_API_BASE_URL"] = "http://fake_aaqv2/"
    os.environ["RAPIDPRO_API_KEY"] = "RAPIDPRO_API_KEY"
    os.environ["RAPIDPRO_API_BASE_URL"] = "http://RAPIDPRO_API_BASE_URL/"
