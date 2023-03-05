import re

import pytest
from werkzeug.security import check_password_hash
from bikerepair.models import User, Order, Service, OrderItem


def test_main_route(client, captured_templates) -> None:
    route = "/home"
    rv = client.get(route)

    # Sanity checks - it would be a total surprise if this would not hold true
    assert rv.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "index.html"


def test_signup(client, session):
    response = client.post("/signup", data={
        "login": "admin",
        "password": "1234",
        "password2": "1234",
        "email": "admin@gmail.com",
    })
    assert response.status_code == 302

    expected_user = User(login="admin", password="1234", email="admin@gmail.com")
    actual_user = session.query(User).filter_by(login="admin").first()
    assert actual_user.login == expected_user.login and actual_user.email == expected_user.email
    assert check_password_hash(actual_user.password, expected_user.password)


def test_duplicate_signup(client, session):
    response = client.post("/signup", data={
        "login": "admin",
        "password": "1234",
        "password2": "1234",
        "email": "admin@gmail.com",
    })
    response1 = client.post("/signup", data={
        "login": "admin",
        "password": "1234",
        "password2": "1234",
        "email": "admin@gmail.com",
    })
    assert response1.status_code == 200
    assert re.search('Such login exists. Choose another name!',
                              response1.get_data(as_text=True))


def test_signup_pass_not_equal(client, session):
    response = client.post("/signup", data={
        "login": "bob",
        "password": "1234",
        "password2": "12345",   # Does NOT match!
        "email": "bob@gmail.com",
    })

    assert response.status_code == 200
    assert re.search('Passwords are not equal!',
                     response.get_data(as_text=True))


def test_signup_not_fill(client, session):
    response = client.post("/signup", data={
        "login": "bob",
        "password": "1234",
        "password2": "1234",
        "email": "",  # blank!
    })

    assert response.status_code == 200
    assert re.search('Please, fill all fields!',
                     response.get_data(as_text=True))


def test_signup_not_allowed_login(client, session):
    response = client.post("/signup", data={
        "login": "bob@",  # NOT allowed character
        "password": "1234",
        "password2": "1234",
        "email": "",
    })

    assert response.status_code == 200
    assert re.search('Login must be 3-40 length and contents only letters, numbers, underscore!',
                     response.get_data(as_text=True))


def test_invalid_login(client, session, captured_templates):
    name = 'bob'
    response = client.post("/signup", data={
        "login": name,
        "password": "1234",
        "password2": "1234",
        "email": "bob@gmail.com",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "login.html"
    response1 = client.post("/login", data={
        "login": name,
        "password": "123",  # password NOT match
    }, follow_redirects=True)

    assert response1.status_code == 200
    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert template.name == "login.html"
    assert re.search('Login or password is not correct',
                     response1.get_data(as_text=True))


def test_login(client, session, captured_templates):
    name = 'bob'
    response = client.post("/signup", data={
        "login": name,
        "password": "1234",
        "password2": "1234",
        "email": "bob@gmail.com",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "login.html"
    response1 = client.post("/login", data={
        "login": name,
        "password": "1234",
    }, follow_redirects=True)

    assert response1.status_code == 200
    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert template.name == "user_account.html"
    assert re.search(f'Welcome, {name}',
                     response1.get_data(as_text=True))


def test_invalid_login_empty_field(client, session, captured_templates):

    response = client.post("/login", data={
        "login": "",  # EMPTY field
        "password": "1234",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert len(captured_templates) == 1
    template, context = captured_templates[0]
    assert template.name == "login.html"
    assert re.search('Please fill login and password fields',
                     response.get_data(as_text=True))


def test_logout( client, session, captured_templates):

    response = client.post("/login", data={
        "login": "bob",
        "password": "1234",
    }, follow_redirects=True)
    assert response.status_code == 200

    response1 = client.get("/logout", follow_redirects=True)

    assert response1.status_code == 200
    assert len(captured_templates) == 2
    template, context = captured_templates[1]
    assert template.name == "login.html"
    assert re.search('You have been logged out, my friend!',
                     response1.get_data(as_text=True))


def test_new_user():
    user = User(login="bob", password="1234", email="bob@bob.com")
    assert user.email == "bob@bob.com"
    assert user.password == "1234"
    assert user.__repr__() == "<User 'bob'>"
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_service_default_table(session, db):
    service = Service(name="wax", price=100)
    session.commit()
    assert service.name == "wax"
    assert service.price == 100
    Service.default_table(current_db=db)
    default_service = session.query(Service)
    result_services = [service for service in default_service]
    assert len(result_services) == 4


def test_order(session, db):
    order = Order(login="bob", date="2023-03-01 23:04:38", status="done")
    session.commit()
    assert order.login == "bob"
    assert order.date == "2023-03-01 23:04:38"
    assert order.status == "done"
    assert order.__repr__() == f"<Order {order.id}>"


def test_order_item(session, db):
    order = OrderItem(order_id=4, serv_name="wash", price=100)
    session.commit()
    assert order.order_id == 4
    assert order.serv_name == "wash"
    assert order.price == 100


