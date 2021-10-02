from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from backend.models.usersetting import UserSetting

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.create_superuser(email='root@uteoj.hcmute.edu.vn', username='admin', password='1234567890', is_superuser=True)
            user.save()
            usersetting = UserSetting.createSettingIfNotExists(user)
            usersetting.verified = True
            usersetting.save()
            print('Tạo tài khoản admin thành công')
        except:
            print('Tài khoản admin đã có')

