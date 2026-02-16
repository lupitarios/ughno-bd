# python
from repository.db import db_configuration


def setup_module(module):
    # ensure singleton cleared before running tests in this module
    db_configuration.DBConfiguration.instance = None


def teardown_function(function):
    # reset singleton between tests
    db_configuration.DBConfiguration.instance = None


def test_get_url_connection_builds_expected_url(monkeypatch):
    # Arrange: set env vars and avoid loading any .env file
    monkeypatch.setenv("POSTGRES_HOST", "db-host")
    monkeypatch.setenv("POSTGRES_DB", "mydb")
    monkeypatch.setenv("POSTGRES_USER", "dbuser")
    monkeypatch.setenv("POSTGRES_PASSWORD", "s3cr3t")
    monkeypatch.setenv("POSTGRES_PORT", "5433")
    monkeypatch.setattr(db_configuration, "load_dotenv", lambda: None)

    db_configuration.DBConfiguration.instance = None
    cfg = db_configuration.DBConfiguration()

    # Act
    cfg.get_url_connection()

    # Assert
    expected = "postgresql://dbuser:s3cr3t@db-host:5433/mydb"
    assert cfg.postgres_url == expected


def test_db_connection_uses_create_engine(monkeypatch):
    # Arrange
    monkeypatch.setenv("POSTGRES_HOST", "h")
    monkeypatch.setenv("POSTGRES_DB", "d")
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setattr(db_configuration, "load_dotenv", lambda: None)

    created = {}

    def fake_create_engine(url):
        created["url"] = url
        return "FAKE_ENGINE"

    monkeypatch.setattr(db_configuration, "create_engine", fake_create_engine)

    db_configuration.DBConfiguration.instance = None
    cfg = db_configuration.DBConfiguration()

    # Act
    engine = cfg.db_connection()

    # Assert
    assert engine == "FAKE_ENGINE"
    assert created["url"] == "postgresql://u:p@h:5432/d"


def test_db_session_returns_session_from_sessionmaker(monkeypatch):
    # Arrange: patch load_dotenv and create_engine
    monkeypatch.setenv("POSTGRES_HOST", "h2")
    monkeypatch.setenv("POSTGRES_DB", "d2")
    monkeypatch.setenv("POSTGRES_USER", "u2")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p2")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setattr(db_configuration, "load_dotenv", lambda: None)

    fake_engine = object()
    monkeypatch.setattr(db_configuration, "create_engine", lambda url: fake_engine)

    fake_session_obj = object()
    captured = {}

    def fake_sessionmaker(bind=None):
        captured["bind"] = bind
        # return a callable that when called returns the session instance
        return lambda: fake_session_obj

    monkeypatch.setattr(db_configuration, "sessionmaker", fake_sessionmaker)

    db_configuration.DBConfiguration.instance = None
    cfg = db_configuration.DBConfiguration()

    # Act
    session = cfg.db_session()

    # Assert
    assert session is fake_session_obj
    assert captured["bind"] is fake_engine


def test_close_db_session_calls_close(monkeypatch):
    # Arrange: prepare a fake session with a close method that records invocation
    class FakeSession:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    s = FakeSession()

    # Act
    db_configuration.close_db_session(s)

    # Assert
    assert s.closed is True
