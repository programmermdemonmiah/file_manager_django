from .auth_view import RegisterView, LoginView
from .user_view import UserView
from .file_view import FileCreateView,  MoveFileView, FileInFolderView
from .folder_view import FolderCreateView, MoveFolderView, SubFolderCreateView, FolderDetailView

__all__ = ['RegisterView', "LoginView", "UserView",
           "FileCreateView", "MoveFileView", "FileInFolderView",
           "FolderCreateView", "MoveFolderView", "SubFolderCreateView", "FolderDetailView"
           
           ]