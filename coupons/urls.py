from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('logs', views.logs, name='log'),
    path('scrape/<int:website_id>', views.bs4_scrape, name='scrape'),
    path('isfree', views.IsFree, name='isfree'),
    path('print', views.printy, name='print'),
    # path('<int:year>/<int:month>/<int:day>/<slug:post>/',
    #      views.post_detail,
    #      name='post_detail'),
    # path('<int:post_id>/share/', views.post_share,
    #      name='post_share')
]