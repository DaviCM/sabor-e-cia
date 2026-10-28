from typing import Any
from logs.models import PaymentLog, PaymentMethods
from logs.errors import LogNotFoundError, InvalidLogDateError, InvalidPaymentMethodError
from core.models import Order
from core.errors import OrderNotFoundError, InvalidValueError
from users.models import Employee
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError

def create_payment_log(current_employee: Employee, params: dict[str, Any]) -> PaymentLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    value = params["value"]
    if value < 0:
        raise InvalidValueError

    payment_method = params["payment_method"]
    valid_methods = [m.value for m in PaymentMethods]
    if payment_method not in valid_methods and payment_method not in PaymentMethods:
        raise InvalidPaymentMethodError
    method_val = payment_method.value if isinstance(payment_method, PaymentMethods) else payment_method

    order = params.get("order")
    order_id = params.get("order_id")
    if order is None:
        if order_id is None:
            raise OrderNotFoundError
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise OrderNotFoundError

    new_log = PaymentLog(
        payment_method=method_val,
        value=value,
        order=order,
    )
    if "datetime" in params and params["datetime"] is not None:
        new_log.datetime = params["datetime"]

    new_log.save()
    return new_log


def list_payment_logs(current_employee: Employee, params: dict[str, Any]):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    minimum_date = params.get("minimum_date")
    maximum_date = params.get("maximum_date")
    minimum_value = params.get("minimum_value")
    maximum_value = params.get("maximum_value")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidLogDateError

    if (minimum_value is not None) and (minimum_value < 0):
        raise InvalidValueError

    if (maximum_value is not None) and (maximum_value < 0):
        raise InvalidValueError

    if (minimum_value is not None) and (maximum_value is not None):
        if minimum_value > maximum_value:
            raise InvalidValueError

    payment_method = params.get("payment_method")
    if payment_method is not None:
        valid_methods = [m.value for m in PaymentMethods]
        if payment_method not in valid_methods and payment_method not in PaymentMethods:
            raise InvalidPaymentMethodError

    logs = PaymentLog.objects.all()

    log_id = params.get("id")
    if log_id is not None:
        logs = logs.filter(pk=log_id)

    if minimum_date is not None:
        logs = logs.filter(datetime__gte=minimum_date)

    if maximum_date is not None:
        logs = logs.filter(datetime__lte=maximum_date)

    if payment_method is not None:
        method_val = payment_method.value if isinstance(payment_method, PaymentMethods) else payment_method
        logs = logs.filter(payment_method=method_val)

    if minimum_value is not None:
        logs = logs.filter(value__gte=minimum_value)

    if maximum_value is not None:
        logs = logs.filter(value__lte=maximum_value)

    order_id = params.get("order_id")
    if order_id is not None:
        logs = logs.filter(order__id=order_id)

    if not logs.exists():
        raise LogNotFoundError

    return logs


def get_payment_log(current_employee: Employee, log_id: int) -> PaymentLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        return PaymentLog.objects.get(pk=log_id)
    except PaymentLog.DoesNotExist:
        raise LogNotFoundError

