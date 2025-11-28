from django.contrib import admin

from .models import (
    AdditionDeduction,
    AssetType,
    Company,
    Degree,
    Department,
    Designation,
    Employee,
    EmployeeAccountInfo,
    EmployeeAssetAssignment,
    EmployeeDependent,
    EmployeeExperience,
    EmployeeQualification,
    EmployeeVehicleDetail,
    ExpenseType,
    Holiday,
    LeaveType,
    Plant,
    SalaryType,
    Shift,
    Site,
    SubExpense,
)
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('billing_name', 'company_group', 'status', 'mobile_no')
    list_filter = ('status',)
    search_fields = ('billing_name', 'company_group', 'gstin_no', 'mobile_no')
    ordering = ('billing_name',)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state')
    search_fields = ('name', 'city', 'state', 'address')
    list_filter = ('state',)
    ordering = ('name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'staff_name',
        'staff_id',
        'company',
        'department',
        'work_location',
        'date_of_join',
    )
    list_filter = ('company', 'department', 'premises_type', 'marital_status')
    search_fields = (
        'staff_name',
        'staff_id',
        'company__billing_name',
        'department',
        'work_location',
    )
    autocomplete_fields = ('company',)
    list_per_page = 25


@admin.register(EmployeeDependent)
class EmployeeDependentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'relationship', 'name', 'gender')
    search_fields = ('employee__staff_name', 'name', 'relationship')
    list_filter = ('relationship', 'gender')
    raw_id_fields = ('employee',)


@admin.register(EmployeeAccountInfo)
class EmployeeAccountInfoAdmin(admin.ModelAdmin):
    list_display = ('employee', 'bank_status', 'salary_type', 'bank_name')
    search_fields = ('employee__staff_name', 'bank_name', 'account_no')
    list_filter = ('bank_status', 'salary_type')
    raw_id_fields = ('employee',)


@admin.register(EmployeeQualification)
class EmployeeQualificationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'education_type', 'degree', 'year_of_passing')
    search_fields = ('employee__staff_name', 'degree', 'college_name')
    list_filter = ('education_type',)
    raw_id_fields = ('employee',)


@admin.register(EmployeeExperience)
class EmployeeExperienceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'company_name', 'designation', 'joining_month')
    search_fields = ('employee__staff_name', 'company_name', 'designation')
    list_filter = ('joining_month',)
    raw_id_fields = ('employee',)


@admin.register(EmployeeAssetAssignment)
class EmployeeAssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'asset_name', 'serial_no', 'status')
    list_filter = ('status',)
    search_fields = ('employee__staff_name', 'asset_name', 'serial_no')
    raw_id_fields = ('employee',)


@admin.register(EmployeeVehicleDetail)
class EmployeeVehicleDetailAdmin(admin.ModelAdmin):
    list_display = ('employee', 'vehicle_type', 'vehicle_company', 'rc_no')
    search_fields = ('employee__staff_name', 'vehicle_type', 'vehicle_company', 'rc_no')
    raw_id_fields = ('employee',)


admin.site.register(
    [
        Shift,
        SalaryType,
        AssetType,
        ExpenseType,
        Holiday,
        Department,
        Designation,
        Degree,
        LeaveType,
        AdditionDeduction,
        SubExpense,
        Plant,
    ]
)
