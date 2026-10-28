from typing import Any
from logs.models import DeliveryLog
from logs.errors import LogNotFoundError, InvalidLogDateError
from core.models import Order
from core.errors import OrderNotFoundError, InvalidValueError
from users.models import Employee, ClientAddress
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError, AddressNotFoundError

def create_delivery_log(current_employee: Employee, params: dict[str, Any]) -> DeliveryLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    delivery_fee = params["delivery_fee"]
    if delivery_fee < 0:
        raise InvalidValueError

    address = params.get("address")
    address_id = params.get("address_id")
    if address is None:
        if address_id is None:
            raise AddressNotFoundError
        try:
            address = ClientAddress.objects.get(pk=address_id)
        except ClientAddress.DoesNotExist:
            raise AddressNotFoundError

    deliverer = params.get("deliverer")
    deliverer_id = params.get("deliverer_id")
    if deliverer is None:
        if deliverer_id is None:
            raise EmployeeNotFoundError
        try:
            deliverer = Employee.objects.get(pk=deliverer_id)
        except Employee.DoesNotExist:
            raise EmployeeNotFoundError

    order = params.get("order")
    order_id = params.get("order_id")
    if order is None:
        if order_id is None:
            raise OrderNotFoundError
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise OrderNotFoundError

    new_log = DeliveryLog(
        delivery_fee=delivery_fee,
        address=address,
        deliverer=deliverer,
        order=order,
    )
    if "datetime" in params and params["datetime"] is not None:
        new_log.datetime = params["datetime"]

    new_log.save()
    return new_log


def list_delivery_logs(current_employee: Employee, params: dict[str, Any]):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    minimum_date = params.get("minimum_date")
    maximum_date = params.get("maximum_date")
    minimum_fee = params.get("minimum_fee")
    maximum_fee = params.get("maximum_fee")

    if (minimum_date is not None) and (maximum_date is not None):
        if minimum_date > maximum_date:
            raise InvalidLogDateError

    if (minimum_fee is not None) and (minimum_fee < 0):
        raise InvalidValueError

    if (maximum_fee is not None) and (maximum_fee < 0):
        raise InvalidValueError

    if (minimum_fee is not None) and (maximum_fee is not None):
        if minimum_fee > maximum_fee:
            raise InvalidValueError

    logs = DeliveryLog.objects.all()

    log_id = params.get("id")
    if log_id is not None:
        logs = logs.filter(pk=log_id)

    if minimum_date is not None:
        logs = logs.filter(datetime__gte=minimum_date)

    if maximum_date is not None:
        logs = logs.filter(datetime__lte=maximum_date)

    if minimum_fee is not None:
        logs = logs.filter(delivery_fee__gte=minimum_fee)

    if maximum_fee is not None:
        logs = logs.filter(delivery_fee__lte=maximum_fee)

    address_id = params.get("address_id")
    if address_id is not None:
        logs = logs.filter(address__id=address_id)

    address_cep = params.get("address_cep")
    if address_cep is not None:
        logs = logs.filter(address__cep__icontains=address_cep)

    address_description = params.get("address_description")
    if address_description is not None:
        logs = logs.filter(address__description__icontains=address_description)

    address_number = params.get("address_number")
    if address_number is not None:
        logs = logs.filter(address__number=address_number)

    deliverer_id = params.get("deliverer_id")
    if deliverer_id is not None:
        logs = logs.filter(deliverer__id=deliverer_id)

    deliverer_username = params.get("deliverer_username")
    if deliverer_username is not None:
        logs = logs.filter(deliverer__user__username__icontains=deliverer_username)

    order_id = params.get("order_id")
    if order_id is not None:
        logs = logs.filter(order__id=order_id)

    if not logs.exists():
        raise LogNotFoundError

    return logs


def get_delivery_log(current_employee: Employee, log_id: int) -> DeliveryLog:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        return DeliveryLog.objects.get(pk=log_id)
    except DeliveryLog.DoesNotExist:
        raise LogNotFoundError
