from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.IndexView.as_view(),name='index'),
    path('list/',views.ListViews.as_view(),name='list'),
    path('detail/<int:id>/',views.TotailView.as_view(),name='detail'),
    path('category/<int:id>/',views.CategoryView.as_view(),name='category'),
    path('tag/<int:id>/',views.TagView.as_view(),name='tag'),
    path('search/',views.Search.as_view(),name='search'),
    path('register/',views.RegisterViews.as_view(),name='register'),
    path('login/', views.LoginViews.as_view(), name='login'),
    path('logout/', views.log_out, name='logout'),
    path('comment/', views.comment,name='comment')

]
