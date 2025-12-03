"""
Django management command to create sample data for all Masters module forms.

Usage:
    python manage.py create_master_sample_data
    python manage.py create_master_sample_data --clear
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta, time
import random

from master.models import (
    Company,
    AdditionDeduction,
    AssetType,
    Department,
    Designation,
    Degree,
    ExpenseType,
    SubExpense,
    Site,
    Plant,
    Holiday,
    LeaveType,
    SalaryType,
    Shift,
    ShiftRoster,
    ShiftRosterAssignment,
    Employee,
    EmployeeAssetAssignment,
)


class Command(BaseCommand):
    help = 'Create sample data for all Masters module forms (Company, Department, Designation, etc.)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing sample data before creating new ones',
        )

    def handle(self, *args, **options):
        clear_existing = options['clear']

        if clear_existing:
            self.stdout.write(self.style.WARNING('Clearing existing sample data...'))
            # Clear in reverse dependency order
            ShiftRosterAssignment.objects.filter(roster__description__icontains='Sample').delete()
            ShiftRoster.objects.filter(description__icontains='Sample').delete()
            EmployeeAssetAssignment.objects.filter(description__icontains='Sample').delete()
            SubExpense.objects.filter(description__icontains='Sample').delete()
            ExpenseType.objects.filter(description__icontains='Sample').delete()
            Plant.objects.filter(name__icontains='Sample').delete()
            Site.objects.filter(name__icontains='Sample').delete()
            Holiday.objects.filter(description__icontains='Sample').delete()
            Designation.objects.filter(description__icontains='Sample').delete()
            Department.objects.filter(description__icontains='Sample').delete()
            Degree.objects.filter(name__icontains='Sample').delete()
            LeaveType.objects.filter(description__icontains='Sample').delete()
            SalaryType.objects.filter(description__icontains='Sample').delete()
            Shift.objects.filter(description__icontains='Sample').delete()
            AssetType.objects.filter(description__icontains='Sample').delete()
            AdditionDeduction.objects.filter(description__icontains='Sample').delete()
            Company.objects.filter(billing_name__icontains='Sample').delete()

        self.stdout.write(self.style.SUCCESS('Creating sample data for all Masters modules...\n'))

        # 1. COMPANY
        self.stdout.write('1. Creating Company data...')
        companies = []
        company_data = [
            {
                'company_group': 'Ascent Group',
                'address': '123 Main Street, Chennai, Tamil Nadu 600001',
                'billing_name': 'Ascent HRMS Solutions Pvt Ltd',
                'billing_address': '123 Main Street, Chennai, Tamil Nadu 600001',
                'mobile_no': '9876543210',
                'phone_no': '0441234567',  # 10 digits without dashes
                'gstin_no': '29ABCDE1234F1Z5',
                'status': Company.STATUS_ACTIVE,
            },
            {
                'company_group': 'Tech Corp Group',
                'address': '456 Tech Park, Bangalore, Karnataka 560001',
                'billing_name': 'Tech Corp Solutions Ltd',
                'billing_address': '456 Tech Park, Bangalore, Karnataka 560001',
                'mobile_no': '9876543220',
                'phone_no': '0801234567',
                'gstin_no': '29FGHIJ5678K2M6',
                'status': Company.STATUS_ACTIVE,
            },
            {
                'company_group': 'Sample Industries',
                'address': '789 Industrial Area, Mumbai, Maharashtra 400001',
                'billing_name': 'Sample Industries Limited',
                'billing_address': '789 Industrial Area, Mumbai, Maharashtra 400001',
                'mobile_no': '9876543230',
                'phone_no': '0221234567',
                'gstin_no': '27PQRST9012U3V7',
                'status': Company.STATUS_INACTIVE,
            },
        ]

        for comp_data in company_data:
            company, created = Company.objects.get_or_create(
                gstin_no=comp_data['gstin_no'],
                defaults=comp_data
            )
            companies.append(company)
            if created:
                self.stdout.write(f'  ✓ Created: {company.billing_name}')
            else:
                self.stdout.write(f'  → Exists: {company.billing_name}')

        # 2. ADDITION/DEDUCTION
        self.stdout.write('\n2. Creating Addition/Deduction data...')
        addition_data = [
            {'type': AdditionDeduction.TYPE_ADDITION, 'name': 'Basic Salary', 'description': 'Sample - Basic salary component'},
            {'type': AdditionDeduction.TYPE_ADDITION, 'name': 'HRA', 'description': 'Sample - House Rent Allowance'},
            {'type': AdditionDeduction.TYPE_ADDITION, 'name': 'Transport Allowance', 'description': 'Sample - Transport allowance'},
            {'type': AdditionDeduction.TYPE_ADDITION, 'name': 'Bonus', 'description': 'Sample - Annual bonus'},
            {'type': AdditionDeduction.TYPE_DEDUCTION, 'name': 'PF Contribution', 'description': 'Sample - Provident Fund'},
            {'type': AdditionDeduction.TYPE_DEDUCTION, 'name': 'ESI Contribution', 'description': 'Sample - ESI deduction'},
            {'type': AdditionDeduction.TYPE_DEDUCTION, 'name': 'Income Tax', 'description': 'Sample - TDS deduction'},
            {'type': AdditionDeduction.TYPE_DEDUCTION, 'name': 'Professional Tax', 'description': 'Sample - Professional tax'},
        ]

        for add_data in addition_data:
            obj, created = AdditionDeduction.objects.get_or_create(
                type=add_data['type'],
                name=add_data['name'],
                defaults={'description': add_data['description']}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.type} - {obj.name}')

        # 3. ASSET TYPE
        self.stdout.write('\n3. Creating Asset Type data...')
        asset_type_data = [
            {'name': 'Laptop', 'description': 'Sample - Laptop computers', 'is_active': True},
            {'name': 'Desktop', 'description': 'Sample - Desktop computers', 'is_active': True},
            {'name': 'Mobile Phone', 'description': 'Sample - Mobile phones', 'is_active': True},
            {'name': 'Tablet', 'description': 'Sample - Tablets', 'is_active': True},
            {'name': 'Vehicle - Two Wheeler', 'description': 'Sample - Two wheeler vehicles', 'is_active': True},
            {'name': 'Vehicle - Four Wheeler', 'description': 'Sample - Four wheeler vehicles', 'is_active': True},
        ]

        for asset_data in asset_type_data:
            obj, created = AssetType.objects.get_or_create(
                name=asset_data['name'],
                defaults={'description': asset_data['description'], 'is_active': asset_data['is_active']}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name}')

        # 4. DEPARTMENT
        self.stdout.write('\n4. Creating Department data...')
        departments = []
        dept_data = [
            {'name': 'IT', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Information Technology'},
            {'name': 'HR', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Human Resources'},
            {'name': 'Finance', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Finance & Accounts'},
            {'name': 'Operations', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Operations'},
            {'name': 'Sales', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Sales & Marketing'},
            {'name': 'Admin', 'status': Department.STATUS_ACTIVE, 'description': 'Sample - Administration'},
        ]

        for dept in dept_data:
            obj, created = Department.objects.get_or_create(
                name=dept['name'],
                defaults={'status': dept['status'], 'description': dept['description']}
            )
            departments.append(obj)
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name}')

        # 5. DESIGNATION
        self.stdout.write('\n5. Creating Designation data...')
        designations = []
        designation_data = [
            {'department': 'IT', 'name': 'Software Engineer', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Software Engineer'},
            {'department': 'IT', 'name': 'Senior Software Engineer', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Senior Software Engineer'},
            {'department': 'IT', 'name': 'Tech Lead', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Tech Lead'},
            {'department': 'HR', 'name': 'HR Executive', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - HR Executive'},
            {'department': 'HR', 'name': 'HR Manager', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - HR Manager'},
            {'department': 'Finance', 'name': 'Accountant', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Accountant'},
            {'department': 'Finance', 'name': 'Finance Manager', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Finance Manager'},
            {'department': 'Operations', 'name': 'Operations Executive', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Operations Executive'},
            {'department': 'Sales', 'name': 'Sales Executive', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Sales Executive'},
            {'department': 'Admin', 'name': 'Admin Executive', 'status': Designation.STATUS_ACTIVE, 'description': 'Sample - Admin Executive'},
        ]

        for desig_data in designation_data:
            dept = next((d for d in departments if d.name == desig_data['department']), None)
            if dept:
                try:
                    obj, created = Designation.objects.get_or_create(
                        department=dept,
                        name=desig_data['name'],
                        defaults={'status': desig_data['status'], 'description': desig_data['description']}
                    )
                    designations.append(obj)
                    if created:
                        self.stdout.write(f'  ✓ Created: {obj.department.name} - {obj.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error creating designation {desig_data["name"]}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠ Department "{desig_data["department"]}" not found, skipping designation "{desig_data["name"]}"'))

        # 6. DEGREE
        self.stdout.write('\n6. Creating Degree data...')
        degree_data = [
            {'education_type': Degree.TYPE_SSLC, 'name': 'SSLC', 'description': 'Sample - SSLC'},
            {'education_type': Degree.TYPE_HSC, 'name': 'HSC', 'description': 'Sample - HSC'},
            {'education_type': Degree.TYPE_UG, 'name': 'B.E. Computer Science', 'description': 'Sample - B.E. Computer Science'},
            {'education_type': Degree.TYPE_UG, 'name': 'B.Com', 'description': 'Sample - B.Com'},
            {'education_type': Degree.TYPE_UG, 'name': 'B.Sc. Mathematics', 'description': 'Sample - B.Sc. Mathematics'},
            {'education_type': Degree.TYPE_PG, 'name': 'M.Tech. Software Engineering', 'description': 'Sample - M.Tech. Software Engineering'},
            {'education_type': Degree.TYPE_PG, 'name': 'MBA', 'description': 'Sample - MBA'},
            {'education_type': Degree.TYPE_TECHNICAL, 'name': 'Diploma in Computer Engineering', 'description': 'Sample - Diploma'},
        ]

        for deg_data in degree_data:
            obj, created = Degree.objects.get_or_create(
                name=deg_data['name'],
                defaults={'education_type': deg_data['education_type']}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.education_type} - {obj.name}')

        # 7. EXPENSE TYPE
        self.stdout.write('\n7. Creating Expense Type data...')
        expense_types = []
        expense_type_data = [
            {'name': 'Travel', 'is_active': True, 'description': 'Sample - Travel expenses'},
            {'name': 'Food', 'is_active': True, 'description': 'Sample - Food expenses'},
            {'name': 'Accommodation', 'is_active': True, 'description': 'Sample - Accommodation expenses'},
            {'name': 'Fuel', 'is_active': True, 'description': 'Sample - Fuel expenses'},
            {'name': 'Office Supplies', 'is_active': True, 'description': 'Sample - Office supplies'},
        ]

        for exp_data in expense_type_data:
            obj, created = ExpenseType.objects.get_or_create(
                name=exp_data['name'],
                defaults={'is_active': exp_data['is_active'], 'description': exp_data['description']}
            )
            expense_types.append(obj)
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name}')

        # 8. SUB EXPENSE
        self.stdout.write('\n8. Creating Sub Expense data...')
        sub_expense_data = [
            {'expense_type': 'Travel', 'name': 'Flight Ticket', 'entry_date': date.today(), 'image_required': False, 'status': SubExpense.STATUS_ACTIVE, 'description': 'Sample - Flight ticket'},
            {'expense_type': 'Travel', 'name': 'Train Ticket', 'entry_date': date.today(), 'image_required': False, 'status': SubExpense.STATUS_ACTIVE, 'description': 'Sample - Train ticket'},
            {'expense_type': 'Food', 'name': 'Lunch', 'entry_date': date.today(), 'image_required': True, 'image_type': SubExpense.IMAGE_TYPE_COMMON, 'status': SubExpense.STATUS_ACTIVE, 'description': 'Sample - Lunch expense'},
            {'expense_type': 'Fuel', 'name': 'Petrol', 'entry_date': date.today(), 'image_required': True, 'image_type': SubExpense.IMAGE_TYPE_METER, 'meter_type': SubExpense.METER_TYPE_START_END, 'status': SubExpense.STATUS_ACTIVE, 'description': 'Sample - Petrol expense'},
        ]

        for sub_exp_data in sub_expense_data:
            exp_type = next((e for e in expense_types if e.name == sub_exp_data['expense_type']), None)
            if exp_type:
                try:
                    obj, created = SubExpense.objects.get_or_create(
                        expense_type=exp_type,
                        name=sub_exp_data['name'],
                        defaults={
                            'entry_date': sub_exp_data['entry_date'],
                            'image_required': sub_exp_data.get('image_required', False),
                            'image_type': sub_exp_data.get('image_type', ''),
                            'meter_type': sub_exp_data.get('meter_type', ''),
                            'status': sub_exp_data['status'],
                            'description': sub_exp_data['description'],
                        }
                    )
                    if created:
                        self.stdout.write(f'  ✓ Created: {obj.expense_type.name} - {obj.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error creating sub expense {sub_exp_data["name"]}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠ Expense type "{sub_exp_data["expense_type"]}" not found, skipping sub expense "{sub_exp_data["name"]}"'))

        # 9. SITE
        self.stdout.write('\n9. Creating Site data...')
        sites = []
        site_data = [
            {'name': 'Chennai Office', 'address': '123 Main Street', 'city': 'Chennai', 'state': 'Tamil Nadu', 'latitude': 13.0827, 'longitude': 80.2707},
            {'name': 'Bangalore Office', 'address': '456 Tech Park', 'city': 'Bangalore', 'state': 'Karnataka', 'latitude': 12.9716, 'longitude': 77.5946},
            {'name': 'Mumbai Office', 'address': '789 Business Park', 'city': 'Mumbai', 'state': 'Maharashtra', 'latitude': 19.0760, 'longitude': 72.8777},
            {'name': 'Sample Site 1', 'address': 'Sample Address 1', 'city': 'Sample City', 'state': 'Sample State'},
            {'name': 'Sample Site 2', 'address': 'Sample Address 2', 'city': 'Sample City', 'state': 'Sample State'},
        ]

        for site in site_data:
            obj, created = Site.objects.get_or_create(
                name=site['name'],
                defaults={
                    'address': site.get('address', ''),
                    'city': site.get('city', ''),
                    'state': site.get('state', ''),
                    'latitude': site.get('latitude'),
                    'longitude': site.get('longitude'),
                }
            )
            sites.append(obj)
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name}')

        # 10. PLANT
        self.stdout.write('\n10. Creating Plant data...')
        plant_data = [
            {'site': 'Chennai Office', 'name': 'Plant A'},
            {'site': 'Chennai Office', 'name': 'Plant B'},
            {'site': 'Bangalore Office', 'name': 'Plant C'},
            {'site': 'Mumbai Office', 'name': 'Plant D'},
        ]

        for plant in plant_data:
            site = next((s for s in sites if s.name == plant['site']), None)
            if site:
                try:
                    obj, created = Plant.objects.get_or_create(
                        site=site,
                        name=plant['name'],
                        defaults={}
                    )
                    if created:
                        self.stdout.write(f'  ✓ Created: {site.name} - {obj.name}')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'  ✗ Error creating plant {plant["name"]}: {str(e)}'))
            else:
                self.stdout.write(self.style.WARNING(f'  ⚠ Site "{plant["site"]}" not found, skipping plant "{plant["name"]}"'))

        # 11. HOLIDAYS
        self.stdout.write('\n11. Creating Holiday data...')
        holiday_data = [
            {'date': date(2025, 1, 26), 'site_name': ['Chennai Office', 'Bangalore Office'], 'holiday_type': 'Public', 'description': 'Sample - Republic Day'},
            {'date': date(2025, 8, 15), 'site_name': ['Chennai Office', 'Bangalore Office', 'Mumbai Office'], 'holiday_type': 'Public', 'description': 'Sample - Independence Day'},
            {'date': date(2025, 10, 2), 'site_name': ['Chennai Office'], 'holiday_type': 'Public', 'description': 'Sample - Gandhi Jayanti'},
        ]

        for hol_data in holiday_data:
            obj, created = Holiday.objects.get_or_create(
                date=hol_data['date'],
                site_name=', '.join(hol_data['site_name']),
                defaults={
                    'holiday_type': hol_data['holiday_type'],
                    'description': hol_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.date} - {obj.site_name}')

        # 12. LEAVE TYPE
        self.stdout.write('\n12. Creating Leave Type data...')
        leave_type_data = [
            {'leave_type': 'Casual Leave', 'short_name': 'CL', 'description': 'Sample - Casual Leave'},
            {'leave_type': 'Sick Leave', 'short_name': 'SL', 'description': 'Sample - Sick Leave'},
            {'leave_type': 'Earned Leave', 'short_name': 'EL', 'description': 'Sample - Earned Leave'},
            {'leave_type': 'Compensatory Off', 'short_name': 'CO', 'description': 'Sample - Compensatory Off'},
            {'leave_type': 'Leave Without Pay', 'short_name': 'LWP', 'description': 'Sample - Leave Without Pay'},
        ]

        for leave_data in leave_type_data:
            obj, created = LeaveType.objects.get_or_create(
                leave_type=leave_data['leave_type'],
                defaults={
                    'short_name': leave_data['short_name'],
                    'description': leave_data['description'],
                }
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.leave_type} ({obj.short_name})')

        # 13. SALARY TYPE
        self.stdout.write('\n13. Creating Salary Type data...')
        salary_type_data = [
            {'name': 'Monthly Salary', 'is_active': True, 'description': 'Sample - Monthly salary'},
            {'name': 'Daily Wages', 'is_active': True, 'description': 'Sample - Daily wages'},
            {'name': 'Contract Based', 'is_active': True, 'description': 'Sample - Contract based'},
        ]

        for sal_data in salary_type_data:
            obj, created = SalaryType.objects.get_or_create(
                name=sal_data['name'],
                defaults={'is_active': sal_data['is_active'], 'description': sal_data['description']}
            )
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name}')

        # 14. SHIFT
        self.stdout.write('\n14. Creating Shift data...')
        shifts = []
        shift_data = [
            {'name': 'Day Shift', 'start_time': time(9, 0), 'end_time': time(18, 0), 'description': 'Sample - Day Shift (9 AM to 6 PM)'},
            {'name': 'Night Shift', 'start_time': time(21, 0), 'end_time': time(6, 0), 'description': 'Sample - Night Shift (9 PM to 6 AM)'},
            {'name': 'Morning Shift', 'start_time': time(6, 0), 'end_time': time(14, 0), 'description': 'Sample - Morning Shift (6 AM to 2 PM)'},
            {'name': 'Evening Shift', 'start_time': time(14, 0), 'end_time': time(22, 0), 'description': 'Sample - Evening Shift (2 PM to 10 PM)'},
        ]

        for shift in shift_data:
            obj, created = Shift.objects.get_or_create(
                name=shift['name'],
                defaults={
                    'start_time': shift['start_time'],
                    'end_time': shift['end_time'],
                    'description': shift['description'],
                }
            )
            shifts.append(obj)
            if created:
                self.stdout.write(f'  ✓ Created: {obj.name} ({obj.start_time} - {obj.end_time})')

        # 15. SHIFT ROSTER (Week Wise)
        self.stdout.write('\n15. Creating Shift Roster data...')
        if sites and len(sites) > 0:
            roster_site = sites[0]
            from_date = date.today() - timedelta(days=date.today().weekday())  # Start of current week
            
            try:
                roster, created = ShiftRoster.objects.get_or_create(
                    site=roster_site,
                    from_date=from_date,
                    roster_type=ShiftRoster.ROSTER_TYPE_WEEK,
                    defaults={
                        'salary_type': ShiftRoster.SALARY_TYPE_SALARY,
                        'to_date': from_date + timedelta(days=6),
                        'status': ShiftRoster.STATUS_DRAFT,
                        'description': 'Sample - Week wise roster for testing',
                    }
                )
                if created:
                    self.stdout.write(f'  ✓ Created: Week Roster for {roster_site.name} ({from_date})')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Error creating shift roster: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('  ⚠ No sites available, skipping shift roster creation'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('✓ Sample data creation completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nCreated/Verified:')
        self.stdout.write(f'  - Companies: {Company.objects.count()}')
        self.stdout.write(f'  - Additions/Deductions: {AdditionDeduction.objects.count()}')
        self.stdout.write(f'  - Asset Types: {AssetType.objects.count()}')
        self.stdout.write(f'  - Departments: {Department.objects.count()}')
        self.stdout.write(f'  - Designations: {Designation.objects.count()}')
        self.stdout.write(f'  - Degrees: {Degree.objects.count()}')
        self.stdout.write(f'  - Expense Types: {ExpenseType.objects.count()}')
        self.stdout.write(f'  - Sub Expenses: {SubExpense.objects.count()}')
        self.stdout.write(f'  - Sites: {Site.objects.count()}')
        self.stdout.write(f'  - Plants: {Plant.objects.count()}')
        self.stdout.write(f'  - Holidays: {Holiday.objects.count()}')
        self.stdout.write(f'  - Leave Types: {LeaveType.objects.count()}')
        self.stdout.write(f'  - Salary Types: {SalaryType.objects.count()}')
        self.stdout.write(f'  - Shifts: {Shift.objects.count()}')
        self.stdout.write(f'  - Shift Rosters: {ShiftRoster.objects.count()}')
        self.stdout.write('\n' + '='*60)

