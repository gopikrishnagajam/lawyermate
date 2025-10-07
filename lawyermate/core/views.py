from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    """
    Home page view - shows different content based on user authentication status
    """
    return render(request, 'core/home.html')

def signup_view(request):
    """
    User registration view - handles both GET (show form) and POST (process form)
    """
    if request.method == 'POST':
        # Get form data from POST request
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'core/signup.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'core/signup.html')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'core/signup.html')
        
        try:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')
        except Exception as e:
            messages.error(request, 'Error creating account. Please try again.')
            return render(request, 'core/signup.html')
    
    # If GET request, just show the signup form
    return render(request, 'core/signup.html')

def login_view(request):
    """
    User login view - handles authentication
    """
    if request.method == 'POST':
        # Get login credentials
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # User credentials are valid
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect to home page or next page if specified
            next_page = request.GET.get('next', 'home')
            return redirect(next_page)
        else:
            # Invalid credentials
            messages.error(request, 'Invalid username or password!')
            return render(request, 'core/login.html')
    
    # If GET request, show login form
    return render(request, 'core/login.html')

def logout_view(request):
    """
    User logout view - logs out user and redirects to home
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

@login_required
def profile_view(request):
    """
    User profile view - only accessible to logged in users
    """
    return render(request, 'core/profile.html')


# ============================
# ELECTRONIC DIARY VIEWS
# ============================

from .models import Case, Client, Court, Hearing, Document, TaskReminder
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import date, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse

@login_required
def diary_dashboard(request):
    """
    Main dashboard for Electronic Diary showing overview of cases, hearings, and tasks
    """
    user = request.user
    
    # Get counts for dashboard cards
    total_cases = Case.objects.filter(lawyer=user).count()
    active_cases = Case.objects.filter(lawyer=user, status='ACTIVE').count()
    total_clients = Client.objects.filter(lawyer=user, is_active=True).count()
    
    # Today's hearings
    today = date.today()
    today_hearings = Hearing.objects.filter(
        case__lawyer=user,
        hearing_date__date=today,
        status='SCHEDULED'
    ).select_related('case', 'case__client')
    
    # Upcoming hearings (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_hearings = Hearing.objects.filter(
        case__lawyer=user,
        hearing_date__date__gt=today,
        hearing_date__date__lte=next_week,
        status='SCHEDULED'
    ).select_related('case', 'case__client')[:5]
    
    # Pending tasks
    pending_tasks = TaskReminder.objects.filter(
        lawyer=user,
        is_completed=False,
        due_date__gte=timezone.now()
    ).order_by('due_date')[:5]
    
    # Overdue tasks
    overdue_tasks = TaskReminder.objects.filter(
        lawyer=user,
        is_completed=False,
        due_date__lt=timezone.now()
    ).order_by('due_date')[:5]
    
    # Recent cases
    recent_cases = Case.objects.filter(lawyer=user).order_by('-created_at')[:5]
    
    context = {
        'total_cases': total_cases,
        'active_cases': active_cases,
        'total_clients': total_clients,
        'today_hearings': today_hearings,
        'upcoming_hearings': upcoming_hearings,
        'pending_tasks': pending_tasks,
        'overdue_tasks': overdue_tasks,
        'recent_cases': recent_cases,
        'today': today,
    }
    
    return render(request, 'core/diary/dashboard.html', context)


@login_required
def case_list(request):
    """
    List all cases with filtering and search functionality
    """
    user = request.user
    cases_list = Case.objects.filter(lawyer=user).select_related('client', 'court')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        cases_list = cases_list.filter(
            Q(case_number__icontains=search_query) |
            Q(case_title__icontains=search_query) |
            Q(client__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        cases_list = cases_list.filter(status=status_filter)
    
    # Filter by case type
    case_type_filter = request.GET.get('case_type', '')
    if case_type_filter:
        cases_list = cases_list.filter(case_type=case_type_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        cases_list = cases_list.filter(priority=priority_filter)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    cases_list = cases_list.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(cases_list, 20)
    page_number = request.GET.get('page')
    cases = paginator.get_page(page_number)
    
    # Get choices for filters
    status_choices = Case.CASE_STATUS
    case_type_choices = Case.CASE_TYPES
    priority_choices = Case.PRIORITY_LEVELS
    
    context = {
        'cases': cases,
        'search_query': search_query,
        'status_filter': status_filter,
        'case_type_filter': case_type_filter,
        'priority_filter': priority_filter,
        'status_choices': status_choices,
        'case_type_choices': case_type_choices,
        'priority_choices': priority_choices,
        'sort_by': sort_by,
    }
    
    return render(request, 'core/diary/case_list.html', context)


@login_required
def case_detail(request, case_id):
    """
    Detailed view of a specific case
    """
    case = get_object_or_404(Case, id=case_id, lawyer=request.user)
    
    # Get related data
    hearings = case.hearings.all().order_by('-hearing_date')
    documents = case.documents.all().order_by('-created_at')
    tasks = case.tasks.all().order_by('due_date')
    
    # Calculate statistics
    total_hearings = hearings.count()
    completed_hearings = hearings.filter(status='COMPLETED').count()
    upcoming_hearings = hearings.filter(
        hearing_date__gt=timezone.now(),
        status='SCHEDULED'
    ).count()
    
    context = {
        'case': case,
        'hearings': hearings,
        'documents': documents,
        'tasks': tasks,
        'total_hearings': total_hearings,
        'completed_hearings': completed_hearings,
        'upcoming_hearings': upcoming_hearings,
    }
    
    return render(request, 'core/diary/case_detail.html', context)


@login_required
def case_create(request):
    """
    Create a new case
    """
    if request.method == 'POST':
        try:
            # Get client
            client_id = request.POST.get('client')
            client = get_object_or_404(Client, id=client_id, lawyer=request.user)
            
            # Get court
            court_id = request.POST.get('court')
            court = get_object_or_404(Court, id=court_id)
            
            # Create case
            case = Case.objects.create(
                lawyer=request.user,
                client=client,
                court=court,
                case_number=request.POST.get('case_number'),
                case_title=request.POST.get('case_title'),
                case_type=request.POST.get('case_type'),
                filing_date=request.POST.get('filing_date'),
                status=request.POST.get('status', 'ACTIVE'),
                priority=request.POST.get('priority', 'MEDIUM'),
                description=request.POST.get('description', ''),
                legal_issues=request.POST.get('legal_issues', ''),
                case_value=request.POST.get('case_value') or None,
                fees_charged=request.POST.get('fees_charged') or None,
            )
            
            # Add next hearing if provided
            next_hearing = request.POST.get('next_hearing_date')
            if next_hearing:
                case.next_hearing_date = next_hearing
                case.save()
            
            messages.success(request, f'Case "{case.case_title}" created successfully!')
            return redirect('case_detail', case_id=case.id)
            
        except Exception as e:
            messages.error(request, f'Error creating case: {str(e)}')
    
    # Get data for form
    clients = Client.objects.filter(lawyer=request.user, is_active=True)
    courts = Court.objects.all()
    case_types = Case.CASE_TYPES
    status_choices = Case.CASE_STATUS
    priority_choices = Case.PRIORITY_LEVELS
    
    context = {
        'clients': clients,
        'courts': courts,
        'case_types': case_types,
        'status_choices': status_choices,
        'priority_choices': priority_choices,
    }
    
    return render(request, 'core/diary/case_create.html', context)


@login_required
def client_list(request):
    """
    List all clients with search functionality
    """
    user = request.user
    clients_list = Client.objects.filter(lawyer=user, is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        clients_list = clients_list.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(clients_list, 20)
    page_number = request.GET.get('page')
    clients = paginator.get_page(page_number)
    
    context = {
        'clients': clients,
        'search_query': search_query,
    }
    
    return render(request, 'core/diary/client_list.html', context)


@login_required
def client_create(request):
    """
    Create a new client
    """
    if request.method == 'POST':
        try:
            client = Client.objects.create(
                lawyer=request.user,
                name=request.POST.get('name'),
                email=request.POST.get('email', ''),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                occupation=request.POST.get('occupation', ''),
                aadhar_number=request.POST.get('aadhar_number', ''),
                pan_number=request.POST.get('pan_number', ''),
                notes=request.POST.get('notes', ''),
            )
            
            messages.success(request, f'Client "{client.name}" created successfully!')
            return redirect('client_list')
            
        except Exception as e:
            messages.error(request, f'Error creating client: {str(e)}')
    
    return render(request, 'core/diary/client_create.html')


@login_required
def hearing_list(request):
    """
    List all hearings with filtering by date
    """
    user = request.user
    hearings_list = Hearing.objects.filter(case__lawyer=user).select_related('case', 'case__client')
    
    # Date filtering
    date_filter = request.GET.get('date_filter', 'upcoming')
    today = timezone.now().date()
    
    if date_filter == 'today':
        hearings_list = hearings_list.filter(hearing_date__date=today)
    elif date_filter == 'tomorrow':
        tomorrow = today + timedelta(days=1)
        hearings_list = hearings_list.filter(hearing_date__date=tomorrow)
    elif date_filter == 'this_week':
        week_end = today + timedelta(days=7)
        hearings_list = hearings_list.filter(
            hearing_date__date__gte=today,
            hearing_date__date__lte=week_end
        )
    elif date_filter == 'upcoming':
        hearings_list = hearings_list.filter(hearing_date__date__gte=today)
    elif date_filter == 'past':
        hearings_list = hearings_list.filter(hearing_date__date__lt=today)
    
    # Status filtering
    status_filter = request.GET.get('status', '')
    if status_filter:
        hearings_list = hearings_list.filter(status=status_filter)
    
    hearings_list = hearings_list.order_by('hearing_date')
    
    # Pagination
    paginator = Paginator(hearings_list, 20)
    page_number = request.GET.get('page')
    hearings = paginator.get_page(page_number)
    
    context = {
        'hearings': hearings,
        'date_filter': date_filter,
        'status_filter': status_filter,
        'status_choices': Hearing.HEARING_STATUS,
        'today': today,
    }
    
    return render(request, 'core/diary/hearing_list.html', context)


@login_required
def task_list(request):
    """
    List all tasks and reminders
    """
    user = request.user
    tasks_list = TaskReminder.objects.filter(lawyer=user)
    
    # Filter by completion status
    status_filter = request.GET.get('status', 'pending')
    if status_filter == 'pending':
        tasks_list = tasks_list.filter(is_completed=False)
    elif status_filter == 'completed':
        tasks_list = tasks_list.filter(is_completed=True)
    elif status_filter == 'overdue':
        tasks_list = tasks_list.filter(
            is_completed=False,
            due_date__lt=timezone.now()
        )
    
    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        tasks_list = tasks_list.filter(priority=priority_filter)
    
    tasks_list = tasks_list.order_by('due_date')
    
    # Pagination
    paginator = Paginator(tasks_list, 20)
    page_number = request.GET.get('page')
    tasks = paginator.get_page(page_number)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'priority_choices': TaskReminder.PRIORITY_LEVELS,
    }
    
    return render(request, 'core/diary/task_list.html', context)


@login_required
@require_http_methods(["POST"])
def task_complete(request, task_id):
    """
    Mark a task as completed (AJAX endpoint)
    """
    task = get_object_or_404(TaskReminder, id=task_id, lawyer=request.user)
    task.mark_completed()
    
    return JsonResponse({
        'success': True,
        'message': f'Task "{task.title}" marked as completed!'
    })


@login_required
def court_list(request):
    """
    List all courts
    """
    courts_list = Court.objects.all()
    
    # Filter by court type
    court_type_filter = request.GET.get('court_type', '')
    if court_type_filter:
        courts_list = courts_list.filter(court_type=court_type_filter)
    
    # Filter by state
    state_filter = request.GET.get('state', '')
    if state_filter:
        courts_list = courts_list.filter(state__icontains=state_filter)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        courts_list = courts_list.filter(
            Q(name__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    courts_list = courts_list.order_by('court_type', 'name')
    
    # Pagination
    paginator = Paginator(courts_list, 20)
    page_number = request.GET.get('page')
    courts = paginator.get_page(page_number)
    
    context = {
        'courts': courts,
        'court_type_filter': court_type_filter,
        'state_filter': state_filter,
        'search_query': search_query,
        'court_type_choices': Court.COURT_TYPES,
    }
    
    return render(request, 'core/diary/court_list.html', context)
