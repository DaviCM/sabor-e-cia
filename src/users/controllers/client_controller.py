from users.models import User, Client, ClientAddress

def create_client(firstname, lastname, username, email, password, phone):
    new_client = Client(
        user = User(
            first_name=firstname,
            last_name=lastname,
            username=username,
            email=email,
            password=password
        ),
        phone=phone
    )