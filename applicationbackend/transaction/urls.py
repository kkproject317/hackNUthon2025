from django.urls import path
from .views import transactions,admin

urlpatterns = [
    path('user/',transactions,name='userTransaction'),
    path('admin/',admin,name="admin")
]
