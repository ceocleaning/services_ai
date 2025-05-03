from django.db import models
from business.models import Business




class RetellAgent(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=100)
    retell_agent_id = models.CharField(max_length=100)
    retell_phone_number = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.agent_name

    class Meta:
        verbose_name = "Retell Agent"
        verbose_name_plural = "Retell Agents"
        ordering = ["-created_at"]
