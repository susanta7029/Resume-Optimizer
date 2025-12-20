from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from.serializer import JobDescriptionSerializer,JobDesCription,ResumeSerializer,Resume,AnalysisHistorySerializer,AnalysisHistory
from.analyzer import process_resume
import logging

logger = logging.getLogger(__name__)

class JobDescriptionAPI(APIView):
    def get(self,request):
        queryset=JobDesCription.objects.all()
        serializer=JobDescriptionSerializer(queryset,many=True)
        return Response(
    {
        'status':True,
        'data':serializer.data

    })

class AnalyzeResmeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data.get('job_description') or not data.get('resume'):
                return Response(
                    {
                        'status': False,
                        'messages': 'Job description and resume are required',
                        'data': {}
                    }
                )

            serializer = ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response(
                    {
                        'status': False,
                        'messages': 'Validation errors',
                        'data': serializer.errors
                    }
                )

            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id=_data['id'])
            resume_path = resume_instance.resume.path
            job_desc = JobDesCription.objects.get(id=data.get('job_description'))
            
            # Analyze resume
            analysis_data = process_resume(resume_path, job_desc.job_description)
            
            # Save to history
            AnalysisHistory.objects.create(
                resume=resume_instance,
                job_description=job_desc,
                rank=analysis_data.get('rank', 0),
                skills=analysis_data.get('skills', []),
                total_experience=analysis_data.get('total_experience', 0),
                project_categories=analysis_data.get('project_categories', []),
                suggestions=analysis_data.get('suggestions', [])
            )

            return Response({
                'status': True,
                'message': 'Resume analyzed successfully',
                'data': analysis_data
            })

        except Exception as e:
            logger.error(f"Error analyzing resume: {str(e)}", exc_info=True)
            return Response({
                'status': False,
                'message': f'Error: {str(e)}',
                'data': {}
            })

class AnalysisHistoryAPI(APIView):
    def get(self, request):
        try:
            # Get the last 10 analyses
            analyses = AnalysisHistory.objects.all()[:10]
            serializer = AnalysisHistorySerializer(analyses, many=True)
            return Response({
                'status': True,
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': f'Error: {str(e)}',
                'data': []
            })

