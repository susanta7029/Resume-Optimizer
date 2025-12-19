from django.contrib import admin

# Register your models here.
from .models import Resume, JobDesCription
admin.site.register(Resume)
admin.site.register(JobDesCription)
