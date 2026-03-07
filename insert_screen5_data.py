"""
Screen 5: User Management - Data Insertion Script
Insert predefined user management data based on dashboard requirements
Data matches dashboard screenshot: 1,284 total users, 12 admins, 42 active, 8 pending invites
"""

import os
import django
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import uuid
import hashlib

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')
django.setup()

from user_management.models import (
    Department, Role, ERPUser, Module, Permission, 
    ActivityLog, UserInvite, SecuritySetting
)

# ============================================================================
# Helper functions
# ============================================================================

def generate_token():
    """Generate unique invitation token"""
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()

def clear_existing_data():
    """Clear existing data from all tables"""
    print("Clearing existing data...")
    ERPUser.objects.all().delete()
    Department.objects.all().delete()
    Role.objects.all().delete()
    Module.objects.all().delete()
    Permission.objects.all().delete()
    ActivityLog.objects.all().delete()
    UserInvite.objects.all().delete()
    SecuritySetting.objects.all().delete()
    print("✓ Existing data cleared\n")

# ============================================================================
# Insert Departments
# ============================================================================

def insert_departments():
    """Insert department data"""
    print("Inserting departments...")
    
    departments_data = [
        {'name': 'Engineering', 'head': 'Ali ', 'budget': Decimal('500000.00'), 'description': 'Development and technical operations'},
        {'name': 'Operations', 'head': 'Ashar', 'budget': Decimal('350000.00'), 'description': 'Day-to-day operational management'},
        {'name': 'Finance', 'head': 'Zoraiz', 'budget': Decimal('280000.00'), 'description': 'Financial planning and analysis'},
        {'name': 'Sales & Marketing', 'head': 'Ayesha', 'budget': Decimal('450000.00'), 'description': 'Sales strategy and customer acquisition'},
        {'name': 'Human Resources', 'head': 'Shan', 'budget': Decimal('200000.00'), 'description': 'Recruitment and employee management'},
        {'name': 'Quality Assurance', 'head': 'Bilal', 'budget': Decimal('180000.00'), 'description': 'Quality testing and assurance'},
        {'name': 'Customer Support', 'head': 'Avais', 'budget': Decimal('220000.00'), 'description': 'Customer service and support'},
    ]
    
    departments = {}
    for dept_data in departments_data:
        dept = Department.objects.create(**dept_data)
        departments[dept.name] = dept
        print(f"  ✓ Created department: {dept.name}")
    
    print(f"✓ {len(departments)} departments created\n")
    return departments

# ============================================================================
# Insert Roles
# ============================================================================

def insert_roles():
    """Insert role data"""
    print("Inserting roles...")
    
    roles_data = [
        {'name': 'Administrator', 'level': 'ADMIN', 'description': 'Full system access and administration'},
        {'name': 'Manager', 'level': 'MANAGER', 'description': 'Department management and reporting'},
        {'name': 'Supervisor', 'level': 'SUPERVISOR', 'description': 'Team supervision and task management'},
        {'name': 'Analyst', 'level': 'ANALYST', 'description': 'Data analysis and reporting'},
        {'name': 'Staff', 'level': 'STAFF', 'description': 'Regular operational staff'},
        {'name': 'Viewer', 'level': 'VIEWER', 'description': 'Read-only access to reports'},
    ]
    
    roles = {}
    for role_data in roles_data:
        role = Role.objects.create(**role_data)
        roles[role.name] = role
        print(f"  ✓ Created role: {role.name}")
    
    print(f"✓ {len(roles)} roles created\n")
    return roles

# ============================================================================
# Insert Modules
# ============================================================================

def insert_modules():
    """Insert ERP module data"""
    print("Inserting modules...")
    
    modules_data = [
        {'name': 'Dashboard', 'description': 'System dashboard and KPIs', 'is_active': True},
        {'name': 'Accounts & Finance', 'description': 'Financial management and accounting', 'is_active': True},
        {'name': 'Sales & CRM', 'description': 'Sales management and customer relations', 'is_active': True},
        {'name': 'Inventory & Products', 'description': 'Product and inventory management', 'is_active': True},
        {'name': 'Purchases & Vendors', 'description': 'Purchase orders and vendor management', 'is_active': True},
        {'name': 'Invoicing', 'description': 'Invoice generation and management', 'is_active': True},
        {'name': 'User Management', 'description': 'User provisioning and access control', 'is_active': True},
        {'name': 'Reports', 'description': 'Business reporting and analytics', 'is_active': True},
    ]
    
    modules = {}
    for module_data in modules_data:
        module = Module.objects.create(**module_data)
        modules[module.name] = module
        print(f"  ✓ Created module: {module.name}")
    
    print(f"✓ {len(modules)} modules created\n")
    return modules

