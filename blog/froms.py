import re

from django import forms
from django.core.exceptions import ValidationError
from .models import BlosUser
#
#
#   ━━━━━━神兽出没━━━━━━
#   　　　┏┓　　　┏┓
#   　　┏┛┻━━━┛┻┓
#   　　┃　　　　　　　┃
#   　　┃　　　━　　　┃
#   　　┃　┳┛　┗┳　┃
#   　　┃　　　　　　　┃
#   　　┃　　　┻　　　┃
#   　　┃　　　　　　　┃
#   　　┗━┓　　　┏━┛Code is far away from bug with the animal protecting
#   　　　　┃　　　┃    神兽保佑,代码无bug
#   　　　　┃　　　┃
#   　　　　┃　　　┗━━━┓
#   　　　　┃　　　　　　　┣┓
#   　　　　┃　　　　　　　┏┛
#   　　　　┗┓┓┏━┳┓┏┛
#   　　　　　┃┫┫　┃┫┫
#   　　　　　┗┻┛　┗┻┛
#
#   ━━━━━━感觉萌萌哒━━━━━━
#

def check_phone(phone):
    # print('--------------------------------------》',phone)
    result = r'1[13456789]\d{9}'
    phone1 = re.match(result,phone)
    if phone1:
        print('123')
        return phone1
    else:
        print('456')
        raise ValidationError('请您输入正确的手机号，我们没有时间和你在这玩')

def check_pwd(password):
    result = r'^[\d|a-z|A-Z][\d|a-z|A-Z|@]{5,19}$'
    password = re.match(result,password)
    if password:
        return password
    else:
        raise ValidationError('请输入正确密码，必须以数字或者字母开头，中间可以使用@')



class RegisterForm(forms.Form):
    name = forms.CharField(label='名字', max_length=20,required=True,min_length=3,
                           error_messages={'max_length':'名字的最大的限制为20',
                                           'required':'这个字段是必填',
                                           'min_length':"最小值为3"},
                           widget=forms.TextInput(attrs={'class':'form-control',
                                                         'id':'exampleInputEmail1',
                                                         'placeholder':'请输入用户名'}),
                           )
    phone = forms.CharField(label='手机号',required=True,validators=[check_phone]
                            ,error_messages={
                                             'required':'此字段不能为空'},
                            widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'id':'exampleInputEmail1',
                                                              'placeholder':'请输入手机号'})
                            )

    pwd = forms.CharField(label='密码1',max_length=20,min_length=6,required=True,validators=[check_pwd],
                          error_messages={'max_length':'密码的最大长度为20',
                                          'min_length':'密码的最小的长度是6',
                                          'required':'此字段不能为空'},
                          widget=forms.PasswordInput(attrs={'class':'form-control',
                                                            'id':'exampleInputEmail1',
                                                            'placeholder':'请输入密码'})
                          )


    pwd1 = forms.CharField(label='重复密码',max_length=20,min_length=6,required=True,validators=[check_pwd],
                           error_messages={'max_length':'最大的长度为20',
                                           'min_length':'最小的长度为6',
                                           'required':'此字段不能为空'},
                           widget=forms.PasswordInput(attrs={'class':'form-control',
                                                             'id':'exampleInputEmail1',
                                                             'placeholder':'请输入密码'}
                                                      )
                           )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = BlosUser.objects.filter(username=name).count()
        if count:
            raise ValidationError('用户已经存在')
        return name

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        count = BlosUser.objects.filter(phone=phone).count()
        if count:
            raise ValidationError('手机号已经存在')
        return phone

    def clean(self):
        clean_data = self.cleaned_data
        pwd1 = clean_data.get('pwd1')
        pwd2 = clean_data.get('pwd')
        if pwd1 != pwd2:
            raise ValidationError('两次密码输入不一致')
        else:
            return clean_data




class LoginForms(forms.Form):
    name = forms.CharField(label='用户名',required=True,
                            error_messages={'required':'该字断是必填字段'},
                            widget=forms.TextInput(attrs={'class':'form-control',
                                                          'id':'exampleInputEmail1',
                                                          'placeholder':'请输入用户名'}
                                                   )
                            )

    pwd = forms.CharField(label='密码',required=True,validators=[check_pwd],
                          error_messages={'required':'该字段为必填字段'},
                          widget=forms.PasswordInput(attrs={'placeholder':'请输入密码',
                                                            'class':'form-control',
                                                            'id':'exampleInputEmail1'}
                                                     )
                          )
    def clean_name(self):
        name = self.cleaned_data.get('name')
        count = BlosUser.objects.filter(username=name).count()
        if not count:
            raise ValidationError('用户已经存在')
        return name




