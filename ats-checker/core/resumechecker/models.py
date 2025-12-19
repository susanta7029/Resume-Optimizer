from django.db import models

# Create your models here.
class Resume(models.Model):
    resume=models.FileField(upload_to="resume")

class JobDesCription(models.Model):
    job_title=models.CharField(max_length=100)
    job_description=models.TextField()

    def __str__(self):
        return self.job_title

class AnalysisHistory(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='analyses')
    job_description = models.ForeignKey(JobDesCription, on_delete=models.CASCADE)
    rank = models.IntegerField()
    skills = models.JSONField()
    total_experience = models.FloatField()
    project_categories = models.JSONField()
    suggestions = models.JSONField(default=list)
    analyzed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-analyzed_at']
        verbose_name_plural = 'Analysis Histories'
    
    def __str__(self):
        return f"Analysis {self.id} - Score: {self.rank}%"