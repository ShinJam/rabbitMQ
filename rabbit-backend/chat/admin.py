from django.contrib import admin
from .models import ChatSession, ChatSessionMember, ChatSessionMessage


@admin.register(ChatSession, ChatSessionMessage, ChatSessionMember)
class ChatAdmin(admin.ModelAdmin):
    pass
