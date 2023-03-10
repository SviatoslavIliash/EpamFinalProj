"""Tests for database models"""
from bikerepair.models.models import User, Order, Service, OrderItem


def test_new_user():
    """Test for User model"""
    user = User(login="bob", password="1234", email="bob@bob.com")
    assert user.email == "bob@bob.com"
    assert user.password == "1234"
    assert user.__repr__() == "<User 'bob'>"
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous


def test_service_default_table(session, db):
    """Test for default service table in Service model"""
    service = Service(name="wax", price=100)
    session.commit()
    assert service.name == "wax"
    assert service.price == 100
    Service.default_table(current_db=db)
    default_service = session.query(Service)
    result_services = [service for service in default_service]
    assert len(result_services) == 4


def test_order(session, db):
    """Test for Order model"""
    order = Order(login="bob", date="2023-03-01 23:04:38", status="done")
    session.commit()
    assert order.login == "bob"
    assert order.date == "2023-03-01 23:04:38"
    assert order.status == "done"
    assert order.__repr__() == f'<Order id {order.id}|{order.login}|' \
                               f'{order.date}|{order.status}>'


def test_order_item(session, db):
    """Test for OrderItem model"""
    order = OrderItem(order_id=4, serv_name="wash", price=100)
    session.commit()
    assert order.order_id == 4
    assert order.serv_name == "wash"
    assert order.price == 100
