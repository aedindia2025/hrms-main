"""
Context processor to make user profile image available in all templates.
"""
from django.db.models import Q


def user_profile_image(request):
    """Add user's employee profile image to context."""
    profile_image = None
    employee = None
    
    if request.user.is_authenticated:
        try:
            from master.models import Employee
            
            # Try to find employee linked to user
            employee = Employee.objects.filter(
                Q(personal_email=request.user.email) | 
                Q(office_email=request.user.email) |
                Q(staff_id=request.user.username)
            ).first()
            
            # Also check if user has a profile with employee_code
            if not employee:
                try:
                    profile = request.user.profile
                    if profile.employee_code:
                        employee = Employee.objects.filter(staff_id=profile.employee_code).first()
                except:
                    pass
            
            # Get profile image if employee exists
            if employee and employee.profile_image:
                profile_image = employee.profile_image.url
        except:
            pass
    
    return {
        'user_employee': employee,
        'user_profile_image': profile_image,
    }

