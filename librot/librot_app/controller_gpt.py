
from llama_cpp import Llama
import os 
from .models import Message, MessageThread

END_CUT = '[/INST]'

model_path = os.environ.get('LIBROT_GPT_GUFF_PATH')

# from huggingface_hub import hf_hub_download
# # from llama_cpp import Llama

# ## Define model name and file name
# model_name = "google/gemma-2b-it"
# model_file = "gemma-2b-it.gguf"


# ## Download the model
# model_path = hf_hub_download(model_name, filename=model_file)
# print('model_path: ', model_path)

llm = Llama(
    model_path=model_path,
    chat_format="llama-2",
    verbose=False,
    )

def process_received_prompt(user_prompt, thread_id, knowledge_only=False, system_prompt=None, stream=False):
    messages = messages_preprocess(user_prompt, system_prompt)
    print('-----prom--------')
    print(messages)
    generated_response = llm.create_chat_completion(messages, stream = stream)
    
    print('----resp--------')
    print(generated_response)
    print('----------------')

    msg_thread = MessageThread.objects.get(id=thread_id)

    Message.objects.create(
        message_thread_id=msg_thread,
        role='user',
        message=user_prompt,
    )

    if generated_response['choices'][0]['message']['content'] == '\n':
        message_content = 'Sorry and I do not have a knowledge about it.'
    else:
        content_response = generated_response['choices'][0]['message']['content']
        end_index = content_response.find(END_CUT)
        # message_content = content_response[:end_index].strip()
        message_content = content_response.split(END_CUT)[0]
    

    Message.objects.create(
            message_thread_id=msg_thread,
            role='bot',
            message=message_content,
            prompt_tokens=generated_response['usage']['prompt_tokens'],
            completion_tokens=generated_response['usage']['completion_tokens'],
            total_tokens=generated_response['usage']['total_tokens'],
        )
    return generated_response
        

def messages_preprocess(user_prompt, system_prompt=None):

    if not system_prompt:
        system_prompt = {
                "role": "system",
                "content": "You are an assistant."
            }

    messages = [
            system_prompt,
            {
                "role": "user",
                "content":user_prompt
            }
        ]
    return messages