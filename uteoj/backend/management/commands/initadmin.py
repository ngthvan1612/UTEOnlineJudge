from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        user_filter = User.objects.filter(username='root')
        
        if user_filter.exists():
            for user in user_filter:
                user.set_password('92ad5d248d6da148092419b836ce16c1')
                user.is_superuser = True
                user.save()
            print('------------------ FIX user root ok')
        else:
            User.objects.create_superuser(email='root@uteoj.hcmute.edu.vn', username='root', password='92ad5d248d6da148092419b836ce16c1', is_superuser=True).save()
            print('------------------ CREATE user root ok')

        user_filter = User.objects.filter(username='admin')
        if not user_filter.exists():
            print('------------------ CREATE user admin ok')
            User.objects.create_superuser(email='root@uteoj.hcmute.edu.vn', username='admin', password='1234567890', is_superuser=True).save()
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
