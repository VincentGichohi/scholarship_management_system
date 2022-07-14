from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, is_staff, password=None):
        """
        Creates a user with a given email and password
        """
        if not username:
            raise ValueError("Enter a valid username")
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(
            username=username,
            email=email,
            is_staff=True
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password=None):
        """
        Creates and saves a staff user with a given email and password
        """
        if not username:
            raise ValueError("Users must have a valid username")
        if not email:
            raise ValueError("Users must have a valid email address")
        user = self.model(
            username=username,
            email=email,
            is_staff=True
        )
        user.set_passwod(password)
        user.save(using=self._db)
        return user
        

        
    def create_superuser(self, username, email,  password=None):
        """
        Creates and saves a superuser with the given email and password
        """
        user = self.create_user(
            username=username,
            email=email,
            is_staff=True,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)

        return user