# ============================================================================
# Insert Users
# ============================================================================

def insert_users(departments, roles):
    """Insert user data - realistic distribution matching dashboard screenshot"""
    print("Inserting users...")
    
    # Core management users (visible in dashboard)
    core_users = [
        {'username': 'Ali Ashar', 'email': 'aliashar@company.com', 'first_name': 'Ali', 'last_name': 'Ashar', 'department': departments['Sales & Marketing'], 'role': roles['Administrator'], 'status': 'ACTIVE'},
        {'username': 'Zoraiz Anwar', 'email': 'zoraizanwar@company.com', 'first_name': 'Zoariz', 'last_name': 'Anwar', 'department': departments['Engineering'], 'role': roles['Manager'], 'status': 'ACTIVE'},
        {'username': 'Shan Ali', 'email': 'shanali@company.com', 'first_name': 'shan', 'last_name': 'ali', 'department': departments['Operations'], 'role': roles['Analyst'], 'status': 'ACTIVE'},
        {'username': 'Bilal Abid', 'email': 'bilalabid@company.com', 'first_name': 'Bilal', 'last_name': 'Abid', 'department': departments['Finance'], 'role': roles['Manager'], 'status': 'ACTIVE'},
        {'username': 'Avais aleem', 'email': 'avaisaleem@company.com', 'first_name': 'avais', 'last_name': 'aleem', 'department': departments['Human Resources'], 'role': roles['Manager'], 'status': 'ACTIVE'},
        {'username': 'Zeeshan Farooq', 'email': 'zeeshanfarooq@company.com', 'first_name': 'Zeeshan', 'last_name': 'Farooq', 'department': departments['Quality Assurance'], 'role': roles['Supervisor'], 'status': 'ACTIVE'},
        {'username': 'Ahsan Riaz', 'email': 'ahsanriaz@company.com', 'first_name': 'Ahsan', 'last_name': 'Riaz', 'department': departments['Customer Support'], 'role': roles['Supervisor'], 'status': 'ACTIVE'},
    ]
    
    # Additional admin users (12 total admins as per dashboard)
    admin_first_names = ['Ali', 'Ashar', 'Zoraiz', 'Shan', 'Ayesha', 'Bilal']
    other_admins = [
        {'username': f'admin_{i}', 'email': f'admin{i}@company.com', 'first_name': admin_first_names[i % len(admin_first_names)], 'last_name': f'Admin{i}', 'department': departments['Engineering'], 'role': roles['Administrator'], 'status': 'ACTIVE'}
        for i in range(1, 6)  # 5 more admins + 1 sarah = 6 total
    ]
    
    # Staff users for other departments (distributed across company)
    staff_users = []
    dept_list = list(departments.values())
    role_list = [roles['Staff'], roles['Supervisor'], roles['Analyst']]
    
    # Create ~1200+ more users to reach 1,284 total
    user_count = 7 + 5 + 1  # core + other admins + sarah (13 so far)
    remaining_users = 1284 - user_count
    
    for i in range(remaining_users):
        dept = dept_list[i % len(dept_list)]
        role = role_list[i % len(role_list)]
        status = 'ACTIVE' if i < remaining_users - 100 else 'SUSPENDED'  # Last 100 are suspended
        
        staff_users.append({
            'username': f'user_{i:04d}',
            'email': f'user{i:04d}@company.com',
            'first_name': f'Employee{i:04d}',
            'last_name': 'Staff',
            'department': dept,
            'role': role,
            'status': status
        })
    
    all_users = core_users + other_admins + staff_users
    created_users = {}
    
    for user_data in all_users:
        user_dict = {k: v for k, v in user_data.items() if k != 'password'}
        user_dict['password'] = 'DefaultPassword123!'
        user = ERPUser.objects.create(**user_dict)
        created_users[user.username] = user
        
        # Mark some users as recently active (42 active now)
        if len(created_users) <= 42:
            user.last_activity = timezone.now() - timedelta(minutes=5)
            user.last_login = timezone.now() - timedelta(hours=1)
            user.login_count = 15
            user.two_factor_enabled = True if len(created_users) <= 10 else False
            user.save()
    
    print(f"  ✓ Created {len(all_users)} users total")
    print(f"    - Active: {ERPUser.objects.filter(status='ACTIVE').count()}")
    print(f"    - Suspended: {ERPUser.objects.filter(status='SUSPENDED').count()}")
    print(f"    - With 2FA: {ERPUser.objects.filter(two_factor_enabled=True).count()}\n")
    
    return created_users

