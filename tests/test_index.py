import pytest
from bikerepair.models import User

@pytest.fixture()
def new_user(app, session):
    #with app.app_context():
    user = User(login='mat1', password='1234', email='bla@bla.com')
    session.add(user)
    session.flush()

    return user

def test_1(session):
    user = User(login='mat1', password='1234', email='bla@bla.com')
    session.add(user)
    session.flush()

    assert User.query.filter_by(login="mat1").first() == user




