import re
from werkzeug.security import check_password_hash, generate_password_hash
from bikerepair.models import User

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

def test_signup_exist_user(client, session):
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
