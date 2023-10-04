from django.contrib import admin
from .models import TurnitinSubmission

class TurnitinSubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'turnitin_submission_id', 'turnitin_submission_pdf_id', 'created_at')
    search_fields = ('user__username', 'turnitin_submission_id', 'turnitin_submission_pdf_id')  # Esto te permite buscar por ciertos campos.
    list_filter = ('created_at',)  # Esto añade un filtro en el lado derecho para filtrar por fechas.

admin.site.register(TurnitinSubmission, TurnitinSubmissionAdmin)