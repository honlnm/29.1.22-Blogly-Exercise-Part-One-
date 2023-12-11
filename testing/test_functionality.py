from app import app
from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLACHEMY_ECHO'] = True
app.config['TESTING'] = True

class UserTestCase(TestCase):
    """test for model for Users"""

    def setUp(self):
        """clear the table contents and add user"""
        with app.app_context():
            User.query.delete()
            db.session.commit()
            user = User(first_name="John", last_name="Doe")
            db.session.add(user)
            db.session.commit()
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """clear up all transactions"""
        with app.app_context():
            db.session.rollback()

    def test_showUsers(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)

    def test_addUser(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)

    def test_editUser(self):
        with app.test_client() as client:
            res = client.get('/users/1/edit')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 200)

    def test_deleteUser(self):
        with app.test_client() as client:
            res = client.get('/users/1/delete')
            html = res.get_data(as_text=True)

        self.assertEqual(res.status_code, 302)
    
