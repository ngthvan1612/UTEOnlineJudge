from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user_filter = User.objects.filter(username='admin')
        
        if user_filter.exists():
            for user in user_filter:
                user.username='admin'
                user.set_password('1234567890')
                user.save()
        else:
            User.objects.create_superuser(email='123@gmail.com', username='admin', password='1234567890').save()
        print('Create user admin ok')
        # if User.objects.count() == 0:
        #     for user in settings.ADMINS:
        #         username = user[0].replace(' ', '')
        #         email = user[1]
        #         password = 'admin'
        #         print('Creating account for %s (%s)' % (username, email))
        #         admin = Account.objects.create_superuser(email=email, username=username, password=password)
        #         admin.is_active = True
        #         admin.is_admin = True
        #         admin.save()
        # else:
        #     print('Admin accounts can only be initialized if no Accounts exist')

