# coding=utf-8
import os


WEBSITE_INFO = {"website_name": u"Beijing Forestry University Online Judge",
                "website_name_shortcut": u"AcDay",
                "website_footer": u"北京林业大学大学信息学院 京ICP备17025039号",
                # url结尾没有/
                "url": u"www.bjfuacm.com"}


# https://github.com/QingdaoU/OnlineJudge/wiki/SMTP
SMTP_CONFIG = {"smtp_server": "smtp.domain.com",
               "email": "noreply@domain.com",
               "password": "your_password",
               "port": 25,
               "tls": True}


# 是否显示所有人的提交, False就只显示自己的
SHOW_ALL_SUBMISSIONS_LIST = True


# please set your own SECRET_KEY to a long random string
# SECRET_KEY = ""


SECRET_KEY="0b3321a8107fe382f145350b93f2ada3"
