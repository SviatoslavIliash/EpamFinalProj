import pytest
from bikerepair import create_app, db as _db
from flask import template_rendered
from bikerepair.models import User, Service, Order, OrderItem


@pytest.fixture(scope="session", autouse=True)
def app():
    test_app = create_app('TEST')
    test_app.config.update({
        "TESTING": True,

    })


    # other setup can go here
    with test_app.app_context():
        yield test_app


@pytest.fixture(scope="session")
def client(app):
    client = app.test_client()
    #with app.app_context():
    #_db.create_all()
    yield client


@pytest.fixture(scope="function")
def session(db, request):
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
    return app.test_cli_runner()

def test_index(client):
    response = client.get("/home")
    assert "index.html" in response.data

def test_main_route_status_code(client) -> None:
    route = "/login"
    rv = client.get(route)
    assert rv.status_code == 200

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


def test_main_route(client, captured_templates) -> None:
    route = "/home"
    rv = client.get(route)

    # Sanity checks - it would be a total surprise if this would not hold true
    assert rv.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"




@pytest.fixture(scope="module")
def new_service():
    service = Service(name='default', price='400')
    return service

@pytest.fixture(scope='session')
def db(app, request):
    def teardown():
        _db.drop_all()

    _db.create_all()
    request.addfinalizer(teardown)
    return _db


