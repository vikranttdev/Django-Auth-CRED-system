from django.contrib import admin
from django.urls import path
from app import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/',admin.site.urls),
    path('', user_views.home, name='home'),
    path('signup/', user_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='lms/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='lms/logout.html'), name='logout'),
    path('cred/', user_views.cred, name='cred'),
    path('add', user_views.add, name='add'),
    path('edit', user_views.edit, name='edit'),
    path('update/<str:id>', user_views.update, name='update'),
    path('delete/<str:id>', user_views.delete, name='delete'),
    path('password_change', user_views.password_change, name='password_change'),
    path('password_reset', user_views.password_reset_request, name="password_reset"),
    path('forget-password/',user_views.ForgetPassword , name="forget_password"),
    path('change-password/<token>/',user_views.ChangePassword , name="change_password"),


]