from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class OrderCategories(Enum):
    DELVERY = "delivery"
    PHONE = "phone"
    LOCAL = "local"



@verify(UNIQUE)
class OrderStatus(Enum):
    RECEIVED = "received"
    PREPARING = "preparing"
    READY = "ready"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELED = "canceled"



@verify(UNIQUE)
class ProductCategories(Enum):
    DRINK = "drink"
    UNITARY = "unitary"
    PORTION = "portion"



@verify(UNIQUE)
class ProductTypes(Enum):
    SMALL = "small"
    MEDIUM = "medium" 
    LARGE = "large"



@verify(UNIQUE)
class Units(Enum):
    KG = "kg"
    L = "l"
    UNIT = "unit"