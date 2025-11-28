"""
Django management command to create sample employee data with all 6 tabs filled.

Usage:
    python manage.py create_sample_employees
    python manage.py create_sample_employees --count 5
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date, timedelta
import uuid

from master.models import (
    Company,
    Employee,
    EmployeeDependent,
    EmployeeAccountInfo,
    EmployeeQualification,
    EmployeeExperience,
    EmployeeAssetAssignment,
    EmployeeVehicleDetail,
)


class Command(BaseCommand):
    help = 'Create sample employee data with all 6 tabs (Staff, Dependent, Account, Qualification, Experience, Asset)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=3,
            help='Number of sample employees to create (default: 3)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing sample employees before creating new ones',
        )

    def handle(self, *args, **options):
        count = options['count']
        clear_existing = options['clear']

        # Get or create a company
        company, created = Company.objects.get_or_create(
            gstin_no='29ABCDE1234F1Z5',
            defaults={
                'company_group': 'Ascent Group',
                'address': '123 Main Street, Chennai, Tamil Nadu',
                'billing_name': 'Ascent HRMS Solutions',
                'billing_address': '123 Main Street, Chennai, Tamil Nadu',
                'mobile_no': '9876543210',
                'phone_no': '044-12345678',
                'status': Company.STATUS_ACTIVE,
            }
        )

        if clear_existing:
            self.stdout.write(self.style.WARNING('Clearing existing sample employees...'))
            Employee.objects.filter(staff_id__startswith='EMP').delete()

        self.stdout.write(self.style.SUCCESS(f'Creating {count} sample employees...'))

        # Sample data templates
        sample_employees = [
            {
                'staff_name': 'Rajesh Kumar',
                'staff_id': 'EMP001',
                'gender': Employee.GENDER_MALE,
                'father_name': 'Ramesh Kumar',
                'date_of_birth': date(1990, 5, 15),
                'document_date_of_birth': date(1990, 5, 15),
                'age': 34,
                'marital_status': Employee.MARITAL_MARRIED,
                'personal_contact': '9876543210',
                'office_contact': '9876543211',
                'personal_email': 'rajesh.kumar@example.com',
                'office_email': 'rajesh.kumar@ascent.com',
                'aadhar_no': '123456789012',
                'pan_no': 'ABCDE1234F',
                'medical_claim': True,
                'blood_group': 'O+',
                'qualification': 'B.E. Computer Science',
                'present_country': 'India',
                'present_state': 'Tamil Nadu',
                'present_city': 'Chennai',
                'present_building': 'A-101',
                'present_street': 'MG Road',
                'present_area': 'T Nagar',
                'present_pincode': '600017',
                'permanent_country': 'India',
                'permanent_state': 'Tamil Nadu',
                'permanent_city': 'Chennai',
                'permanent_building': 'A-101',
                'permanent_street': 'MG Road',
                'permanent_area': 'T Nagar',
                'permanent_pincode': '600017',
                'date_of_join': date(2020, 1, 15),
                'designation': 'Software Engineer',
                'department': 'IT',
                'work_location': 'Chennai',
                'esi_no': 'ESI123456',
                'pf_no': 'PF123456',
                'biometric_id': 'BIO001',
                'salary_category': Employee.SALARY_CATEGORY_MONTHLY,
                'premises_type': Employee.PREMISES_OUT,
                'branch': 'Branch 1',
                'attendance_setting': 'Default',
                'reporting_officer': 'RO1',
            },
            {
                'staff_name': 'Priya Sharma',
                'staff_id': 'EMP002',
                'gender': Employee.GENDER_FEMALE,
                'father_name': 'Suresh Sharma',
                'date_of_birth': date(1992, 8, 20),
                'document_date_of_birth': date(1992, 8, 20),
                'age': 32,
                'marital_status': Employee.MARITAL_SINGLE,
                'personal_contact': '9876543220',
                'office_contact': '9876543221',
                'personal_email': 'priya.sharma@example.com',
                'office_email': 'priya.sharma@ascent.com',
                'aadhar_no': '234567890123',
                'pan_no': 'BCDEF2345G',
                'medical_claim': True,
                'blood_group': 'A+',
                'qualification': 'M.Sc. Mathematics',
                'present_country': 'India',
                'present_state': 'Tamil Nadu',
                'present_city': 'Coimbatore',
                'present_building': 'B-202',
                'present_street': 'Gandhi Road',
                'present_area': 'RS Puram',
                'present_pincode': '641002',
                'permanent_country': 'India',
                'permanent_state': 'Tamil Nadu',
                'permanent_city': 'Coimbatore',
                'permanent_building': 'B-202',
                'permanent_street': 'Gandhi Road',
                'permanent_area': 'RS Puram',
                'permanent_pincode': '641002',
                'date_of_join': date(2021, 3, 10),
                'designation': 'Data Analyst',
                'department': 'Analytics',
                'work_location': 'Coimbatore',
                'esi_no': 'ESI234567',
                'pf_no': 'PF234567',
                'biometric_id': 'BIO002',
                'salary_category': Employee.SALARY_CATEGORY_MONTHLY,
                'premises_type': Employee.PREMISES_IN,
                'branch': 'Branch 2',
                'attendance_setting': 'Night Shift',
                'reporting_officer': 'RO2',
            },
            {
                'staff_name': 'Arjun Menon',
                'staff_id': 'EMP003',
                'gender': Employee.GENDER_MALE,
                'father_name': 'Krishnan Menon',
                'date_of_birth': date(1988, 12, 5),
                'document_date_of_birth': date(1988, 12, 5),
                'age': 36,
                'marital_status': Employee.MARITAL_MARRIED,
                'personal_contact': '9876543230',
                'office_contact': '9876543231',
                'personal_email': 'arjun.menon@example.com',
                'office_email': 'arjun.menon@ascent.com',
                'aadhar_no': '345678901234',
                'pan_no': 'CDEFG3456H',
                'medical_claim': False,
                'blood_group': 'B+',
                'qualification': 'MBA Finance',
                'present_country': 'India',
                'present_state': 'Kerala',
                'present_city': 'Kochi',
                'present_building': 'C-303',
                'present_street': 'Marine Drive',
                'present_area': 'Fort Kochi',
                'present_pincode': '682001',
                'permanent_country': 'India',
                'permanent_state': 'Kerala',
                'permanent_city': 'Thrissur',
                'permanent_building': 'D-404',
                'permanent_street': 'Round North',
                'permanent_area': 'Thrissur City',
                'permanent_pincode': '680001',
                'date_of_join': date(2019, 6, 1),
                'designation': 'Project Manager',
                'department': 'Operations',
                'work_location': 'Kochi',
                'esi_no': 'ESI345678',
                'pf_no': 'PF345678',
                'biometric_id': 'BIO003',
                'salary_category': Employee.SALARY_CATEGORY_MONTHLY,
                'premises_type': Employee.PREMISES_OUT,
                'branch': 'Branch 3',
                'attendance_setting': 'Default',
                'reporting_officer': 'RO1',
            },
        ]

        for i in range(count):
            # Use sample data or generate new
            if i < len(sample_employees):
                emp_data = sample_employees[i].copy()
                emp_data['staff_id'] = f'EMP{i+1:03d}'
            else:
                # Generate new employee data
                emp_data = {
                    'staff_name': f'Employee {i+1}',
                    'staff_id': f'EMP{i+1:03d}',
                    'gender': Employee.GENDER_MALE if i % 2 == 0 else Employee.GENDER_FEMALE,
                    'father_name': f'Father {i+1}',
                    'date_of_birth': date(1990 + (i % 10), 1 + (i % 12), 1 + (i % 28)),
                    'document_date_of_birth': date(1990 + (i % 10), 1 + (i % 12), 1 + (i % 28)),
                    'age': 25 + (i % 20),
                    'marital_status': Employee.MARITAL_MARRIED if i % 2 == 0 else Employee.MARITAL_SINGLE,
                    'personal_contact': f'9876543{i:03d}',
                    'office_contact': f'9876543{i+1:03d}',
                    'personal_email': f'employee{i+1}@example.com',
                    'office_email': f'employee{i+1}@ascent.com',
                    'aadhar_no': f'{123456789012 + i:012d}',
                    'pan_no': f'ABCDE{i+1:04d}F',
                    'medical_claim': i % 2 == 0,
                    'blood_group': ['A+', 'B+', 'O+', 'AB+'][i % 4],
                    'qualification': 'B.E. Computer Science',
                    'present_country': 'India',
                    'present_state': 'Tamil Nadu',
                    'present_city': 'Chennai',
                    'present_building': f'Building {i+1}',
                    'present_street': f'Street {i+1}',
                    'present_area': f'Area {i+1}',
                    'present_pincode': f'{600000 + i:06d}',
                    'permanent_country': 'India',
                    'permanent_state': 'Tamil Nadu',
                    'permanent_city': 'Chennai',
                    'permanent_building': f'Building {i+1}',
                    'permanent_street': f'Street {i+1}',
                    'permanent_area': f'Area {i+1}',
                    'permanent_pincode': f'{600000 + i:06d}',
                    'date_of_join': date(2020, 1, 1) + timedelta(days=i*30),
                    'designation': ['Software Engineer', 'Data Analyst', 'Project Manager'][i % 3],
                    'department': ['IT', 'Analytics', 'Operations'][i % 3],
                    'work_location': 'Chennai',
                    'esi_no': f'ESI{i+1:06d}',
                    'pf_no': f'PF{i+1:06d}',
                    'biometric_id': f'BIO{i+1:03d}',
                    'salary_category': Employee.SALARY_CATEGORY_MONTHLY,
                    'premises_type': Employee.PREMISES_OUT if i % 2 == 0 else Employee.PREMISES_IN,
                    'branch': f'Branch {(i % 5) + 1}',
                    'attendance_setting': 'Default',
                    'reporting_officer': f'RO{(i % 2) + 1}',
                }

            # Create Employee (Tab 1: Staff Details)
            unique_id = str(uuid.uuid4())
            employee, created = Employee.objects.update_or_create(
                unique_id=unique_id,
                defaults={
                    **emp_data,
                    'company': company,
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created employee: {employee.staff_name} ({employee.staff_id})'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Updated employee: {employee.staff_name} ({employee.staff_id})'))

            # Tab 2: Dependent Details (Multiple dependents)
            dependents_data = [
                {
                    'relationship': 'Spouse',
                    'name': f'{employee.staff_name.split()[0]} Spouse',
                    'gender': 'Female' if employee.gender == 'Male' else 'Male',
                    'date_of_birth': date(1992, 6, 15),
                    'aadhar_no': f'{123456789013 + i:012d}',
                    'occupation': 'Housewife',
                    'standard': 'N/A',
                    'school': 'N/A',
                    'existing_illness': 'No',
                    'description': 'Healthy',
                    'existing_insurance': 'Yes',
                    'insurance_no': f'INS{i+1:06d}',
                    'physically_challenged': 'No',
                    'remarks': 'No remarks',
                },
                {
                    'relationship': 'Child',
                    'name': f'{employee.staff_name.split()[0]} Child',
                    'gender': 'Male',
                    'date_of_birth': date(2015, 3, 10),
                    'aadhar_no': f'{123456789014 + i:012d}',
                    'occupation': 'Student',
                    'standard': '5th',
                    'school': 'ABC School',
                    'existing_illness': 'No',
                    'description': 'Healthy',
                    'existing_insurance': 'Yes',
                    'insurance_no': f'INS{i+2:06d}',
                    'physically_challenged': 'No',
                    'remarks': 'No remarks',
                },
            ]

            # Delete existing dependents
            EmployeeDependent.objects.filter(employee=employee).delete()
            for dep_data in dependents_data:
                EmployeeDependent.objects.create(employee=employee, **dep_data)
            self.stdout.write(f'  → Created {len(dependents_data)} dependents')

            # Tab 3: Account Details
            account_data = {
                'bank_status': EmployeeAccountInfo.BANK_STATUS_ACTIVE,
                'salary_type': EmployeeAccountInfo.SALARY_TYPE_AXIS,
                'accountant_name': employee.staff_name,
                'account_no': f'{1234567890123456 + i:016d}',
                'bank_name': 'Axis Bank',
                'ifsc_code': 'UTIB0001234',
                'contact_no': employee.personal_contact,
                'bank_address': '123 Bank Street, Chennai, Tamil Nadu',
            }
            EmployeeAccountInfo.objects.update_or_create(
                employee=employee,
                defaults=account_data
            )
            self.stdout.write(f'  → Created account details')

            # Tab 4: Qualification Details (Multiple qualifications)
            qualifications_data = [
                {
                    'education_type': 'UG',
                    'degree': 'B.E. Computer Science',
                    'college_name': 'Anna University',
                    'year_of_passing': '2012',
                    'percentage': '85.5',
                    'university': 'Anna University',
                },
                {
                    'education_type': 'PG',
                    'degree': 'M.Tech. Software Engineering',
                    'college_name': 'IIT Madras',
                    'year_of_passing': '2014',
                    'percentage': '88.0',
                    'university': 'IIT Madras',
                },
            ]

            # Delete existing qualifications
            EmployeeQualification.objects.filter(employee=employee).delete()
            for qual_data in qualifications_data:
                EmployeeQualification.objects.create(employee=employee, **qual_data)
            self.stdout.write(f'  → Created {len(qualifications_data)} qualifications')

            # Tab 5: Experience Details (Multiple experiences)
            experiences_data = [
                {
                    'company_name': 'Tech Solutions Pvt Ltd',
                    'designation': 'Junior Software Engineer',
                    'salary': '30000',
                    'joining_month': '2014-07',
                    'relieving_month': '2017-06',
                    'experience_years': '3',
                },
                {
                    'company_name': 'Digital Innovations Inc',
                    'designation': 'Senior Software Engineer',
                    'salary': '50000',
                    'joining_month': '2017-07',
                    'relieving_month': '2020-01',
                    'experience_years': '2.5',
                },
            ]

            # Delete existing experiences
            EmployeeExperience.objects.filter(employee=employee).delete()
            for exp_data in experiences_data:
                EmployeeExperience.objects.create(employee=employee, **exp_data)
            self.stdout.write(f'  → Created {len(experiences_data)} experiences')

            # Tab 6: Asset/Vehicle Details (Multiple assets)
            assets_data = [
                {
                    'asset_name': 'Laptop',
                    'serial_no': f'LAP{i+1:03d}',
                    'quantity': 1,
                    'status': EmployeeAssetAssignment.STATUS_ISSUED,
                    'vehicle_reg_no': '',
                    'license_mode': '',
                    'license_no': '',
                    'license_valid_from': None,
                    'license_valid_to': None,
                },
                {
                    'asset_name': 'Mobile Phone',
                    'serial_no': f'MOB{i+1:03d}',
                    'quantity': 1,
                    'status': EmployeeAssetAssignment.STATUS_ISSUED,
                    'vehicle_reg_no': f'TN{i+1:02d}AB{i+1:04d}',
                    'license_mode': EmployeeAssetAssignment.LICENSE_MODE_TWO,
                    'license_no': f'DL{i+1:06d}',
                    'license_valid_from': date(2020, 1, 1),
                    'license_valid_to': date(2030, 1, 1),
                },
            ]

            # Delete existing assets
            EmployeeAssetAssignment.objects.filter(employee=employee).delete()
            for asset_data in assets_data:
                EmployeeAssetAssignment.objects.create(employee=employee, **asset_data)
            self.stdout.write(f'  → Created {len(assets_data)} assets')

            # Vehicle Details (OneToOne)
            vehicle_data = {
                'vehicle_type': 'Motorcycle',
                'vehicle_company': 'Honda',
                'vehicle_owner': employee.staff_name,
                'registration_year': date(2020, 1, 1),
                'rc_no': f'RC{i+1:06d}',
                'rc_validity_from': date(2020, 1, 1),
                'rc_validity_to': date(2030, 1, 1),
                'insurance_no': f'INSV{i+1:06d}',
                'insurance_validity_from': date(2020, 1, 1),
                'insurance_validity_to': date(2025, 1, 1),
            }
            EmployeeVehicleDetail.objects.update_or_create(
                employee=employee,
                defaults=vehicle_data
            )
            self.stdout.write(f'  → Created vehicle details')

        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully created {count} sample employees with all 6 tabs data!'))
        self.stdout.write(self.style.SUCCESS(f'  - Staff Details: ✓'))
        self.stdout.write(self.style.SUCCESS(f'  - Dependent Details: ✓ (2 dependents per employee)'))
        self.stdout.write(self.style.SUCCESS(f'  - Account Details: ✓'))
        self.stdout.write(self.style.SUCCESS(f'  - Qualification Details: ✓ (2 qualifications per employee)'))
        self.stdout.write(self.style.SUCCESS(f'  - Experience Details: ✓ (2 experiences per employee)'))
        self.stdout.write(self.style.SUCCESS(f'  - Asset/Vehicle Details: ✓ (2 assets per employee)'))

