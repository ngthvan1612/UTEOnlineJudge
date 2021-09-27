from django.contrib.auth.hashers import PBKDF2PasswordHasher

class UTEOJ_PBKDF2PasswordHasher(PBKDF2PasswordHasher):
    iterations = 16