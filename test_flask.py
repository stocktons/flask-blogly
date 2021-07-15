from unittest import TestCase

from app import app
from models import db, User, Post

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

        self.user = user # I want to add a user id property to the UserViewsTestCase class. But maybe more useful to store the entire user instance object.

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()



    def test_root_redirect(self):
        """Checks to see that root redirects correctly."""

        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")

    def test_user_list(self):
        """Checks to see that the current user list displays."""

        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User listing template.', html) # looks for something on the page that won't ever move (in theory, since we labeled it as testing.)



    def test_show_user(self):
        """Checks to see that the user profile is displayed."""

        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.user.first_name} {self.user.last_name}', html) # self.user.first_name and don't specify h1 use an fstring to use self.user.fir...



    def test_add_user(self):
        """Checks to see if a user can be added and displayed on user list successfully."""
        
        with app.test_client() as client:
            d = {"first-name": "TestFN2", "last-name": "TestLN2", "img-url" : ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{d["first-name"]} {d["last-name"]}', html)


class PostViewsTestCase(TestCase):
    """Tests view functions for Posts."""

    def setUp(self): # this runs before every test
        """Add sample user & sample post."""

        Post.query.delete()
        User.query.delete()
        
        user = User(first_name="TestUserFN", last_name="TestUserLN", image_url="")
        post = Post(title="TestPostTitle", content="TestPostContent", user_id=user.id) 

        db.session.add_all([user, post])
        db.session.commit()

        self.user = user
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_show_post(self):
        """Checks to see that the post page displays posts."""

        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post.id}") 
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.post.title, html) 

    def test_add_post(self):
        """Checks to see that a new post is added."""
        
        with app.test_client() as client:
            d = {"post-title": "TestTitle2", "post-content": "TestContent2"}
            resp = client.post(f"/users/{self.user.id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{d["post-title"]}', html) 

    def test_delete_post(self):
        """Checks to see that a post is deleted."""
        
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(self.post.title, html) 


   