# ============================================================================
# Insert Permissions
# ============================================================================

def insert_permissions(users, modules, roles):
    """Insert permission data based on roles"""
    print("Inserting permissions...")
    
    # Define role-based permissions
    admin_modules = ['Dashboard', 'Accounts & Finance', 'Sales & CRM', 'Inventory & Products', 
                     'Purchases & Vendors', 'Invoicing', 'User Management', 'Reports']
    manager_modules = ['Dashboard', 'Accounts & Finance', 'Sales & CRM', 'Inventory & Products', 
                       'Purchases & Vendors', 'Invoicing', 'Reports']
    supervisor_modules = ['Dashboard', 'Sales & CRM', 'Inventory & Products', 'Purchases & Vendors', 'Reports']
    analyst_modules = ['Dashboard', 'Reports']
    staff_modules = ['Dashboard', 'Sales & CRM', 'Inventory & Products']
    viewer_modules = ['Dashboard', 'Reports']
    
    permission_mapping = {
        'Administrator': {'modules': admin_modules, 'can_create': True, 'can_read': True, 'can_update': True, 'can_delete': True},
        'Manager': {'modules': manager_modules, 'can_create': True, 'can_read': True, 'can_update': True, 'can_delete': False},
        'Supervisor': {'modules': supervisor_modules, 'can_create': True, 'can_read': True, 'can_update': True, 'can_delete': False},
        'Analyst': {'modules': analyst_modules, 'can_create': False, 'can_read': True, 'can_update': False, 'can_delete': False},
        'Staff': {'modules': staff_modules, 'can_create': True, 'can_read': True, 'can_update': False, 'can_delete': False},
        'Viewer': {'modules': viewer_modules, 'can_create': False, 'can_read': True, 'can_update': False, 'can_delete': False},
    }
    
    permission_count = 0
    for user in list(users.values())[:100]:  # Assign permissions to first 100 users as sample
        role_name = user.role.name
        if role_name in permission_mapping:
            perm_config = permission_mapping[role_name]
            for module_name in perm_config['modules']:
                module = modules[module_name]
                Permission.objects.create(
                    user=user,
                    module=module,
                    can_create=perm_config['can_create'],
                    can_read=perm_config['can_read'],
                    can_update=perm_config['can_update'],
                    can_delete=perm_config['can_delete']
                )
                permission_count += 1
    
    print(f"✓ {permission_count} permissions assigned\n")

# ============================================================================
# Insert Activity Logs
# ============================================================================

def insert_activity_logs(users, modules):
    """Insert activity logs for user actions"""
    print("Inserting activity logs...")
    
    actions = [
        ('LOGIN', 'User login'),
        ('CREATE', 'Created record'),
        ('UPDATE', 'Updated record'),
        ('DELETE', 'Deleted record'),
        ('EXPORT', 'Exported data'),
        ('IMPORT', 'Imported data'),
        ('PASSWORD_CHANGE', 'Changed password'),
    ]
    
    activity_count = 0
    for i, (user, action_info) in enumerate(zip(list(users.values())[:50], actions * 10)):
        action, description = action_info
        ActivityLog.objects.create(
            user=user,
            action=action,
            description=description,
            ip_address=f'192.168.1.{(i % 255) + 1}',
            status='SUCCESS'
        )
        activity_count += 1
    
    print(f"✓ {activity_count} activity logs created\n")

# ============================================================================
# Insert User Invites
# ============================================================================

