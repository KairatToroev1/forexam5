from django.urls import path
from .views import (LoginView,
                    RegisterView,
                    logout_view,)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_url'),
    path('register/', RegisterView.as_view(), name='register_url'),
    path('logout/', logout_view, name='logout_url'),
]