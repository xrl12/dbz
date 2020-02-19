import datetime
# from dateutil.parser import parse
from django.test import TestCase

# Create your tests here.
# print(datetime.datetime.now())
# create_time = parse('2019-12-29/00:00:00')
# now_time = datetime.datetime.now()
# (now_time-create_time).days

# import datetime
# start = datetime.datetime.strptime('2019-12-29 00:00:00', "%Y-%m-%d %H:%M:%S")
# end = (datetime.datetime.now())
# print((end - start).days)



import re
# def check_pwd(password):
#     result = r'^[\d|a-z|A-Z][\d|a-z|A-Z|@]{5,19}$'
#     abc = re.match(result,password)
#     print(abc.group())
#
#
# check_pwd('234566fgasdfghqertgys')

def check_phone(phone):
    result = r'^1[13456789]\d{9}$'
    phone = re.match(result,phone)
    print('123456')
    if phone:
        print('123')
        return phone

    else:
        print('456')
        print('请您输入正确的手机号，我们没有时间和你在这玩')

check_phone('123456')