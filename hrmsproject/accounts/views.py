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
    """Dashboard for authenticated users with dynamic data."""
    from django.utils import timezone
    from datetime import datetime, timedelta
    from django.db.models import Q, Sum, Count
    from master.models import Employee
    from entry.models import PermissionEntry, LeaveEntry
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    current_month_name = today.strftime('%B')
    
    # Get employee linked to user (if exists)
    employee = None
    try:
        # Try to find employee by email or username
        employee = Employee.objects.filter(
            Q(personal_email=request.user.email) | 
            Q(office_email=request.user.email) |
            Q(staff_id=request.user.username)
        ).first()
        
        # Also check if user has a profile with employee_code
        try:
            profile = request.user.profile
            if profile.employee_code:
                employee = Employee.objects.filter(staff_id=profile.employee_code).first() or employee
        except:
            pass
    except:
        pass
    
    # Permission Details (Current Month)
    permission_data = {
        'total': 0,
        'taken': 0,
        'available': 0,
        'request': 0,
    }
    
    if employee:
        # Get permission entries for current month
        permission_entries = PermissionEntry.objects.filter(
            employee=employee,
            permission_date__year=current_year,
            permission_date__month=current_month
        )
        permission_data['total'] = permission_entries.count()
        permission_data['taken'] = permission_entries.filter(status='approved').count()
        permission_data['request'] = permission_entries.filter(status='pending').count()
        # Assuming 4 permissions per month as default, adjust as needed
        permission_data['available'] = max(0, 4 - permission_data['taken'])
    
    # Leave Details (Current Month)
    leave_data = {
        'casual': {'applied': 0.0, 'taken': 0.0, 'available': 3.0},
        'earned': {'applied': 0.0, 'taken': 0.0, 'available': 3.0},
        'sick': {'applied': 0.0, 'taken': 0.0, 'available': 3.0},
    }
    
    if employee:
        # Get leave entries for current month
        leave_entries = LeaveEntry.objects.filter(
            employee=employee,
            from_date__year=current_year,
            from_date__month=current_month
        )
        
        # Casual Leave
        casual_leaves = leave_entries.filter(leave_type='casual-leave')
        leave_data['casual']['applied'] = sum([float(leave.leave_days) for leave in casual_leaves.filter(approval_status__in=['pending', 'staff_approved'])])
        leave_data['casual']['taken'] = sum([float(leave.leave_days) for leave in casual_leaves.filter(approval_status='hr_approved')])
        leave_data['casual']['available'] = max(0, 3.0 - leave_data['casual']['taken'])
        
        # Earned Leave
        earned_leaves = leave_entries.filter(leave_type='earned-leave')
        leave_data['earned']['applied'] = sum([float(leave.leave_days) for leave in earned_leaves.filter(approval_status__in=['pending', 'staff_approved'])])
        leave_data['earned']['taken'] = sum([float(leave.leave_days) for leave in earned_leaves.filter(approval_status='hr_approved')])
        leave_data['earned']['available'] = max(0, 3.0 - leave_data['earned']['taken'])
        
        # Sick Leave
        sick_leaves = leave_entries.filter(leave_type='Sick-leave')
        leave_data['sick']['applied'] = sum([float(leave.leave_days) for leave in sick_leaves.filter(approval_status__in=['pending', 'staff_approved'])])
        leave_data['sick']['taken'] = sum([float(leave.leave_days) for leave in sick_leaves.filter(approval_status='hr_approved')])
        leave_data['sick']['available'] = max(0, 3.0 - leave_data['sick']['taken'])
    
    # Calendar Data - Get attendance for current month
    calendar_data = {}
    if employee:
        # This is a placeholder - you'll need to implement actual attendance tracking
        # For now, we'll generate a basic calendar structure
        pass
    
    # Birthday Buddies (Current Month)
    birthday_buddies = Employee.objects.filter(
        date_of_birth__month=current_month
    ).exclude(date_of_birth__isnull=True).order_by('date_of_birth__day')[:10]
    
    # New Joiners (Current Month)
    new_joiners = Employee.objects.filter(
        date_of_join__year=current_year,
        date_of_join__month=current_month
    ).order_by('-date_of_join')[:10]
    
    context = {
        'employee': employee,
        'current_month': current_month_name,
        'current_year': current_year,
        'permission_data': permission_data,
        'leave_data': leave_data,
        'birthday_buddies': birthday_buddies,
        'new_joiners': new_joiners,
        'today': today,
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




