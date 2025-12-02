from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Company(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    company_group = models.CharField(max_length=150)
    address = models.TextField()
    billing_name = models.CharField(max_length=150)
    billing_address = models.TextField()
    mobile_no = models.CharField(max_length=20)
    phone_no = models.CharField(max_length=20, blank=True)
    gstin_no = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['company_group', 'billing_name']

    def __str__(self) -> str:
        return self.billing_name or self.company_group


class Shift(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class SalaryType(models.Model):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class AssetType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class ExpenseType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to='expense_type/documents/', blank=True, null=True, help_text='Upload document related to this expense type')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Holiday(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateField()
    site_name = models.CharField(max_length=255)
    holiday_type = models.CharField(max_length=120, blank=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'site_name']

    def __str__(self) -> str:
        return f'{self.site_name} - {self.date}'



class Department(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return self.name


class Designation(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='designations')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department__name', 'name']
        unique_together = [('department', 'name')]

    def __str__(self) -> str:
        return self.name


class Degree(models.Model):
    TYPE_UG = 'UG'
    TYPE_PG = 'PG'
    TYPE_TECHNICAL = 'TECH'
    TYPE_HSC = 'HSC'
    TYPE_SSLC = 'SSLC'
    EDUCATION_TYPE_CHOICES = [
        (TYPE_UG, 'UG'),
        (TYPE_PG, 'PG'),
        (TYPE_TECHNICAL, 'Technical Education'),
        (TYPE_HSC, 'HSC'),
        (TYPE_SSLC, 'SSLC'),
    ]

    education_type = models.CharField(max_length=10, choices=EDUCATION_TYPE_CHOICES, default=TYPE_UG)
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['education_type', 'name']

    def __str__(self) -> str:
        return self.name


class LeaveType(models.Model):
    leave_type = models.CharField(max_length=150, unique=True)
    short_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['leave_type']
        verbose_name = 'Leave Type'
        verbose_name_plural = 'Leave Types'

    def __str__(self) -> str:
        return self.leave_type


class AdditionDeduction(models.Model):
    TYPE_ADDITION = 'Addition'
    TYPE_DEDUCTION = 'Deduction'
    TYPE_CHOICES = [
        (TYPE_ADDITION, 'Addition'),
        (TYPE_DEDUCTION, 'Deduction'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['type', 'name']
        unique_together = [('type', 'name')]
        verbose_name = 'Addition and Deduction'
        verbose_name_plural = 'Additions and Deductions'

    def __str__(self) -> str:
        return f'{self.type} - {self.name}'


class SubExpense(models.Model):
    STATUS_ACTIVE = 'Active'
    STATUS_INACTIVE = 'Inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    IMAGE_TYPE_COMMON = 'Common Image'
    IMAGE_TYPE_METER = 'Start and End Meter Image'
    IMAGE_TYPE_CHOICES = [
        (IMAGE_TYPE_COMMON, 'Common Image'),
        (IMAGE_TYPE_METER, 'Start and End Meter Image'),
    ]

    METER_TYPE_START_END = 'Start and End Meter'
    METER_TYPE_TOTAL_KM = 'Total Kilometer'
    METER_TYPE_CHOICES = [
        (METER_TYPE_START_END, 'Start and End Meter'),
        (METER_TYPE_TOTAL_KM, 'Total Kilometer'),
    ]

    entry_date = models.DateField()
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE, related_name='sub_expenses')
    name = models.CharField(max_length=150)
    image_required = models.BooleanField(default=False)
    image_type = models.CharField(max_length=50, choices=IMAGE_TYPE_CHOICES, blank=True)
    meter_type = models.CharField(max_length=50, choices=METER_TYPE_CHOICES, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-entry_date', 'expense_type__name', 'name']
        unique_together = [('expense_type', 'name')]
        verbose_name = 'Sub Expense'
        verbose_name_plural = 'Sub Expenses'

    def __str__(self) -> str:
        return f'{self.expense_type.name} - {self.name}'


class Site(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'

    def __str__(self) -> str:
        return self.name


class Plant(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['site__name', 'name']
        unique_together = [('site', 'name')]
        verbose_name = 'Plant'
        verbose_name_plural = 'Plants'

    def __str__(self) -> str:
        return f'{self.site.name} - {self.name}'


class Employee(models.Model):
    GENDER_MALE = 'Male'
    GENDER_FEMALE = 'Female'
    GENDER_OTHERS = 'Others'
    GENDER_CHOICES = [
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHERS, 'Others'),
    ]

    MARITAL_MARRIED = 'Married'
    MARITAL_SINGLE = 'Unmarried'
    MARITAL_CHOICES = [
        (MARITAL_MARRIED, 'Married'),
        (MARITAL_SINGLE, 'Unmarried'),
    ]

    PREMISES_IN = 'IN'
    PREMISES_OUT = 'OUT'
    PREMISES_CHOICES = [
        (PREMISES_OUT, 'Out Premises'),
        (PREMISES_IN, 'In Premises'),
    ]

    SALARY_CATEGORY_MONTHLY = 'Monthly'
    SALARY_CATEGORY_WAGES = 'Wages'
    SALARY_CATEGORY_CONTRACT = 'Contract'
    SALARY_CATEGORY_CHOICES = [
        (SALARY_CATEGORY_MONTHLY, 'Monthly'),
        (SALARY_CATEGORY_WAGES, 'Wages'),
        (SALARY_CATEGORY_CONTRACT, 'Contract'),
    ]

    id = models.BigAutoField(primary_key=True)
    unique_id = models.CharField(max_length=64, blank=True)
    staff_name = models.CharField(max_length=255)
    staff_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    father_name = models.CharField(max_length=255, blank=True)
    date_of_birth = models.DateField()
    document_date_of_birth = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(70)],
        null=True,
        blank=True,
    )
    marital_status = models.CharField(max_length=12, choices=MARITAL_CHOICES, blank=True)
    personal_contact = models.CharField(max_length=15, blank=True)
    office_contact = models.CharField(max_length=15, blank=True)
    personal_email = models.EmailField(blank=True)
    office_email = models.EmailField(blank=True)
    aadhar_no = models.CharField(max_length=14, blank=True)
    pan_no = models.CharField(max_length=10, blank=True)
    medical_claim = models.BooleanField(default=False)
    blood_group = models.CharField(max_length=4, blank=True)
    qualification = models.CharField(max_length=255, blank=True)

    present_country = models.CharField(max_length=120, blank=True)
    present_state = models.CharField(max_length=120, blank=True)
    present_city = models.CharField(max_length=120, blank=True)
    present_building = models.CharField(max_length=120, blank=True)
    present_street = models.CharField(max_length=120, blank=True)
    present_area = models.CharField(max_length=120, blank=True)
    present_pincode = models.CharField(max_length=10, blank=True)

    permanent_country = models.CharField(max_length=120, blank=True)
    permanent_state = models.CharField(max_length=120, blank=True)
    permanent_city = models.CharField(max_length=120, blank=True)
    permanent_building = models.CharField(max_length=120, blank=True)
    permanent_street = models.CharField(max_length=120, blank=True)
    permanent_area = models.CharField(max_length=120, blank=True)
    permanent_pincode = models.CharField(max_length=10, blank=True)

    date_of_join = models.DateField()
    designation = models.CharField(max_length=120)
    department = models.CharField(max_length=120)
    work_location = models.CharField(max_length=120)
    esi_no = models.CharField(max_length=50, blank=True)
    pf_no = models.CharField(max_length=50, blank=True)
    biometric_id = models.CharField(max_length=50, blank=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='employees')
    salary_category = models.CharField(max_length=20, choices=SALARY_CATEGORY_CHOICES, blank=True)
    profile_image = models.ImageField(upload_to='employee/profile/', blank=True, null=True)
    premises_type = models.CharField(max_length=3, choices=PREMISES_CHOICES, default=PREMISES_OUT)
    branch = models.CharField(max_length=150, blank=True)
    attendance_setting = models.CharField(max_length=120, blank=True)
    reporting_officer = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['staff_name']

    def __str__(self) -> str:
        return f'{self.staff_name} ({self.staff_id})'


class EmployeeDependent(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='dependents')
    relationship = models.CharField(max_length=120)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    aadhar_no = models.CharField(max_length=12, blank=True)
    occupation = models.CharField(max_length=255, blank=True)
    standard = models.CharField(max_length=120, blank=True)
    school = models.CharField(max_length=255, blank=True)
    existing_illness = models.CharField(max_length=3, blank=True)
    description = models.CharField(max_length=255, blank=True)
    existing_insurance = models.CharField(max_length=3, blank=True)
    insurance_no = models.CharField(max_length=120, blank=True)
    physically_challenged = models.CharField(max_length=3, blank=True)
    remarks = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['employee', 'name']

    def __str__(self) -> str:
        return f'{self.name} - {self.relationship}'


class EmployeeAccountInfo(models.Model):
    BANK_STATUS_ACTIVE = 'Active'
    BANK_STATUS_INACTIVE = 'Inactive'
    BANK_STATUS_CHOICES = [
        (BANK_STATUS_ACTIVE, 'Active'),
        (BANK_STATUS_INACTIVE, 'Inactive'),
    ]

    SALARY_TYPE_AXIS = 'Axis Bank'
    SALARY_TYPE_NEFT = 'NEFT'
    SALARY_TYPE_CHEQUE = 'Cheque'
    SALARY_TYPE_CASH = 'Cash'
    SALARY_TYPE_HOLD = 'Hold'
    SALARY_TYPE_CHOICES = [
        (SALARY_TYPE_AXIS, 'Axis Bank'),
        (SALARY_TYPE_NEFT, 'NEFT'),
        (SALARY_TYPE_CHEQUE, 'Cheque'),
        (SALARY_TYPE_CASH, 'Cash'),
        (SALARY_TYPE_HOLD, 'Hold'),
    ]

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='account_info')
    bank_status = models.CharField(max_length=10, choices=BANK_STATUS_CHOICES, default=BANK_STATUS_ACTIVE)
    salary_type = models.CharField(max_length=20, choices=SALARY_TYPE_CHOICES, blank=True)
    accountant_name = models.CharField(max_length=255, blank=True)
    account_no = models.CharField(max_length=34, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    contact_no = models.CharField(max_length=15, blank=True)
    bank_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.employee.staff_name} - {self.bank_name}'


class EmployeeQualification(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='qualifications')
    education_type = models.CharField(max_length=50, blank=True)
    degree = models.CharField(max_length=120, blank=True)
    college_name = models.CharField(max_length=255, blank=True)
    year_of_passing = models.CharField(max_length=7, blank=True)
    percentage = models.CharField(max_length=10, blank=True)
    university = models.CharField(max_length=255, blank=True)
    documents = models.FileField(upload_to='employee/qualifications/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['employee', 'year_of_passing']

    def __str__(self) -> str:
        return f'{self.employee.staff_name} - {self.degree}'


class EmployeeExperience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255, blank=True)
    designation = models.CharField(max_length=255, blank=True)
    salary = models.CharField(max_length=50, blank=True)
    joining_month = models.CharField(max_length=7, blank=True)
    relieving_month = models.CharField(max_length=7, blank=True)
    experience_years = models.CharField(max_length=10, blank=True)
    documents = models.FileField(upload_to='employee/experience/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['employee', '-joining_month']

    def __str__(self) -> str:
        return f'{self.employee.staff_name} - {self.company_name}'


class EmployeeAssetAssignment(models.Model):
    STATUS_ISSUED = 'Issued'
    STATUS_RETURNED = 'Returned'
    STATUS_IN_REPAIR = 'In Repair'
    STATUS_CHOICES = [
        (STATUS_ISSUED, 'Issued'),
        (STATUS_RETURNED, 'Returned'),
        (STATUS_IN_REPAIR, 'In Repair'),
    ]

    LICENSE_MODE_TWO = 'Two Wheeler'
    LICENSE_MODE_FOUR = 'Four Wheeler'
    LICENSE_MODE_HEAVY = 'Heavy Vehicle'
    LICENSE_MODE_CHOICES = [
        (LICENSE_MODE_TWO, 'Two Wheeler'),
        (LICENSE_MODE_FOUR, 'Four Wheeler'),
        (LICENSE_MODE_HEAVY, 'Heavy Vehicle'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='asset_assignments')
    asset_type = models.ForeignKey(AssetType, on_delete=models.PROTECT, related_name='assignments', null=True, blank=True)
    asset_name = models.CharField(max_length=255, blank=True, help_text='Legacy field - use asset_type instead')
    serial_no = models.CharField(max_length=255, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ISSUED)
    description = models.TextField(blank=True, help_text='Additional notes or description')
    # Vehicle-specific fields (optional - only for vehicle assets)
    vehicle_reg_no = models.CharField(max_length=120, blank=True)
    license_mode = models.CharField(max_length=20, choices=LICENSE_MODE_CHOICES, blank=True)
    license_no = models.CharField(max_length=120, blank=True)
    license_valid_from = models.DateField(null=True, blank=True)
    license_valid_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee', '-created_at']
        verbose_name = 'Employee Asset Assignment'
        verbose_name_plural = 'Employee Asset Assignments'

    def __str__(self) -> str:
        asset_display = self.asset_type.name if self.asset_type else self.asset_name
        return f'{self.employee.staff_name} - {asset_display}'
    
    @property
    def asset_name_display(self):
        """Return asset name from asset_type if available, otherwise use asset_name field."""
        return self.asset_type.name if self.asset_type else self.asset_name


class EmployeeVehicleDetail(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='vehicle_detail')
    vehicle_type = models.CharField(max_length=120, blank=True)
    vehicle_company = models.CharField(max_length=120, blank=True)
    vehicle_owner = models.CharField(max_length=120, blank=True)
    registration_year = models.DateField(null=True, blank=True)
    rc_no = models.CharField(max_length=120, blank=True)
    rc_validity_from = models.DateField(null=True, blank=True)
    rc_validity_to = models.DateField(null=True, blank=True)
    insurance_no = models.CharField(max_length=120, blank=True)
    insurance_validity_from = models.DateField(null=True, blank=True)
    insurance_validity_to = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.employee.staff_name} - Vehicle'
