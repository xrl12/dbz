import datetime

from django.shortcuts import render,reverse,redirect
from django.views import View
from pure_pagination import PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

from .froms import LoginForms,RegisterForm
from .models import Banner,Article,FriendLink,Category,Nav,Comment,Tag,BlosUser

# Create your views here.

class BaseViews(View):
    def get(self,reqeuest,*args,**kwargs):
        comments = Comment.objects.filter(is_show=True).all()
        art_ids = []
        new_comments = []
        for comment in comments:
            if comment.article.id not in art_ids:
                art_ids.append(comment.article.id)
                new_comments.append(comment)
        return new_comments
    def getTime(self):
        start = datetime.datetime.strptime('2019-12-29 00:00:00', "%Y-%m-%d %H:%M:%S")
        end = (datetime.datetime.now())
        day = (end - start).days
        return day


class IndexView(BaseViews):
    def get(self,request,*args,**kwargs):
        new_comments =super().get(self,*args,**kwargs)
        banners = Banner.objects.filter(is_show=True).all()
        top_article = Article.objects.filter(is_top=True).first()
        all_article = Article.objects.filter(is_top=False).filter(is_show=True).all()
        article = Article.objects.filter(is_show=True).all()
        category = Category.objects.filter(is_show=True).all()
        friend_link = FriendLink.objects.filter(is_show=True).all()
        day = super().getTime()
        return  render(request,'index.html',locals())


class ListViews(BaseViews):
    def get(self,request,*args,**kwargs):
        new_comments =super().get(request,*args,**kwargs)
        articles = Article.objects.filter(is_show=True).all()
        tags = Tag.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        arts = Article.objects.all()
        p = Paginator(arts, per_page=1, request=request)
        articles = p.page(page)
        return render(request,'list.html',locals())

class TotailView(BaseViews):
    def get(self,request,*args,**kwargs):

        new_comments = super().get(request,*kwargs,**kwargs)
        id = kwargs.get('id')
        article = Article.objects.filter(id=id).first()
        comments = Comment.objects.filter(is_show=True).all()[:10]
        article.vnum = article.vnum+1
        article.save()


        tags = article.tag.filter(id=id).all()

        recommend_ariticle = []
        for tag in tags:
            tag_article = tag.article_set.all()
            recommend_ariticle.extend(tag_article)
        recommend_ariticle = list(set(recommend_ariticle))

        return render(request,'show.html',locals())

class CategoryView(BaseViews):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        new_comments = super().get(request,*args,**kwargs)
        try:
            category = Category.objects.get(id=id)
            articles = category.article_set.all()
            return render(request,'list.html',locals())
        except Category.DoesNotExist:
            return render(request,'404.html')


class TagView(BaseViews):
    def get(self,request,*args,**kwargs):
        id = kwargs.get('id')
        new_comments = super().get(request,*args,**kwargs)
        try:
            tag = Tag.objects.get(id=id)
            articles = tag.article_set.all()
            return render(request,'list.html',locals())
        except Category.DoesNotExist:
            return render(request,'404.html')

class Search(BaseViews):
    def get(self,request,*args,**kwargs):
        kw = request.GET.get('kw')
        article = Article.objects.filter(Q(title__contains=kw)| Q(content__icontains=kw))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # arts = Article.objects.all()
        p = Paginator(article, per_page=3, request=request)
        articles = p.page(page)
        return render(request,'list.html',locals())


class RegisterViews(BaseViews):
    def get(self,request,*args,**kwargs):
       register_form = RegisterForm()
       return render(request,'register.html',locals())
    def post(self,request,*args,**kwargs):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            phone = register_form.cleaned_data.get('phone')
            pwd = register_form.cleaned_data.get('pwd')
            name = register_form.cleaned_data.get('name')
            BlosUser.objects.create_user(phone=phone,username=name,password=pwd)
            return redirect(reverse('blog:login'))
        else:
            return render(request,'register.html',locals())
class LoginViews(BaseViews):
    def get(self,request,*args,**kwargs):
        login_form = LoginForms()
        return render(request,'login.html',locals())
    def post(self,request,*args,**kwargs):
        login_form = LoginForms(request.POST)
        if login_form.is_valid():
            # name = login_form.cleaned_data.get('name')
            pwd = login_form.cleaned_data.get('pwd')
            name = login_form.cleaned_data.get('name')

            user = authenticate(request=request,username = name,password=pwd,)
            if user:
                login(request,user)
                return redirect(reverse('blog:index'))
            else:
                return HttpResponse('123')
        else:
            return render(request,'login.html',locals())

def log_out(request):
    logout(request)
    return redirect(reverse('blog:index'))


@require_http_methods(['POST'])
@login_required #只可以用post方法
def comment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        id = request.POST.get('id')
        user = request.user
        try:
           article =  Article.objects.get(id=id)
        except Exception as e:
            return render(request,'404.html')
        Comment.objects.create(title=content,article=article,users=user)
        print(id)
        return redirect(reverse("blog:detail",kwargs={'id':id}))


