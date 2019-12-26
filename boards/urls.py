from django.urls import include, path
from boards import views
# from boards.views import PostUpdateView
urlpatterns =[
path('',views.home, name='home'),
# path('',views.BoardListView.as_view(),name='home'),   # for gcbv implementation
path('boards/<int:pk>/',views.board_topics, name='board_topics'),
path('boards/<int:pk>/new/',views.new_topic, name='new_topic'),
path('boards/<int:pk>/topics/<int:topic_pk>/',views.PostListView.as_view(), name='topic_posts'),
# path('boards/<int:pk>/topics/<int:topic_pk>/',views.topic_posts, name='topic_posts'),
path('boards/<int:pk>/topics/<int:topic_pk>/reply/', views.reply_topic, name='reply_topic'),
path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
path('boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/delete/', views.delete_post, name='delete_post'),
]

# urlpatterns = [
# path('', include(board_patterns)),
# ]
