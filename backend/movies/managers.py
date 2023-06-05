from django.contrib.auth.models import  BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, firstname, lastname, password=None, birthdate=None,
                    isadmin=False):
        if not username:
            raise ValueError('Użytkownik musi mieć login.')

        user = self.model(
            username=username,
            # login=username,
            birthdate=birthdate,
            firstname=firstname,
            lastname=lastname,
            isadmin=isadmin
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, firstname, lastname, birthdate=None):
        user = self.create_user(
            # login=login,
            username=login,
            password=password,
            birthdate=birthdate,
            firstname=firstname,
            lastname=lastname,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user