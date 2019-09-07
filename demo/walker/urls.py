from django.urls import path
from walker import views


urlpatterns = [
    path('<int:walk_id>/status/', views.CheckWalkStatusView.as_view(), name='walk_status'),
    path('start/', views.StartWalkView.as_view(), name='walk_start'),
    path('<int:walk_id>/complete/', views.CompleteWalkView.as_view(), name='walk_complete'),
]
