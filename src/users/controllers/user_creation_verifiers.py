from users.models import User, Client, Employee

def email_already_exists(email: str):
    target_email = User.objects.filter(email=email)
    
    if target_email.exists() == True:
        return True
    else:
        return False
    
    
def cpf_already_exists(cpf: str):
    target_cpf = Employee.objects.filter(cpf=cpf)
    
    if target_cpf.exists() == True:
        return True
    else:
        return False
    
    
