from . import views
from django.urls import path

app_name = "main"

urlpatterns = [
    path('<int:id>', views.index, name="index"),
    path('', views.home, name="home"),
    path('create/', views.create, name="create"),
    path("login", views.login_request, name="login"),

]
