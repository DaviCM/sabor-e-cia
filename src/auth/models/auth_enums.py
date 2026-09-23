from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class Roles(Enum):
    WAITER = "waiter"
    COOK = "cook"
    DELIVERER = "deliverer"
    MANAGER = "manager"

    # Será acessível via Role.name e Role.value, respectivamente