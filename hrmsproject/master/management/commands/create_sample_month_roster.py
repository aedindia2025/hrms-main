"""
Django management command to create sample month roster data.
Usage: python manage.py create_sample_month_roster
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
from master.models import ShiftRoster, ShiftRosterAssignment, Site, Employee, Shift


class Command(BaseCommand):
    help = 'Create sample month roster data for testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating sample month roster data...'))
        
        # Get or create required objects
        try:
            # Get first site
            site = Site.objects.first()
            if not site:
                self.stdout.write(self.style.ERROR('No Site found. Please create a Site first.'))
                return
            
            # Get first few employees
            employees = Employee.objects.all()[:5]  # Get first 5 employees
            if not employees.exists():
                self.stdout.write(self.style.ERROR('No Employees found. Please create employees first.'))
                return
            
            # Get shifts (optional)
            shifts = Shift.objects.all()[:3]  # Get first 3 shifts if available
            
            # Create sample month roster for current month
            current_date = date.today()
            month_start = date(current_date.year, current_date.month, 1)
            
            # Calculate month end
            if month_start.month == 12:
                month_end = date(month_start.year + 1, 1, 1) - timedelta(days=1)
            else:
                month_end = date(month_start.year, month_start.month + 1, 1) - timedelta(days=1)
            
            # Check if roster already exists
            existing_roster = ShiftRoster.objects.filter(
                site=site,
                roster_type=ShiftRoster.ROSTER_TYPE_MONTH,
                from_date__year=month_start.year,
                from_date__month=month_start.month
            ).first()
            
            if existing_roster:
                self.stdout.write(self.style.WARNING(f'Roster already exists for {month_start.strftime("%B %Y")}. Skipping...'))
                roster = existing_roster
            else:
                # Create new roster
                roster = ShiftRoster.objects.create(
                    site=site,
                    salary_type=ShiftRoster.SALARY_TYPE_SALARY,
                    from_date=month_start,
                    to_date=month_end,
                    roster_type=ShiftRoster.ROSTER_TYPE_MONTH,
                    status=ShiftRoster.STATUS_DRAFT,
                    description=f'Sample month roster for {month_start.strftime("%B %Y")}'
                )
                self.stdout.write(self.style.SUCCESS(f'Created roster: {roster}'))
            
            # Create assignments for each employee
            assignments_created = 0
            shift_names = ['DAY SHIFT', 'NIGHT SHIFT', 'GENERAL SHIFT']
            
            # Loop through each day of the month
            current_day = month_start
            day_counter = 0
            
            while current_day <= month_end:
                # Loop through each employee
                for idx, employee in enumerate(employees):
                    # Skip if assignment already exists
                    existing = ShiftRosterAssignment.objects.filter(
                        roster=roster,
                        employee=employee,
                        date=current_day
                    ).first()
                    
                    if existing:
                        continue
                    
                    # Determine shift based on day pattern
                    # Alternate shifts for variety
                    shift_index = (day_counter + idx) % len(shift_names)
                    shift_name = shift_names[shift_index]
                    
                    # Every 7th day is day off for rotation
                    is_day_off = (day_counter + idx) % 7 == 0
                    
                    # Get shift object if available
                    shift_obj = shifts[idx % len(shifts)] if shifts.exists() else None
                    
                    # Create assignment
                    ShiftRosterAssignment.objects.create(
                        roster=roster,
                        employee=employee,
                        date=current_day,
                        shift=shift_obj,
                        shift_name=shift_name if not is_day_off else '',
                        site=site,
                        is_day_off=is_day_off
                    )
                    assignments_created += 1
                
                # Move to next day
                current_day += timedelta(days=1)
                day_counter += 1
            
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created {assignments_created} assignments for {employees.count()} employees'
            ))
            self.stdout.write(self.style.SUCCESS(
                f'Roster ID: {roster.id} | Month: {month_start.strftime("%B %Y")} | Site: {site.name}'
            ))
            self.stdout.write(self.style.SUCCESS('\n✅ Sample month roster data created successfully!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating sample data: {str(e)}'))
            import traceback
            traceback.print_exc()

