# Django Permissions - How They Work

## Understanding `'master.view_employee'`

**`'master.view_employee'` is a STRING, NOT a variable.**

It's a permission identifier that Django uses to check if a user has permission to perform an action.

---

## Permission String Format

```
'app_label.permission_codename'
```

### Breakdown:

1. **`master`** = App label (the name of your Django app)
2. **`.`** = Separator
3. **`view_employee`** = Permission codename (action + model name)

---

## How Django Creates Permissions

When you define a model like this:

```python
# master/models.py
class Employee(models.Model):
    staff_name = models.CharField(max_length=255)
    # ... other fields
```

Django **automatically creates** 4 permissions for this model:

| Permission String | Codename | What it allows |
|------------------|----------|----------------|
| `master.add_employee` | `add_employee` | Create new employees |
| `master.change_employee` | `change_employee` | Edit existing employees |
| `master.delete_employee` | `delete_employee` | Delete employees |
| `master.view_employee` | `view_employee` | View/list employees |

---

## Permission Codename Pattern

Django follows this pattern:

```
{action}_{modelname}
```

Where:
- **action** = `add`, `change`, `delete`, or `view`
- **modelname** = Model name in **lowercase**

### Examples:

| Model Name | Permission Codenames |
|------------|---------------------|
| `Employee` | `add_employee`, `change_employee`, `delete_employee`, `view_employee` |
| `Company` | `add_company`, `change_company`, `delete_company`, `view_company` |
| `CompOffEntry` | `add_compoffentry`, `change_compoffentry`, `delete_compoffentry`, `view_compoffentry` |
| `SiteEntry` | `add_siteentry`, `change_siteentry`, `delete_siteentry`, `view_siteentry` |

**Note:** Model names are converted to lowercase and spaces/special characters are handled automatically.

---

## How to Use in Code

### In Views (What we did):

```python
@permission_required('master.view_employee', raise_exception=True)
def employee_list(request):
    # Only users with 'master.view_employee' permission can access
    ...
```

### Check Permission in Code:

```python
# Check if user has permission
if request.user.has_perm('master.view_employee'):
    # User can view employees
    pass

# Check multiple permissions
if request.user.has_perm('master.add_employee') and request.user.has_perm('master.change_employee'):
    # User can add and edit employees
    pass
```

### In Templates:

```django
{% if perms.master.view_employee %}
    <a href="{% url 'master:employee_list' %}">View Employees</a>
{% endif %}

{% if perms.master.add_employee %}
    <a href="{% url 'master:employee_create' %}">Create Employee</a>
{% endif %}
```

---

## Where Permissions Are Stored

Permissions are stored in the database in the `auth_permission` table:

| id | name | content_type_id | codename |
|----|------|-----------------|----------|
| 1 | Can add employee | 5 | add_employee |
| 2 | Can change employee | 5 | change_employee |
| 3 | Can delete employee | 5 | delete_employee |
| 4 | Can view employee | 5 | view_employee |

The `content_type_id` links to the `django_content_type` table which stores:
- `app_label` = `master`
- `model` = `employee`

So Django combines: `app_label` + `codename` = `master.view_employee`

---

## How to See All Permissions

### Via Django Shell:

```python
python manage.py shell

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

# Get all permissions for master app
master_perms = Permission.objects.filter(content_type__app_label='master')
for perm in master_perms:
    print(f"{perm.content_type.app_label}.{perm.codename} - {perm.name}")
```

### Via Django Admin:

1. Go to `/admin/auth/permission/`
2. Filter by "Content type" → Select "master | employee"
3. You'll see all 4 permissions

---

## Custom Permissions

You can also define **custom permissions** in your model:

```python
class Employee(models.Model):
    # ... fields ...
    
    class Meta:
        permissions = [
            ('approve_employee', 'Can approve employee'),
            ('export_employee', 'Can export employee data'),
        ]
```

Then use them:
```python
@permission_required('master.approve_employee')
def approve_employee(request, pk):
    ...
```

---

## Summary

- ✅ `'master.view_employee'` is a **STRING** (permission identifier)
- ✅ Format: `app_label.permission_codename`
- ✅ Django **automatically creates** permissions when you run migrations
- ✅ Permission codename = `{action}_{modelname}` (all lowercase)
- ✅ Not a variable - it's a lookup key in the database
- ✅ You can check permissions using `user.has_perm('master.view_employee')`

---

## Quick Reference

For your HRMS models:

| Model | App | View Permission | Add Permission | Change Permission | Delete Permission |
|-------|-----|-----------------|----------------|-------------------|-------------------|
| Employee | master | `master.view_employee` | `master.add_employee` | `master.change_employee` | `master.delete_employee` |
| Company | master | `master.view_company` | `master.add_company` | `master.change_company` | `master.delete_company` |
| CompOffEntry | entry | `entry.view_compoffentry` | `entry.add_compoffentry` | `entry.change_compoffentry` | `entry.delete_compoffentry` |
| SiteEntry | entry | `entry.view_siteentry` | `entry.add_siteentry` | `entry.change_siteentry` | `entry.delete_siteentry` |

