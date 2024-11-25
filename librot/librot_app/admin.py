from django.contrib import admin
from .models import MessageThread, Message, Knowledge, Chunk

class MessageAdmin(admin.ModelAdmin):
    list_display = ('role', 'created_datetime', 'message', 'prompt_tokens', 'completion_tokens', 'total_tokens')
    list_filter = ('role', 'created_datetime')
    search_fields = ('message',)

class MessageThreadAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class KnowledgeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class ChunkAdmin(admin.ModelAdmin):
    list_display = ('chunk_text', 'get_knowledge_name')
    search_fields = ('chunk_text',)

    def get_knowledge_name(self, obj):
        return obj.knowledge.name
    
    get_knowledge_name.short_description = 'Knowledge Name'



admin.site.register(Message, MessageAdmin)
admin.site.register(MessageThread, MessageThreadAdmin)
admin.site.register(Chunk, ChunkAdmin)
admin.site.register(Knowledge, KnowledgeAdmin)
