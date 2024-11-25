from django.shortcuts import render, redirect
from django.http import JsonResponse
from . import controller_gpt, controller_sentence_trans
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import StreamingHttpResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return redirect('librot_login')

def login_view(request):
    if request.method == 'POST':
        print('POST: ', request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print('user: ', user)
        print('username: ', username)
        print('password: ', password)
        if user is not None:
            login(request, user)
            return redirect('chapp')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid username or password')  # Display error message
            return redirect('librot_login')  # Redirect back to the login page
    else:
        if request.user.is_authenticated:
            return redirect('chapp')
        else:
            return render(request, 'librot_app/login.html')

@login_required
def chapp(request):
    return render(request, 'librot_app/chapp.html')

@csrf_exempt
@login_required
def receive_prompt(request):
    response_data = {'message': 'message'}
    if request.method == "POST":
        data = json.loads(request.body)
        user_prompt = data.get("user_prompt")
        knowledge_only = data.get("knowledgeOnly", False)
        thread_id = data.get("threadId")
        print('knowledge_only', knowledge_only)

        #get knowledge context
        references = controller_sentence_trans.get_contexts(user_prompt)
        if references == []:
            augmented_knowledge = 'None'
        else:
            augmented_knowledge = ''
            for r in references:
                augmented_knowledge += r.get('text')+'\n'
        
        context_text = f"ADDITIONAL KNOWLEDGE: {augmented_knowledge}"
        
        if knowledge_only and references == []:
            system_prompt_content = "Strictly just respond with the following sentence 'Sorry and I do not have a knowledge about it.'"
        else: 
            system_prompt_content = "You are an assistant, respond base on data you are pretrained and besure to undestand and use the additional knowledge if available for more reference."+'\n\n'+context_text
        
        

        system_prompt = {
                "role": "system", 
                "content": system_prompt_content
            }
        print('system_prompt: ', system_prompt)


        gpt_output = controller_gpt.process_received_prompt(user_prompt, thread_id, knowledge_only=knowledge_only, system_prompt=system_prompt)
        # content = gpt_output['choices'][0]['message']['content']
        if gpt_output['choices'][0]['message']['content'] == '\n':
            message_content = 'Sorry and I do not have a knowledge about it.'
        else:
            message_content = gpt_output['choices'][0]['message']['content']
        response_data = {'message': message_content, 'references': references}

    return JsonResponse(response_data)

# @csrf_exempt
# def generate_response(request):
#     response_data = {}
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_prompt = data.get("user_prompt")
#         request.session['user_prompt'] = user_prompt
#         return HttpResponseRedirect(reverse('stream_response'))
#     return JsonResponse(response_data)

# def stream_response(request):
#     user_prompt = request.session.get('user_prompt', '')

#     def stream_data(response_data):
#         for r in response_data:
#             print('r: ', r['choices'][0].get('delta', {}).get('content', ''))
#             yield r['choices'][0].get('delta', {}).get('content', '')

#     generated_response = controller_gpt.llm.create_chat_completion(
#         messages = [
#                     # {
#                     #     "role": "system", 
#                     #     "content": "You are an analyst who is an genius."
#                     # },
#                     {
#                         "role": "user",
#                         "content":user_prompt
#                     },
#                 ],
#                 stream = True
#             )
    
#     response_data = {'generated_response': generated_response}
#     response = StreamingHttpResponse(stream_data(generated_response), content_type="text/event-stream")
#     response['Cache-Control'] = 'no-cache'
#     return response