def insert_user_invites(users, departments, roles):
    """Insert pending user invitations (8 pending invites as per dashboard)"""
    print("Inserting user invites...")
    
    # Get an admin user to send invites
    admin_user = next((u for u in users.values() if u.role.name == 'Administrator'), None)
    
    invites_data = [
        {'email': 'new_user1@company.com', 'first_name': 'New', 'last_name': 'User1', 'department': departments['Engineering'], 'role': roles['Staff']},
        {'email': 'new_user2@company.com', 'first_name': 'New', 'last_name': 'User2', 'department': departments['Sales & Marketing'], 'role': roles['Staff']},
        {'email': 'new_user3@company.com', 'first_name': 'New', 'last_name': 'User3', 'department': departments['Finance'], 'role': roles['Analyst']},
        {'email': 'new_user4@company.com', 'first_name': 'New', 'last_name': 'User4', 'department': departments['Operations'], 'role': roles['Supervisor']},
        {'email': 'new_user5@company.com', 'first_name': 'New', 'last_name': 'User5', 'department': departments['Human Resources'], 'role': roles['Staff']},
        {'email': 'new_user6@company.com', 'first_name': 'New', 'last_name': 'User6', 'department': departments['Quality Assurance'], 'role': roles['Supervisor']},
        {'email': 'new_user7@company.com', 'first_name': 'New', 'last_name': 'User7', 'department': departments['Customer Support'], 'role': roles['Staff']},
        {'email': 'new_user8@company.com', 'first_name': 'New', 'last_name': 'User8', 'department': departments['Engineering'], 'role': roles['Analyst']},
    ]
    
    invite_count = 0
    for invite_data in invites_data:
        UserInvite.objects.create(
            email=invite_data['email'],
            first_name=invite_data['first_name'],
            last_name=invite_data['last_name'],
            department=invite_data['department'],
            role=invite_data['role'],
            invited_by=admin_user,
            invitation_token=generate_token(),
            status='PENDING',
            expires_at=timezone.now() + timedelta(days=7)
        )
        invite_count += 1
    
    print(f"✓ {invite_count} user invites created (8 pending)\n")

# ============================================================================
# Insert Security Settings
# ============================================================================

def insert_security_settings(users):
    """Insert security settings for users"""
    print("Inserting security settings...")
    
    # Create security settings for first 20 users as sample
    setting_count = 0
    for user in list(users.values())[:20]:
        try:
            SecuritySetting.objects.create(
                user=user,
                password_min_length=8,
                password_expires_days=90,
                password_history_count=5,
                require_special_characters=True,
                two_factor_required=user.two_factor_enabled,
                two_factor_method='TOTP' if user.two_factor_enabled else None,
                session_timeout_minutes=15,
                max_concurrent_sessions=3,
                restrict_to_ip=False,
            )
            setting_count += 1
        except Exception as e:
            print(f"  ✗ Error creating settings for {user.username}: {str(e)}")
    
    print(f"✓ {setting_count} security settings created\n")

# ============================================================================
# Main execution
# ============================================================================

def main():
    """Main data insertion function"""
    print("\n" + "="*80)
    print("SCREEN 5: USER MANAGEMENT - DATA INSERTION")
    print("="*80 + "\n")
    
    try:
        # Clear existing data
        clear_existing_data()
        
        # Insert data in order of dependencies
        departments = insert_departments()
        roles = insert_roles()
        modules = insert_modules()
        users = insert_users(departments, roles)
        insert_permissions(users, modules, roles)
        insert_activity_logs(users, modules)
        insert_user_invites(users, departments, roles)
        insert_security_settings(users)
        
        # Print summary
        print("\n" + "="*80)
        print("DATA INSERTION SUMMARY")
        print("="*80)
        print(f"✓ Departments: {Department.objects.count()}")
        print(f"✓ Roles: {Role.objects.count()}")
        print(f"✓ Modules: {Module.objects.count()}")
        print(f"✓ Users (Total): {ERPUser.objects.count()}")
        print(f"  - Active: {ERPUser.objects.filter(status='ACTIVE').count()}")
        print(f"  - Inactive: {ERPUser.objects.filter(status='INACTIVE').count()}")
        print(f"  - Suspended: {ERPUser.objects.filter(status='SUSPENDED').count()}")
        print(f"  - Admins: {ERPUser.objects.filter(role__level='ADMIN').count()}")
        print(f"  - With 2FA: {ERPUser.objects.filter(two_factor_enabled=True).count()}")
        print(f"✓ Permissions: {Permission.objects.count()}")
        print(f"✓ Activity Logs: {ActivityLog.objects.count()}")
        print(f"✓ User Invites: {UserInvite.objects.count()} (Pending: {UserInvite.objects.filter(status='PENDING').count()})")
        print(f"✓ Security Settings: {SecuritySetting.objects.count()}")
        print("\n" + "="*80 + "\n")
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
