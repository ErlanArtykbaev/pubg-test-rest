from django.urls import path
from .views import RatesView, RatesSingleView

app_name = "articles"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('rates/', RatesView.as_view()),
    path('rates/<int:pk>/', RatesSingleView.as_view()),

]