# coding=utf-8
from django.core.management.base import BaseCommand
from account.models import User, REGULAR_USER, UserProfile
from utils.shortcuts import rand_str


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open('password', 'r') as users:
            users = users.read()
            user_list = users.split('\n')

        for user in user_list:
            info = user.split(' ')
            name = info[0]
            password = info[1]
            user = User.objects.create(username=name, real_name=name[9:], email="%s@oj.com" % name[:9], admin_type=REGULAR_USER)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS("Successfully created user.\n"
                                                 "Username: %s\nPassword: %s\n"
                                                 "Remember to change password and turn on two factors auth "
                                                 "after installation." % (name, password)))
