
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import controller_knowledge
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Knowledge
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pypdf import PdfReader

@csrf_exempt
@login_required
def add_knowledge_from_data(request):
    response_data = {'message': 'message'}
    if request.method == "POST":
        data_json = json.loads(request.body)
        # print('data: ', data )

        knowledge_name = data_json.get("name", "")
        knowledge_description = data_json.get("description", "")
        data = data_json.get("data", "")
        advance_options = data_json.get("advanceOptions", {})
        print('data_json: ', data_json )
        knowledge_obj = controller_knowledge.store_knowledge(knowledge_name, knowledge_description, data, advance_options=advance_options, knowledge_from='data' )
        response_data = {'status': 'success', 'knowledgeId': knowledge_obj.id if knowledge_obj else None}

    return JsonResponse(response_data)

@csrf_exempt
@login_required
def add_knowledge_from_data_file(request):
    if request.method == 'POST':
        # Get the uploaded file and other details from the request
        uploaded_file = request.FILES.get('file')
        knowledgeNameFromFile = request.POST.get('knowledgeNameFromFile')
        knowledgeDescriptionFromFile = request.POST.get('knowledgeDescriptionFromFile')
        advance_options = request.POST.get("advanceOptions", {})

        # Process the uploaded file and other details as needed
        if uploaded_file:
            if uploaded_file.name.endswith('.pdf'):
                pdf_content = ''

                reader  = PdfReader(uploaded_file)
                num_pages = len(reader.pages)
                for page_num in range(num_pages):
                    page = reader.pages[page_num]
                    per_page_text = page.extract_text()
                    pdf_content = pdf_content+'\n'+per_page_text
                
                if pdf_content == '':
                    raise Exception(f"Can't read pdf content {knowledgeNameFromFile}")
                print('pdf_content: ',type( pdf_content))
                
                knowledge_obj = controller_knowledge.store_knowledge(knowledgeNameFromFile, knowledgeDescriptionFromFile, pdf_content, advance_options=advance_options, knowledge_from='file' )
                response_data = {'status': 'success', 'knowledgeId': knowledge_obj.id if knowledge_obj else None}
                
                # Return a success response with the details
                return JsonResponse(response_data)
            
            return JsonResponse({'error': 'Only PDF file are allowed'}, status=405)
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)



@method_decorator(login_required, name='dispatch')
class KnowledgeView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, knowledge_id=None):
        if knowledge_id:
            knowledge_obj = get_object_or_404(Knowledge, pk=knowledge_id)
            return JsonResponse({'name': knowledge_obj.name})
        else:
            knowledge_objs = Knowledge.objects.all()
            data = [{'name': knowledge_obj.name, 'id': knowledge_obj.id} for knowledge_obj in knowledge_objs]
            knowledges = { "data": data}
            return JsonResponse(knowledges)

    def put(self, request, knowledge_id):
        knowledge_obj = get_object_or_404(Knowledge, pk=knowledge_id)
        data = json.loads(request.body)
        name = data.get('name')
        if name:
            knowledge_obj.name = name
            knowledge_obj.save()
            return JsonResponse({'message': 'Knowledge updated successfully'})
        else:
            return JsonResponse({'error': 'Name field is required'}, status=400)

    def delete(self, request, knowledge_id):
        knowledge_obj = get_object_or_404(Knowledge, pk=knowledge_id)
        knowledge_obj.delete()
        return JsonResponse({'message': 'Knowledge deleted successfully'})
