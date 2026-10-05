from users.models import User, Client, ClientAddress
from users.serializers import CreateClientSerializer, UpdateClientSerializer, CreateAddressSerializer, UpdateAddressSerializer

def create_client(params: CreateClientSerializer):
    new_client = Client(
        user=User.objects.create_user(
            username=params.username,
            email=params.email,
            password=params.password,
            extra_fields={
                "first_name": params.first_name,
                "last_name": params.last_name,
            },
        ),
        phone=params.phone,
    )

    new_client.save()