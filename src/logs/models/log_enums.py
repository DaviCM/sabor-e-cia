from enum import Enum, verify, UNIQUE

@verify(UNIQUE)
class PaymentMethods(Enum):
    CASH = "cash"
    PIX = "pix"
    DEBIT = "debit"
    CREDIT = "credit"
    VA_VR = "va_vr"