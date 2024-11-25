from django.urls import path
from . import views
from .views_messages_threads import MessageThreadView, MessageView
from .views_knowledge import KnowledgeView
from . import views_knowledge 
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.login_view, name='librot_login'),
    path('logout/', views.logout_view, name='librot_logout'),
    # path('generate_response/', views.generate_response, name='generate_response'),
    # path('stream_response/', views.stream_response, name='stream_response'),
    path('receive_prompt/', views.receive_prompt, name='receive_prompt'),

    # chat threads
    path('message_threads/', MessageThreadView.as_view(), name='message_threads'),
    path('message_threads/<int:thread_id>/', MessageThreadView.as_view(), name='message_threads_id'),

    # chat messages
    path('message/<int:message_thread_id>/', MessageView.as_view(), name='message'),
    path('message/<int:message_thread_id>/<int:message_id>/', MessageView.as_view(), name='message_id'),

    # knowledges
    path('knowledges/', KnowledgeView.as_view(), name='knowledges'),
    path('knowledges/<int:knowledge_id>/', KnowledgeView.as_view(), name='knowledges_id'),

    # knowledge
    path('knowledgeFromData/',views_knowledge.add_knowledge_from_data, name='add_knowledge_from_data'),
    path('add_knowledge_from_data_file/',views_knowledge.add_knowledge_from_data_file, name='add_knowledge_from_data_file'),

    # render vue SPA
    re_path(r'^chapp/.*$', TemplateView.as_view(template_name="librot_app/chapp.html"), name='chapp'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)