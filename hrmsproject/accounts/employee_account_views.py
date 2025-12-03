"""
Views for employee account creation and management.
HR creates accounts with temporary passwords, employees verify and change password.
"""
import secrets
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST, require_http_methods

from master.models import Employee
from .models import Profile

User = get_user_model()


@permission_required('master.add_employee', raise_exception=True)
@require_http_methods(["GET", "POST"])
def create_employee_account(request, employee_id):
    """
    HR creates a user account for an employee with temporary password.
    """
    employee = get_object_or_404(Employee, pk=employee_id)
    
    # Check if employee already has an account
    # Find user through Profile using employee_code
    from .models import Profile
    user_exists = Profile.objects.filter(employee_code=employee.staff_id).exists()
    if user_exists:
        messages.warning(request, f'Employee {employee.staff_name} already has a user account.')
        return redirect('master:employee_list')
    
    if request.method == 'POST':
        # Generate temporary password
        temp_password = secrets.token_urlsafe(12)  # Generate secure temporary password
        
        # Create username from employee code or staff_id
        username = employee.staff_id.lower().replace(' ', '_')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            username = f"{username}_{employee.id}"
        
        # Create user account
        user = User.objects.create_user(
            username=username,
            email=employee.personal_email or employee.office_email or f"{username}@company.com",
            password=temp_password,
            first_name=employee.staff_name.split()[0] if employee.staff_name else '',
            last_name=' '.join(employee.staff_name.split()[1:]) if len(employee.staff_name.split()) > 1 else '',
            is_active=False,  # Account inactive until verified
        )
        
        # Create or update profile
        profile, created = Profile.objects.get_or_create(user=user)
        profile.employee_code = employee.staff_id
        profile.must_change_password = True
        profile.account_verified = False
        verification_token = profile.generate_verification_token()
        profile.save()
        
        # Note: Employee model doesn't have a direct user field
        # The relationship is maintained through Profile.employee_code = Employee.staff_id
        
        # Send verification email (optional - you can implement email sending)
        # send_verification_email(user, verification_token, temp_password, employee)
        
        # SECURITY: Do not display sensitive credentials in messages
        # Store them temporarily in session for display on next page only, or send via email
        # For now, just show success without sensitive data
        messages.success(
            request,
            f'Account created successfully for {employee.staff_name}. '
            f'Username: {username}. '
            f'Please provide the temporary password and verification token to the employee securely (via email or in person).'
        )
        
        # Store sensitive data in session temporarily (will be cleared after first access)
        # This allows showing it once on a secure page if needed
        request.session['new_account_credentials'] = {
            'employee_id': employee.id,
            'username': username,
            'temp_password': temp_password,
            'verification_token': verification_token,
            'verification_url': request.build_absolute_uri(
                reverse('accounts:verify_employee_account', args=[verification_token])
            ),
        }
        request.session['new_account_credentials_shown'] = False
        
        return redirect('master:employee_list')
    
    context = {
        'employee': employee,
    }
    return render(request, 'accounts/create_employee_account.html', context)


@require_http_methods(["GET", "POST"])
def verify_employee_account(request, token):
    """
    Employee verifies their account using the verification token.
    """
    try:
        profile = Profile.objects.get(verification_token=token)
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid verification token.')
        return redirect('accounts:login')
    
    if not profile.is_verification_token_valid():
        messages.error(request, 'Verification token has expired. Please contact HR.')
        return redirect('accounts:login')
    
    if request.method == 'POST':
        # Activate account
        profile.user.is_active = True
        profile.user.save()
        profile.account_verified = True
        profile.verification_token = None  # Clear token after verification
        profile.verification_token_expires = None
        profile.save()
        
        messages.success(request, 'Account verified successfully! Please login with your credentials.')
        return redirect('accounts:login')
    
    # Find employee through Profile.employee_code matching Employee.staff_id
    employee = None
    if profile.employee_code:
        try:
            employee = Employee.objects.get(staff_id=profile.employee_code)
        except Employee.DoesNotExist:
            pass
    
    context = {
        'profile': profile,
        'employee': employee,
    }
    return render(request, 'accounts/verify_employee_account.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def change_password_required(request):
    """
    Force password change page for employees with temporary passwords.
    """
    try:
        profile = request.user.profile
    except AttributeError:
        # Django OneToOneField raises AttributeError when related object doesn't exist
        # If no profile, redirect to dashboard
        return redirect('accounts:dashboard')
    
    if not profile.must_change_password:
        return redirect('accounts:dashboard')
    
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        # Validate passwords
        if not old_password or not new_password or not confirm_password:
            messages.error(request, 'All password fields are required.')
        elif not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
        elif len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
        else:
            # Change password
            request.user.set_password(new_password)
            request.user.save()
            profile.must_change_password = False
            profile.save()
            
            messages.success(request, 'Password changed successfully!')
            return redirect('accounts:dashboard')
    
    return render(request, 'accounts/change_password_required.html')


@permission_required('master.change_employee', raise_exception=True)
@require_http_methods(["GET", "POST"])
def resend_verification(request, employee_id):
    """
    HR resends verification token to employee.
    """
    employee = get_object_or_404(Employee, pk=employee_id)
    
    # Find user through Profile using employee_code
    try:
        profile = Profile.objects.get(employee_code=employee.staff_id)
    except Profile.DoesNotExist:
        messages.error(request, 'Employee does not have a user account yet.')
        return redirect('master:employee_list')
    
    # Generate verification token
    try:
        verification_token = profile.generate_verification_token()
        
        # Send verification email (optional)
        # send_verification_email(employee.user, verification_token, None, employee)
        
        # SECURITY: Do not display sensitive verification token in messages
        # Store in session temporarily for secure display
        request.session['resend_verification_token'] = {
            'employee_id': employee.id,
            'verification_token': verification_token,
            'verification_url': request.build_absolute_uri(
                reverse('accounts:verify_employee_account', args=[verification_token])
            ),
        }
        request.session['resend_verification_token_shown'] = False
        
        messages.success(
            request,
            f'Verification token regenerated for {employee.staff_name}. '
            f'Please provide the verification token to the employee securely.'
        )
    except Exception as e:
        # Handle any errors during token generation (e.g., database errors)
        messages.error(request, f'Failed to regenerate verification token: {str(e)}')
    
    return redirect('master:employee_list')

