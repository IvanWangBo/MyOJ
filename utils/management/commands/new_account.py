# coding=utf-8
import sys
from django.core.management.base import BaseCommand
from account.models import User, REGULAR_USER, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.stdout.write(self.style.WARNING("Please enter account file name:"))
        file_name = raw_input()
        try:
            with open(file_name, 'r') as users:
                users = users.read()
                user_list = users.split('\n')
        except:
            self.stdout.write(self.style.WARNING("Can not find file: %s" % file_name))
            exit(1)

        for user in user_list:
            info = user.split(' ')
            name = info[0].strip()
            password = info[1].strip()
            try:
                user = User.objects.get(username=name)
                user.set_password(password)
                user.save()
            except User.DoesNotExist:
                user = User.objects.create(username=name, real_name=name[8:], email=u"bjfu_2018_cpp@oj.com", admin_type=REGULAR_USER)
                user.set_password(password)
                user.save()
                UserProfile.objects.create(user=user)
            print name, password
