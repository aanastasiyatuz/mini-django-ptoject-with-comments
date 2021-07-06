from django.urls import path
from .views import RegisterApi

# если пишем на классах view, нужно указать as_view()
urlpatterns = [
      path('register/', RegisterApi.as_view()),
]