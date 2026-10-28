from typing import Any

from logs.models import DeliveryLog
from logs.serializers import QueryDeliveryLogSerializer
from logs.errors import *
from core.models import Order
from users.models import Employee
from users.errors import UserHasNoPermissionError
from users.models import ClientAddress
