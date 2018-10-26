from django.urls import path
from . import views

# Adding namespace to URLconf, this is to differentiate URL names
app_name = 'secretsanta'
urlpatterns = [
    path('secretsanta/signup/', views.SignupView.as_view(), name='signup'),
    path('secretsanta/thanks/', views.ThanksView.as_view(), name='thanks')
]
