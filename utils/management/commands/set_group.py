# coding=utf-8
import sys
from django.core.management.base import BaseCommand
from account.models import User, REGULAR_USER, UserProfile
from group.models import Group
from group.views import join_group


class Command(BaseCommand):
    def handle(self, *args, **options):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        with open('group_1', 'r') as users:
            users = users.read()
            user_list = users.split('\n')

        for user in user_list:
            info = user.split(' ')
            name = info[0]
            group_id = info[1]
            try:
                user = User.objects.get(username=name)
                group = Group.objects.get(id=group_id)
                join_group(user, group)
                print 'success', name, group_id
            except :
                print 'error', name, group_id
