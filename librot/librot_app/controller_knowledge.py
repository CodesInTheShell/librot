from .models import Knowledge, Chunk

class KnowledgeUtils():

    @staticmethod
    def text_to_chunks(text, words_per_chunk=55):
        words = text.split()
        chunks = []
        chunk = []
        word_count = 0

        for word in words:
            chunk.append(word)
            word_count += 1

            if word_count >= words_per_chunk:
                chunks.append(' '.join(chunk))
                chunk = []
                word_count = 0

        # Add the remaining words if any
        if chunk:
            chunks.append(' '.join(chunk))

        return chunks

def store_knowledge(knowledge_name, knowledge_description, data, advance_options={}, knowledge_from='data'):
    """

    knowledge_from = data, file, url
    """
    knowledge_obj = None
    # if knowledge_from == 'data':
    knowledge_obj = Knowledge.objects.create(
        name = knowledge_name,
        description = knowledge_description,
        knowledge_from = knowledge_from,
    )

    chunks = KnowledgeUtils.text_to_chunks(data, advance_options.get("words_per_chunk", 55))
    for chunk in chunks:
        Chunk.objects.create(
            knowledge = knowledge_obj,
            chunk_text = chunk
        )
    return knowledge_obj







