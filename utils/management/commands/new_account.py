# coding=utf-8
import sys
from django.core.management.base import BaseCommand
from account.models import User, REGULAR_USER, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open('password', 'r') as users:
            users = users.read()
            user_list = users.split('\n')

        for user in user_list:
            info = user.split(' ')
            name = info[0]
            password = info[1]
            try:
                user = User.objects.get(username=name)
                user.set_password(password)
                user.save()
            except User.DoesNotExist:
                user = User.objects.create(username=name, real_name=name[9:], email=u"%s@oj.com" % name[:9], admin_type=REGULAR_USER)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(user=user)
