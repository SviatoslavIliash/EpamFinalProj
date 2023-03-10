"""Tests for database CRUD function"""
import datetime

from bikerepair.models.models import Service, Order
from bikerepair.service.db_crud import check_login_user, create_user, validate_login, \
    create_user_order, total_user_orders, date_filter_orders, crud_status


class TestDbCrud:
    """Test class for testing database CRUD"""
    # create data for testing
    login = 'ben'
    login_invalid = '@ben#'
    password = '1234'
    password2 = '1235'  # NOT correct password2
    email = 'ben@ben.com'
    services = ['lube_chain', 'repair', 'upgrade', 'wash']  # alphabetically sorted
    first_date = '2023-02-10'
    second_date = '2023-03-10 23:59:59'

    def test_check_login_user(self, session):
        """Test for login user"""
        response = check_login_user(self.login, self.password)
        assert response is not None
        assert response == 'Login or password is not correct'

    def test_create_user(self, session):
        """Test for create new user"""
        response = create_user(self.login, self.password, self.password, self.email)
        assert response is None

        response_not_equal_pass = create_user(self.login, self.password, self.password2, self.email)
        assert response_not_equal_pass == 'Passwords are not equal!'

        response_blanc_field = create_user('', self.password, self.password2, self.email)
        assert response_blanc_field == 'Please, fill all fields!'

        response_blanc_field_all = create_user('', '', '', '')
        assert response_blanc_field_all == 'Please, fill all fields!'

        response_double_login = create_user(self.login, self.password, self.password, self.email)
        assert response_double_login == 'Such login exists. Choose another name!'

    def test_validate_login(self):
        """Test for valid user login function"""
        response = validate_login(self.login)
        assert response is True

        response_invalid = validate_login(self.login_invalid)
        assert response_invalid is False

    def test_create_user_order(self, session, db):
        """Test for create new user order"""
        Service.default_table(db)
        response = create_user_order(self.login, self.services)
        assert response is None
        order = session.query(Order).one()
        assert order.date.date() == datetime.date.today()
        assert order.login == self.login
        assert order.status == 'pending'
        assert order.id == 1
        response_no_services = create_user_order(self.login, [])
        assert response_no_services == 'Choose service!'

    def test_total_user_orders(self, session, db):
        """Test for all user orders function"""
        response = total_user_orders(self.login)
        assert not response

        Service.default_table(db)
        create_user_order(self.login, self.services)
        response_order = total_user_orders(self.login)
        assert len(response_order) == 1
        sorted_services = response_order[0].services.split(", ")
        sorted_services.sort()
        assert self.services == sorted_services

    def test_date_filter_orders(self, session, db):
        """Test for filter user orders"""
        Service.default_table(db)
        session.add_all([
            Order(login=self.login, date=datetime.date(2023, 1, 22)),  # id == 1
            Order(login=self.login, date=datetime.date(2023, 2, 14)),  # id == 2
            Order(login=self.login, date=datetime.date(2023, 3, 9)),  # id == 3
            Order(login=self.login, date=datetime.date(2022, 12, 5)),  # id == 4
            Order(login=self.login, date=datetime.date(2023, 3, 10))  # id == 5
        ])
        session.flush()
        response = date_filter_orders(self.first_date, self.second_date)
        valid_response = [order.id for order in response]
        assert valid_response == [2, 3, 5]

        response_blanc = date_filter_orders('', '')
        blanc_response = [order.id for order in response_blanc]
        assert not blanc_response

        no_order_response = date_filter_orders('2022-02-10', '2022-1-10')
        no_order_between = [order.id for order in no_order_response]
        assert not no_order_between

        high_edge_response = date_filter_orders('', '2023-02-10')
        edge_orders = [order.id for order in high_edge_response]
        assert edge_orders == [1, 4]

    def test_crud_status(self, session, db):
        """Test for change status or delete order"""
        Service.default_table(db)
        create_user_order(self.login, self.services)
        order = session.query(Order).one()
        current_status = order.status
        current_id = order.id
        assert current_status == 'pending'
        assert current_id == 1

        crud_status(current_status, 'in process', '', current_id)  # change order status to 'in process'
        assert session.query(Order.status).one().status == 'in process'

        crud_status(current_status, 'in process', 'delete', current_id)  # delete order!
        response_delete = total_user_orders(self.login)
        assert not response_delete
        assert session.query(Order).first() is None
