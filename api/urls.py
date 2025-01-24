from django.urls import path
from api.views import (
    RegisterView, LoginView, UserView,
    FolderCreateView,
    MoveFileView,
    MoveFolderView,
    FileCreateView,
    SubFolderCreateView,
    FileInFolderView,
    FolderDetailView
)


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('user-info', UserView.as_view(), name='user_view'),


    path('create-folder/', FolderCreateView.as_view(), name='create-folder'),
    path('create-file/', FileCreateView.as_view(), name='create-file'),
    path('move-file/', MoveFileView.as_view(), name='move-file'),
    path('move-folder/', MoveFolderView.as_view(), name='move-folder'),
    path('create-subfolder/', SubFolderCreateView.as_view(), name='create-subfolder'),
    path('files-in-folder/', FileInFolderView.as_view(), name='files-in-folder'),
    path('folder-detail/', FolderDetailView.as_view(), name='folder-detail'),
]


