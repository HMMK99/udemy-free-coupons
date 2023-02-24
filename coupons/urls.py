from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('logs', views.logs, name='log')
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    #      views.post_detail,
    #      name='post_detail'),
    # path('<int:post_id>/share/', views.post_share,
    #      name='post_share')
]