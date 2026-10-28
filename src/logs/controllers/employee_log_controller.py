from typing import Any
from logs.models import EmployeeLog
from logs.errors import LogNotFoundError, InvalidLogDateError
from users.models import Employee, Roles
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError, InvalidRoleError

def create_employee_log(current_employee: Employee, params: dict[str, Any]) -> EmployeeLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    role = params["role"]
    valid_roles = [r.value for r in Roles]
    if role not in valid_roles and role not in Roles:
        raise InvalidRoleError
    role_val = role.value if isinstance(role, Roles) else role

    employee = params.get("employee")
    employee_id = params.get("employee_id")
    if employee is None and employee_id is not None:
        try:
            employee = Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            raise EmployeeNotFoundError

    new_log = EmployeeLog(
        role=role_val,
        employee=employee,
    )
    if "datetime" in params and params["datetime"] is not None:
        new_log.datetime = params["datetime"]

    new_log.save()
    return new_log


def list_employee_logs(current_employee: Employee, params: dict[str, Any]):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    minimum_date = params.get("minimum_date")
    maximum_date = params.get("maximum_date")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidLogDateError

    role = params.get("role")
    if role is not None:
        valid_roles = [r.value for r in Roles]
        if role not in valid_roles and role not in Roles:
            raise InvalidRoleError

    logs = EmployeeLog.objects.all()

    log_id = params.get("id")
    if log_id is not None:
        logs = logs.filter(pk=log_id)

    if minimum_date is not None:
        logs = logs.filter(datetime__gte=minimum_date)

    if maximum_date is not None:
        logs = logs.filter(datetime__lte=maximum_date)

    if role is not None:
        role_val = role.value if isinstance(role, Roles) else role
        logs = logs.filter(role=role_val)

    employee_id = params.get("employee_id")
    if employee_id is not None:
        logs = logs.filter(employee__id=employee_id)

    employee_username = params.get("employee_username")
    if employee_username is not None:
        logs = logs.filter(employee__user__username__icontains=employee_username)

    if not logs.exists():
        raise LogNotFoundError

    return logs


def get_employee_log(current_employee: Employee, log_id: int) -> EmployeeLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        return EmployeeLog.objects.get(pk=log_id)
    except EmployeeLog.DoesNotExist:
        raise LogNotFoundError

