from django.contrib import admin
from .models import Court, Client, Case, Hearing, Document, TaskReminder

# Electronic Diary Admin Configuration

@admin.register(Court)
class CourtAdmin(admin.ModelAdmin):
    list_display = ('name', 'court_type', 'location', 'state', 'created_at')
    list_filter = ('court_type', 'state', 'created_at')
    search_fields = ('name', 'location', 'state')
    ordering = ('court_type', 'state', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'court_type', 'location', 'state')
        }),
        ('Contact Details', {
            'fields': ('address', 'contact_info'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'lawyer', 'phone', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'lawyer')
    search_fields = ('name', 'email', 'phone', 'aadhar_number', 'pan_number')
    ordering = ('-created_at', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('lawyer', 'name', 'occupation', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'address')
        }),
        ('Government IDs', {
            'fields': ('aadhar_number', 'pan_number'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'case_title', 'lawyer', 'client', 'court', 'case_type', 'status', 'priority', 'next_hearing_date', 'filing_date')
    list_filter = ('status', 'case_type', 'priority', 'court__court_type', 'filing_date', 'created_at')
    search_fields = ('case_number', 'case_title', 'client__name', 'court__name', 'description')
    ordering = ('-next_hearing_date', '-created_at')
    date_hierarchy = 'filing_date'
    
    fieldsets = (
        ('Case Details', {
            'fields': ('lawyer', 'case_number', 'case_title', 'case_type', 'filing_date')
        }),
        ('Parties & Court', {
            'fields': ('client', 'court')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Case Description', {
            'fields': ('description', 'legal_issues'),
            'classes': ('collapse',)
        }),
        ('Financial Information', {
            'fields': ('case_value', 'fees_charged', 'fees_received'),
            'classes': ('collapse',)
        }),
        ('Important Dates', {
            'fields': ('next_hearing_date', 'limitation_date'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Hearing)
class HearingAdmin(admin.ModelAdmin):
    list_display = ('case', 'hearing_date', 'hearing_type', 'status', 'court_room', 'judge_name')
    list_filter = ('status', 'hearing_type', 'hearing_date', 'created_at')
    search_fields = ('case__case_number', 'case__case_title', 'judge_name', 'court_room')
    ordering = ('-hearing_date',)
    date_hierarchy = 'hearing_date'
    
    fieldsets = (
        ('Hearing Details', {
            'fields': ('case', 'hearing_date', 'hearing_type', 'status')
        }),
        ('Court Information', {
            'fields': ('court_room', 'judge_name')
        }),
        ('Purpose & Outcome', {
            'fields': ('purpose', 'outcome', 'next_date'),
            'classes': ('collapse',)
        }),
        ('Preparation', {
            'fields': ('preparation_notes', 'documents_required', 'witnesses_required'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'case', 'document_type', 'document_date', 'is_original', 'is_certified_copy', 'created_at')
    list_filter = ('document_type', 'is_original', 'is_certified_copy', 'document_date', 'created_at')
    search_fields = ('title', 'case__case_number', 'case__case_title', 'description')
    ordering = ('-document_date', '-created_at')
    date_hierarchy = 'document_date'
    
    fieldsets = (
        ('Document Details', {
            'fields': ('case', 'title', 'document_type', 'description')
        }),
        ('File Information', {
            'fields': ('file_path', 'file_size')
        }),
        ('Document Metadata', {
            'fields': ('document_date', 'received_date', 'is_original', 'is_certified_copy')
        }),
    )

@admin.register(TaskReminder)
class TaskReminderAdmin(admin.ModelAdmin):
    list_display = ('title', 'lawyer', 'case', 'task_type', 'priority', 'due_date', 'is_completed', 'is_overdue')
    list_filter = ('is_completed', 'is_overdue', 'task_type', 'priority', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'case__case_number', 'lawyer__username')
    ordering = ('-due_date', 'priority')
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('Task Details', {
            'fields': ('lawyer', 'case', 'title', 'description')
        }),
        ('Classification', {
            'fields': ('task_type', 'priority')
        }),
        ('Timeline', {
            'fields': ('due_date', 'reminder_date')
        }),
        ('Status', {
            'fields': ('is_completed', 'completed_date', 'is_overdue')
        }),
    )
    
    readonly_fields = ('completed_date', 'created_at', 'updated_at')

# Custom admin site configuration
admin.site.site_header = "LawyerMate Electronic Diary Admin"
admin.site.site_title = "LawyerMate Admin"
admin.site.index_title = "Electronic Diary Administration"
