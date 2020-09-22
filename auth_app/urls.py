from django.urls import path
from auth_app import views
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('auth/', views.auth, name="auth"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]