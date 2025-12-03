import calendar
from datetime import date

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .forms import ProfileForm
from .models import Profile


# ==================== Home & Authentication ====================
def home(request):
    """Redirect unauthenticated users to login, others to dashboard."""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    """Dashboard for authenticated users."""
    # Get current date
    today = date.today()
    current_year = today.year
    current_month = today.month
    
    # Calculate calendar structure
    month_name = calendar.month_name[current_month]  # e.g., "January"
    first_day = date(current_year, current_month, 1)
    last_day = date(current_year, current_month, calendar.monthrange(current_year, current_month)[1])
    
    # Get weekday of first day (0=Monday, 6=Sunday)
    # Adjust to match calendar display (Sunday=0, Monday=1, ..., Saturday=6)
    first_day_weekday = (first_day.weekday() + 1) % 7  # Convert Monday=0 to Sunday=0
    
    # Calculate days in month
    days_in_month = calendar.monthrange(current_year, current_month)[1]
    
    # Create calendar days list
    calendar_days = []
    
    # Calculate previous month's last day (for showing dates before current month)
    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year
    
    prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
    
    # Add empty cells for days before month starts (show previous month dates)
    for i in range(first_day_weekday):
        prev_day = prev_month_days - first_day_weekday + i + 1
        calendar_days.append({
            'date': None,
            'day': prev_day,
            'is_current_month': False,
            'is_today': False,
            'status': None,
        })
    
    # Add all days of current month
    for day in range(1, days_in_month + 1):
        day_date = date(current_year, current_month, day)
        is_today = (day_date == today)
        
        calendar_days.append({
            'date': day_date,
            'day': day,
            'is_current_month': True,
            'is_today': is_today,
            'status': None,  # Will be populated with attendance data if available
            'weekday': day_date.weekday(),  # 0=Monday, 6=Sunday
        })
    
    # Add empty cells to complete last week (show next month dates)
    last_day_weekday = (last_day.weekday() + 1) % 7
    cells_to_add = 6 - last_day_weekday
    next_day = 1
    for _ in range(cells_to_add):
        calendar_days.append({
            'date': None,
            'day': next_day,
            'is_current_month': False,
            'is_today': False,
            'status': None,
        })
        next_day += 1
    
    # Optional: Fetch attendance data for logged-in user
    # This can be enhanced later to fetch actual attendance records
    attendance_data = {}
    
    # Try to get employee record if user has profile with employee_code
    try:
        profile = request.user.profile
        if profile.employee_code:
            # Link to Employee model if needed
            # from master.models import Employee
            # employee = Employee.objects.filter(staff_id=profile.employee_code).first()
            # if employee:
            #     # Fetch attendance records, leaves, week offs, etc.
            pass
    except:
        pass
    
    # Initialize default values for dashboard statistics
    # These will be populated from database in future
    permission_month = calendar.month_abbr[current_month]  # e.g., "Jan"
    
    # Permission Details (default values - to be fetched from PermissionEntry model)
    permission_total = 0
    permission_taken = 0
    permission_available = 0
    permission_request = 0
    
    # Leave Details (default values - to be fetched from LeaveEntry model)
    casual_leave_available = 0
    casual_leave_applied = 0.0
    casual_leave_taken = 0.0
    
    earned_leave_available = 0
    earned_leave_applied = 0.0
    earned_leave_taken = 0.0
    
    sick_leave_available = 0
    sick_leave_applied = 0.0
    sick_leave_taken = 0.0
    
    # Birthday Buddies (default empty list - to be fetched from Employee model)
    birthday_buddies = []
    
    # New Joiners (default empty list - to be fetched from Employee model)
    new_joiners = []
    
    # Announcement (default empty - to be fetched from Announcement model if exists)
    announcement_text = ""
    
    context = {
        'calendar_year': current_year,
        'calendar_month': current_month,
        'calendar_month_name': month_name,
        'calendar_days': calendar_days,
        'attendance_data': attendance_data,
        'today': today,
        # Permission Details
        'permission_month': permission_month,
        'permission_total': permission_total,
        'permission_taken': permission_taken,
        'permission_available': permission_available,
        'permission_request': permission_request,
        # Leave Details
        'casual_leave_available': casual_leave_available,
        'casual_leave_applied': casual_leave_applied,
        'casual_leave_taken': casual_leave_taken,
        'earned_leave_available': earned_leave_available,
        'earned_leave_applied': earned_leave_applied,
        'earned_leave_taken': earned_leave_taken,
        'sick_leave_available': sick_leave_available,
        'sick_leave_applied': sick_leave_applied,
        'sick_leave_taken': sick_leave_taken,
        # Birthday Buddies
        'birthday_buddies': birthday_buddies,
        # New Joiners
        'new_joiners': new_joiners,
        # Announcement
        'announcement_text': announcement_text,
    }
    
    return render(request, 'accounts/dashboard.html', context)


def login_view(request):
    """Render and process the login form."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            
            # Check if user must change password
            try:
                from .models import Profile
                profile = user.profile
                if profile.must_change_password:
                    return redirect('accounts:change_password_required')
            except:
                pass
            
            return redirect('accounts:dashboard')
        messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    """Render and process the registration form."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('accounts:login')
        messages.error(request, 'Registration failed. Please correct the highlighted fields.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    """Log out the current user."""
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


# ==================== Profile & Settings ====================
@login_required
def profile(request):
    """Display and update the user's profile."""
    profile_obj, _ = Profile.objects.get_or_create(user=request.user)
    email_value = request.user.email
    email_error = ''

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_obj)
        email_value = request.POST.get('email', '').strip()

        if not email_value:
            email_error = 'Email is required.'
        else:
            try:
                validate_email(email_value)
            except ValidationError:
                email_error = 'Enter a valid email address.'

        if form.is_valid() and not email_error:
            form.save()
            if email_value != request.user.email:
                request.user.email = email_value
                request.user.save(update_fields=['email'])
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
        messages.error(request, email_error or 'Please correct the highlighted errors.')
    else:
        form = ProfileForm(instance=profile_obj)

    primary_group = request.user.groups.first()
    context = {
        'display_name': request.user.get_full_name() or request.user.username,
        'primary_group_name': primary_group.name if primary_group else ('Admin' if request.user.is_superuser else ''),
        'profile': profile_obj,
        'form': form,
        'email_value': email_value,
        'email_error': email_error,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def inbox(request):
    """Placeholder inbox view."""
    return render(request, 'accounts/inbox.html')


@login_required
def settings_view(request):
    """Placeholder settings view."""
    return render(request, 'accounts/settings.html')


# ==================== Accounts ====================
@login_required
def cash_reports_list(request):
    """Accounts -> Cash Reports list."""
    return render(request, 'accounts/cash_reports/list.html')


# ==================== Demo ====================
@login_required
def demo_add(request):
    return render(request, 'accounts/demo/add.html')


@login_required
def demo_store(request):
    if request.method == 'POST':
        messages.success(request, 'Demo item saved successfully!')
        return redirect('accounts:demo_list')
    return redirect('accounts:demo_add')


@login_required
def demo_list(request):
    return render(request, 'accounts/demo/list.html')




