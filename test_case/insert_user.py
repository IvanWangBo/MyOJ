# coding=utf-8
from django.test import TestCase
import xlrd
from account.models import User
from account.models import UserProfile

class InsertUserTestCases(TestCase):
    def test_set_up_users(self):
        fname = "students.xls"
        bk = xlrd.open_workbook(fname)
        try:
            sh = bk.sheet_by_name("075719592")
        except:
            print "no sheet in %s named Sheet1" % fname
        nrows = sh.nrows
        row_list = []
        for i in range(3, nrows):
            row_data = sh.row_values(i)
            row_list.append(row_data)
        l = len(row_list)
        for i in range(l):
            data = row_list[i]
            account = {}
            account['student_id'] = data[0]
            account['real_name'] = data[1]
            account['school'] = u'北京林业大学'
            account['mail'] = '%s@bjfu.com' % data[0]
            user = User.objects.create(username=account["real_name"], real_name=account["real_name"])
            user.set_password(data[0])
            user.save()
            UserProfile.objects.create(user=user, school=data["school"], student_id=data["student_id"])
