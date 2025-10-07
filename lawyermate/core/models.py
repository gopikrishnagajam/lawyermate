from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, datetime

# Electronic Diary Models for Indian Lawyers

class Court(models.Model):
    """Model to represent Indian Courts"""
    COURT_TYPES = [
        ('SC', 'Supreme Court of India'),
        ('HC', 'High Court'),
        ('DC', 'District Court'),
        ('SC_MAG', 'Sessions Court'),
        ('MAG', 'Magistrate Court'),
        ('CJM', 'Chief Judicial Magistrate Court'),
        ('JMFC', 'Judicial Magistrate First Class'),
        ('FAMILY', 'Family Court'),
        ('CONSUMER', 'Consumer Court'),
        ('LABOUR', 'Labour Court'),
        ('TRIBUNAL', 'Tribunal'),
        ('DEBTS', 'Debts Recovery Tribunal'),
    ]
    
    name = models.CharField(max_length=200, help_text="Court Name")
    court_type = models.CharField(max_length=20, choices=COURT_TYPES)
    location = models.CharField(max_length=200, help_text="City/District")
    state = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    contact_info = models.TextField(blank=True, help_text="Phone, Email, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['court_type', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.get_court_type_display()}"


class Client(models.Model):
    """Model to represent Clients"""
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    occupation = models.CharField(max_length=100, blank=True)
    aadhar_number = models.CharField(max_length=12, blank=True, help_text="Aadhar Card Number")
    pan_number = models.CharField(max_length=10, blank=True, help_text="PAN Card Number")
    notes = models.TextField(blank=True, help_text="Additional client information")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['lawyer', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.lawyer.username}"


class Case(models.Model):
    """Model to represent Legal Cases"""
    CASE_TYPES = [
        ('CIVIL', 'Civil Case'),
        ('CRIMINAL', 'Criminal Case'), 
        ('FAMILY', 'Family Dispute'),
        ('PROPERTY', 'Property Dispute'),
        ('LABOUR', 'Labour Dispute'),
        ('CONSUMER', 'Consumer Complaint'),
        ('MATRIMONIAL', 'Matrimonial Case'),
        ('CHEQUE_BOUNCE', 'Cheque Bounce Case'),
        ('ARBITRATION', 'Arbitration'),
        ('WRIT', 'Writ Petition'),
        ('APPEAL', 'Appeal'),
        ('REVISION', 'Revision Petition'),
        ('BAIL', 'Bail Application'),
        ('COMPANY', 'Company Law'),
        ('TAX', 'Tax Matter'),
        ('BANK_RECOVERY', 'Bank Recovery'),
        ('INSURANCE', 'Insurance Claim'),
    ]
    
    CASE_STATUS = [
        ('ACTIVE', 'Active'),
        ('PENDING', 'Pending'),
        ('ADJOURNED', 'Adjourned'), 
        ('JUDGMENT_RESERVED', 'Judgment Reserved'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('SETTLED', 'Settled'),
        ('WITHDRAWN', 'Withdrawn'),
        ('DISMISSED', 'Dismissed'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cases')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='cases')
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name='cases')
    
    # Case Details
    case_number = models.CharField(max_length=50, help_text="Court Case Number")
    case_title = models.CharField(max_length=300, help_text="Short case description")
    case_type = models.CharField(max_length=20, choices=CASE_TYPES)
    filing_date = models.DateField(help_text="Date case was filed")
    
    # Status and Priority
    status = models.CharField(max_length=20, choices=CASE_STATUS, default='ACTIVE')
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='MEDIUM')
    
    # Case Description
    description = models.TextField(help_text="Detailed case description")
    legal_issues = models.TextField(blank=True, help_text="Key legal issues")
    
    # Financial Details
    case_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fees_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fees_received = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Important Dates
    next_hearing_date = models.DateTimeField(null=True, blank=True)
    limitation_date = models.DateField(null=True, blank=True, help_text="Limitation period expiry")
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-next_hearing_date', '-created_at']
        unique_together = ['lawyer', 'case_number', 'court']
    
    def __str__(self):
        return f"{self.case_number} - {self.case_title[:50]}"
    
    def get_pending_fees(self):
        """Calculate pending fees"""
        if self.fees_charged:
            return self.fees_charged - self.fees_received
        return 0
    
    def is_hearing_today(self):
        """Check if hearing is today"""
        if self.next_hearing_date:
            return self.next_hearing_date.date() == date.today()
        return False
    
    def is_hearing_overdue(self):
        """Check if hearing date has passed"""
        if self.next_hearing_date:
            return self.next_hearing_date.date() < date.today()
        return False


class Hearing(models.Model):
    """Model to track Court Hearings"""
    HEARING_TYPES = [
        ('FIRST_HEARING', 'First Hearing'),
        ('ARGUMENTS', 'Arguments'),
        ('EVIDENCE', 'Evidence Recording'),
        ('CROSS_EXAMINATION', 'Cross Examination'),
        ('FINAL_ARGUMENTS', 'Final Arguments'),
        ('JUDGMENT', 'Judgment'),
        ('MENTION', 'Mention'),
        ('INTERIM_APPLICATION', 'Interim Application'),
        ('BAIL_HEARING', 'Bail Hearing'),
        ('STATUS_CONFERENCE', 'Status Conference'),
    ]
    
    HEARING_STATUS = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('ADJOURNED', 'Adjourned'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='hearings')
    hearing_date = models.DateTimeField()
    hearing_type = models.CharField(max_length=20, choices=HEARING_TYPES)
    court_room = models.CharField(max_length=50, blank=True)
    judge_name = models.CharField(max_length=200, blank=True)
    
    # Hearing Details
    status = models.CharField(max_length=15, choices=HEARING_STATUS, default='SCHEDULED')
    purpose = models.TextField(help_text="Purpose of this hearing")
    outcome = models.TextField(blank=True, help_text="What happened in the hearing")
    next_date = models.DateTimeField(null=True, blank=True, help_text="Next hearing date if adjourned")
    
    # Preparation and Notes
    preparation_notes = models.TextField(blank=True)
    documents_required = models.TextField(blank=True)
    witnesses_required = models.TextField(blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-hearing_date']
    
    def __str__(self):
        return f"{self.case.case_number} - {self.hearing_date.strftime('%d/%m/%Y %H:%M')}"
    
    def is_today(self):
        """Check if hearing is today"""
        return self.hearing_date.date() == date.today()
    
    def is_upcoming(self):
        """Check if hearing is in future"""
        return self.hearing_date > timezone.now()


class Document(models.Model):
    """Model to store Case Documents"""
    DOCUMENT_TYPES = [
        ('PLAINT', 'Plaint/Petition'),
        ('WRITTEN_STATEMENT', 'Written Statement'),
        ('AFFIDAVIT', 'Affidavit'),
        ('EVIDENCE', 'Evidence Document'),
        ('JUDGMENT', 'Judgment/Order'),
        ('NOTICE', 'Notice'),
        ('SUMMONS', 'Summons'),
        ('APPLICATION', 'Application'),
        ('REPLY', 'Reply'),
        ('REJOINDER', 'Rejoinder'),
        ('VAKALATNAMA', 'Vakalatnama'),
        ('POWER_OF_ATTORNEY', 'Power of Attorney'),
        ('CONTRACT', 'Contract/Agreement'),
        ('CORRESPONDENCE', 'Correspondence'),
        ('RECEIPT', 'Receipt/Bill'),
        ('OTHER', 'Other'),
    ]
    
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    description = models.TextField(blank=True)
    
    # File Information
    file_path = models.CharField(max_length=500, blank=True, help_text="File system path or cloud URL")
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    
    # Document Metadata
    document_date = models.DateField(help_text="Date of the document")
    received_date = models.DateField(default=date.today)
    is_original = models.BooleanField(default=False)
    is_certified_copy = models.BooleanField(default=False)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-document_date']
    
    def __str__(self):
        return f"{self.title} - {self.case.case_number}"


class TaskReminder(models.Model):
    """Model for Task Reminders and Deadlines"""
    TASK_TYPES = [
        ('HEARING_PREP', 'Hearing Preparation'),
        ('DOCUMENT_FILING', 'Document Filing'),
        ('LIMITATION', 'Limitation Deadline'),
        ('CLIENT_MEETING', 'Client Meeting'),
        ('COURT_FEE', 'Court Fee Payment'),
        ('APPEAL_DEADLINE', 'Appeal Deadline'),
        ('COMPLIANCE', 'Compliance Matter'),
        ('FOLLOW_UP', 'Follow Up'),
        ('OTHER', 'Other Task'),
    ]
    
    PRIORITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]
    
    lawyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    case = models.ForeignKey(Case, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    task_type = models.CharField(max_length=20, choices=TASK_TYPES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='MEDIUM')
    
    # Dates
    due_date = models.DateTimeField()
    reminder_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_completed = models.BooleanField(default=False)
    is_overdue = models.BooleanField(default=False)
    
    # Tracking  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['due_date', '-priority']
    
    def __str__(self):
        return f"{self.title} - Due: {self.due_date.strftime('%d/%m/%Y')}"
    
    def mark_completed(self):
        """Mark task as completed"""
        self.is_completed = True
        self.completed_date = timezone.now()
        self.save()
    
    def check_overdue(self):
        """Check and update overdue status"""
        if not self.is_completed and self.due_date < timezone.now():
            self.is_overdue = True
            self.save()
            return True
        return False
