from django.contrib.auth.models import  BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, login, first_name, last_name, password=None, birth_date=None):
        if not login:
            raise ValueError('Użytkownik musi mieć login.')

        user = self.model(
            login=login,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, first_name, last_name, birth_date=None):
        user = self.create_user(
            login=login,
            password=password,
            birth_date=birth_date,
            first_name=first_name,
            last_name=last_name,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user