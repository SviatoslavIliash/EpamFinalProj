"""Main file for pytest tests"""
import pytest

from flask import template_rendered

from bikerepair import create_app, db as _db
from bikerepair.models.models import Service


@pytest.fixture(scope="session", autouse=True)
def app():
    """Fixture for app"""
    test_app = create_app('TEST')
    test_app.config.update({
        "TESTING": True,
        "LOGIN_DISABLED": True,
    })

    # other setup can go here
    with test_app.app_context():
        yield test_app


@pytest.fixture(scope="session")
def client(app):
    """Fixture for app client"""
    client = app.test_client()

    yield client


@pytest.fixture(scope="function")
def session(db, request):
    """Fixture for db session"""
    db.session.begin_nested()

    def commit():
        db.session.flush()
    # patch commit method
    old_commit = db.session.commit
    db.session.commit = commit

    def teardown():
        db.session.rollback()
        db.session.close()
        db.session.commit = old_commit
    request.addfinalizer(teardown)
    return db.session


@pytest.fixture()
def runner(app):
    """Fixture for cli runner"""
    return app.test_cli_runner()


@pytest.fixture
def captured_templates(app):
    """Fixture for templates"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(scope="module")
def new_service():
    """Fixture for new service"""
    service = Service(name='default', price='400')
    return service


@pytest.fixture(scope='session')
def db(app, request):
    """Fixture for db"""
    def teardown():
        _db.drop_all()

    _db.create_all()
    request.addfinalizer(teardown)
    return _db
