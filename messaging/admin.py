from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'get_participants')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__username',)
    date_hierarchy = 'created_at'

    def get_participants(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    get_participants.short_description = 'Participants'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content_preview', 'conversation', 'timestamp', 'read')
    list_filter = ('read', 'timestamp', 'sender')
    search_fields = ('content', 'sender__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'