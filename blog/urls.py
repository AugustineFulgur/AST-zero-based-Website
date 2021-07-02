from django.urls import path
from . import views
app_name='blog'

urlpatterns=[
    path('',views.index),#映射到views下的index方法
    path('article/<article_id>',views.article,name="article"),#文章的链接
    path('_search',views.search),
    path('block/<block_name>',views.blocklist),
    path('block/<block_name>/',views.serienil),#无所属系列文章
    path('serie/<serie_name>',views.serielist),
    path('_ajax/_<request_type>/<request_arg>',views.ajax),
    path('article/_comment/<request_meta>',views.comment),
    path('_prefer/<article_id>',views.prefer),

]