from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("all/", views.AllView.as_view(), name="all"),
    path("statistics/", views.statistics, name="statistics"),
    path("<int:pk>/frequency/", views.FrequencyView.as_view(), name="frequency"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    # path('createQuestion/', views.create_question, name='create_question'),
]