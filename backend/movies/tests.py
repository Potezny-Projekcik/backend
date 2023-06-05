from .models import User
from django.contrib.auth.hashers import check_password

def create_user_and_check_password():
    # create a user
    user = User(username='myuser')
    user.set_password('mypassword')
    user.save()

    # check the password
    print(check_password('mypassword', user.password))  # Should print: True

