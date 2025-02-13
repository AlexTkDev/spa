from django.urls import path
from users.views import RegisterView, LogoutUser, CustomLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]