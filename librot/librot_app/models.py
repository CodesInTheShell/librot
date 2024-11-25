from django.db import models

class MessageThread(models.Model):
    name = models.CharField(max_length=255)

class Message(models.Model):
    ROLE_CHOICES = [
        ('bot', 'Bot'),
        ('user', 'User'),
    ]

    message_thread_id = models.ForeignKey(MessageThread, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_datetime = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    prompt_tokens = models.IntegerField(null=True)
    completion_tokens = models.IntegerField(null=True)
    total_tokens = models.IntegerField(null=True)


class Knowledge(models.Model):
    name = models.CharField(max_length=100)
    knowledge_from = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.name

class Chunk(models.Model):
    knowledge = models.ForeignKey(Knowledge, on_delete=models.CASCADE)
    chunk_text = models.TextField()

    def __str__(self):
        return f"Chunk for {self.knowledge.name}"