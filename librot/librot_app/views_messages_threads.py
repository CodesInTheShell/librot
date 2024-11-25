from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import MessageThread, Message
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class MessageThreadView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            message_thread = MessageThread.objects.create(name=name)
            return JsonResponse({'message_thread_id': message_thread.id, 'message_thread_name': name}, status=201)
        else:
            return JsonResponse({'error': 'Name field is required'}, status=400)

    def get(self, request, thread_id=None):
        if thread_id:
            message_thread = get_object_or_404(MessageThread, pk=thread_id)
            return JsonResponse({'name': message_thread.name})
        else:
            message_threads = MessageThread.objects.all()
            data = [{'name': message_thread.name, 'id': message_thread.id} for message_thread in message_threads]
            msg_threads = { "data": data}
            return JsonResponse(msg_threads)

    def put(self, request, thread_id):
        message_thread = get_object_or_404(MessageThread, pk=thread_id)
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            message_thread.name = name
            message_thread.save()
            return JsonResponse({'message': 'Message thread updated successfully'})
        else:
            return JsonResponse({'error': 'Name field is required'}, status=400)

    def delete(self, request, thread_id):
        message_thread = get_object_or_404(MessageThread, pk=thread_id)
        message_thread.delete()
        return JsonResponse({'message': 'Message thread deleted successfully'})

@method_decorator(login_required, name='dispatch')
class MessageView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, message_thread_id=None, message_id=None):
        if message_id:
            # Get a specific message by ID
            try:
                message = Message.objects.get(id=message_id, message_thread_id=message_thread_id)
                data = {
                    'id': message.id,
                    'role': message.role,
                    'created_datetime': message.created_datetime,
                    'message': message.message,
                    'prompt_tokens': message.prompt_tokens,
                    'completion_tokens': message.completion_tokens,
                    'total_tokens': message.total_tokens
                }
                return JsonResponse(data)
            except Message.DoesNotExist:
                return JsonResponse({'error': 'Message not found'}, status=404)
        else:
            # Get all messages for a specific message thread
            messages = Message.objects.filter(message_thread_id=message_thread_id)
            data = [{'id': message.id, 'message': message.message, 'role': message.role} for message in messages]
            res = {"data": data}
            return JsonResponse(res)

    def post(self, request, message_thread_id=None):
        # Create a new message for a specific message thread
        data = request.POST  # Assuming form data is sent via POST request
        role = data.get('role')
        message_text = data.get('message')
        # Assuming other fields are provided in the form data
        
        # Create the message
        message = Message.objects.create(
            message_thread_id=message_thread_id,
            role=role,
            message=message_text,
            # Set other fields accordingly
        )
        
        return JsonResponse({'message': 'Message created successfully'}, status=201)

    def put(self, request, message_thread_id=None, message_id=None):
        # Update an existing message by ID
        data = request.POST
        # Extract data to update
        role = data.get('role')
        message_text = data.get('message')
        # Assuming other fields are provided in the form data
        
        try:
            message = Message.objects.get(id=message_id, message_thread_id=message_thread_id)
            # Update the message
            message.role = role
            message.message = message_text
            # Update other fields accordingly
            message.save()
            return JsonResponse({'message': 'Message updated successfully'})
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)

    def delete(self, request, message_thread_id=None, message_id=None):
        # Delete a message by ID
        try:
            message = Message.objects.get(id=message_id, message_thread_id=message_thread_id)
            message.delete()
            return JsonResponse({'message': 'Message deleted successfully'})
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found'}, status=404)