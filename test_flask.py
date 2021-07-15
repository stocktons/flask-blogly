from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test' #does this need to be blogly_test?
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self): # this runs before every test
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestUserFN", last_name="TestUserLN", image_url="")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id # I want to add a user id property to the UserViewsTestCase class. But maybe more useful to store the entire user instance object.

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_root_redirect(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_user_list(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User listing template.', html) # looks for something on the page that won't ever move (in theory, since we labeled it as testing.)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}") # self.user.id if use whole object
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUserFN TestUserLN</h1>', html) # self.user.first_name and don't specify h1 use an fstring to use self.user.fir...

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first-name": "TestFN2", "last-name": "TestLN2", "img-url" : ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestFN2 TestLN2</h1>", html) # fstring that looks for d[first-name]
