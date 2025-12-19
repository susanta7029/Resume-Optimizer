from rest_framework import serializers
from.models import JobDesCription,Resume,AnalysisHistory

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDesCription
        fields = '__all__'

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'

class AnalysisHistorySerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job_description.job_title', read_only=True)
    
    class Meta:
        model = AnalysisHistory
        fields = ['id', 'rank', 'skills', 'total_experience', 'project_categories', 
                  'suggestions', 'analyzed_at', 'job_title']