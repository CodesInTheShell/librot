from sentence_transformers import SentenceTransformer, util
import os
from .models import Chunk

# SENT_TRANS_NAME = os.environ.get('LIBROT_SENT_TRANS')

# sent_trans_model = SentenceTransformer(SENT_TRANS_NAME)

# # query_embedding = sent_trans_model.encode('How big is London')
# # passage_embedding = sent_trans_model.encode(['London has 9,787,426 inhabitants at the 2011 census. London is known for its finacial district'])

# # print("Testing Similarity:", float(util.dot_score(query_embedding, passage_embedding)[0][0]))

# def get_contexts(text_input, similarity_percent=50, number_of_references=3, similar_chunk_limit_to_fetch=20):
#     print('--------------get_contexts-------------------')

#     query_embedding = sent_trans_model.encode(text_input)

#     similarity_chunks = []

#     chunks = Chunk.objects.all()
#     for chunk in chunks:
#         # print('chunk.chunk_text: ', chunk.chunk_text)
#         # print('chunk.chunk_text: ', chunk.chunk_text)
#         # passage_embedding = sent_trans_model.encode([chunk.chunk_text])
#         passage_embedding = sent_trans_model.encode(chunk.chunk_text)
#         resulting_percent = float(util.dot_score(query_embedding, passage_embedding)[0][0])
#         # print('resulting_percent: ', resulting_percent)
#         if resulting_percent > float(similarity_percent/100.0):
#             similarity_chunks.append({'text': chunk.chunk_text, 'score': resulting_percent})
#             if len(similarity_chunks) > similar_chunk_limit_to_fetch:
#                 break
        
#     if len(similarity_chunks) < 0:
#         return [] 
#     else:
#         sorted_sliced_similarity_chunks = sorted(similarity_chunks, key=lambda x: x['score'], reverse=True)[:number_of_references]
#         # print('sorted_sliced_similarity_chunks: ', sorted_sliced_similarity_chunks)
#         return sorted_sliced_similarity_chunks
    
### USING LLAMA
from llama_cpp import Llama
SENT_TRANS_GUFF_PATH = os.environ.get('LIBROT_SENT_TRANS_GUFF_PATH')
print('SENT_TRANS_GUFF_PATH: ', SENT_TRANS_GUFF_PATH)

sent_trans_model = Llama(
    model_path=SENT_TRANS_GUFF_PATH,
    embedding=True,
    verbose=False,
    )


def get_contexts(text_input, similarity_percent=50, number_of_references=3, similar_chunk_limit_to_fetch=20):
    print('--------------get_contexts-------------------')

    query_embedding = sent_trans_model.create_embedding(text_input)
    query_embedding = query_embedding['data'][0]['embedding']
    # print('query_embedding: ', query_embedding)

    similarity_chunks = []

    chunks = Chunk.objects.all()
    for chunk in chunks:
        passage_embedding = sent_trans_model.create_embedding(chunk.chunk_text)
        passage_embedding = passage_embedding['data'][0]['embedding']
        # print('passage_embedding: ', passage_embedding)
        
        resulting_percent = float(util.dot_score(query_embedding, passage_embedding)[0][0])
        print('resulting_percent: ', resulting_percent)
        if resulting_percent > float(similarity_percent/100.0):
            similarity_chunks.append({'text': chunk.chunk_text, 'score': resulting_percent})
            if len(similarity_chunks) > similar_chunk_limit_to_fetch:
                break
        
    if len(similarity_chunks) < 0:
        return [] 
    else:
        sorted_sliced_similarity_chunks = sorted(similarity_chunks, key=lambda x: x['score'], reverse=True)[:number_of_references]
        # print('sorted_sliced_similarity_chunks: ', sorted_sliced_similarity_chunks)
        print('sorted_sliced_similarity_chunks: ', sorted_sliced_similarity_chunks)
        return sorted_sliced_similarity_chunks
        
    
    


        

