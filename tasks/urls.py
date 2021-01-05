from django.urls import path
from .views import TaskView, CommentView, LoginView, FileUploadView, CommentDeleteView, TakeTaskView, CloseTaskView, AnswerCommentView, LogoutView
from django.contrib.auth import views as auth_views
app_name = "tasks"
# app_name will help us do a reverse look-up latter.

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('tasks/', TaskView.as_view()),
    path('tasks/<int:pk>', TaskView.as_view()),
    path('comments/', CommentView.as_view()),
    path('comments/<int:pk>', CommentView.as_view()),
    path('files/', FileUploadView.as_view()),
    path('comments/delete/<int:pk>', CommentDeleteView.as_view()),
    path('comments/answer/<int:pk>', AnswerCommentView.as_view()),
    path('tasks/take/<int:pk>', TakeTaskView.as_view()),
    path('tasks/close/<int:pk>', CloseTaskView.as_view()),
]