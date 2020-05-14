from django.urls import path
from .views import ChatSessionView, ChatSessionMessageView

app_name = 'chat'
urlpatterns = [
    path('chats/', ChatSessionView.as_view()),
    path('chats/<uri>/', ChatSessionView.as_view()),
    path('chats/<uri>/messages/', ChatSessionMessageView.as_view()),
]