# coding=utf-8
import xlrd
from models import User
from models import UserProfile

fname = "students.xls"
bk = xlrd.open_workbook(fname)
shxrange = range(bk.nsheets)
try:
    sh = bk.sheet_by_name("075719592")
except:
    print "no sheet in %s named Sheet1" % fname
# 获取行数
nrows = sh.nrows
# 获取列数
ncols = sh.ncols
print "nrows %d, ncols %d" % (nrows, ncols)
# 获取第一行第一列数据
cell_value = sh.cell_value(1, 1)
# print cell_value

row_list = []
# 获取各行数据
for i in range(3, nrows):
    row_data = sh.row_values(i)
    row_list.append(row_data)

account_list = []
len = len(row_list)

for i in range(len):
    data = account_list[i]
    account = {}
    account['student_id'] = data[0]
    account['real_name'] = data[1]
    account['school'] = u'北京林业大学'
    account['mail'] = '%s@bjfu.com' % data[0]
    user = User.objects.create(username=account["real_name"], real_name=account["real_name"])
    user.set_password(data[0])
    user.save()
    UserProfile.objects.create(user=user, school=data["school"], student_id=data["student_id"])
