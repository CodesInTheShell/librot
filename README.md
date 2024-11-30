### Librot
Libre - Free
Libro - Book
Bot - Chatbot

Watch it here: https://www.youtube.com/watch?v=tWTNQhKNQd8&t=1s

A chatGPT like app for local that runs on your computer. Can store knowledge base data powered with RAG system.


### Running
Process below assume you already downloaded the guff files and virtualenv activated

$env:LIBROT_GPT_GUFF_PATH  = 'C:\\Users\\Dantebytes\\Documents\\Files\\guff_files\\mistral-7b-openorca.Q2_K.gguf'

$env:LIBROT_SENT_TRANS_GUFF_PATH  = 'C:\\Users\\Dantebytes\\Documents\\Files\\guff_files\\all-MiniLM-L12-v2.F32.gguf'

$env:LIBROT_SECRET_KEY  = 'librot-django-insecure-key'

python manage.py runserver 

### Experimentation app
- Add skip searching augments
- Thread pool on searching augments
- Use vector database for to embed and search, currently RAG system is just POC and not suitable solution.

### Good references
- Mistral Guff download
https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/tree/main

- Sentence similarity Guff download
https://huggingface.co/leliuga/all-MiniLM-L12-v2-GGUF/tree/main
