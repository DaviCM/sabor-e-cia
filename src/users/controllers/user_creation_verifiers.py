from users.models import User, Employee

def email_already_exists(email: str) -> bool:
    return User.objects.filter(email=email).exists()
    
    
def cpf_already_exists(cpf: str) -> bool:
    return Employee.objects.filter(cpf=cpf).exists()
    
