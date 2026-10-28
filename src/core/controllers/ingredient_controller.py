from typing import Any

from core.models import Ingredient
from core.serializers import CreateIngredientSerializer, UpdateIngredientSerializer, QueryIngredientSerializer
from core.errors import InvalidQuantityError, IngredientNotFoundError
from users.models import Employee
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError

def create_ingredient(current_employee: Employee, params: dict[str, Any]) -> Ingredient:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    description = params.get("description")
    quantity = params.get("quantity")
    unit = params.get("unit")
    provider = params.get("provider")

    if quantity < 0:
        raise InvalidQuantityError

    new_ingredient = Ingredient(
        description=description,
        quantity=quantity,
        unit=unit,
        provider=provider
    )

    new_ingredient.save()

    return new_ingredient

 
def list_ingredients(current_employee: Employee, params: dict[str, Any]):
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    id = params.get("id")
    description = params.get("description")
    minimum_quantity = params.get("minimum_quantity")
    maximum_quantity = params.get("maximum_quantity")
    unit = params.get("unit")
    provider = params.get("provider")

    if (minimum_quantity != None) and (maximum_quantity != None):
        if minimum_quantity < 0:
            raise InvalidQuantityError

    if maximum_quantity < 0:
        raise InvalidQuantityError
        
    if minimum_quantity > maximum_quantity:
        raise InvalidQuantityError

    ingredients = Ingredient.objects.all()

    if id != None:
        ingredients = ingredients.filter(pk=id)

    if description != None:
        ingredients = ingredients.filter(description__icontains=description)

    if minimum_quantity != None:
        ingredients = ingredients.filter(quantity__gte=minimum_quantity)

    if minimum_quantity != None:
        ingredients = ingredients.filter(quantity__lte=maximum_quantity)

    if unit != None:
        ingredients = ingredients.filter(unit=unit)

    if provider != None:
        ingredients = ingredients.filter(provider__icontains=provider)

    if ingredients.exists() == False:
        raise IngredientNotFoundError
    
    return ingredients


def update_ingredient(current_employee: Employee, params: dict[str, Any]) -> Ingredient:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    id = params.get("id")
    description = params.get("description")
    quantity = params.get("quantity")
    unit = params.get("unit")
    provider = params.get("provider")

    if (quantity != None) and (quantity < 0):
        raise InvalidQuantityError

    try:
        target_ingredient = Ingredient.objects.get(pk=id)
    except Ingredient.DoesNotExist:
        raise IngredientNotFoundError

    if description != None:
        target_ingredient.description = description

    if quantity != None:
        target_ingredient.quantity = quantity

    if unit != None:
        target_ingredient.unit = unit

    if provider != None:
        target_ingredient.provider = provider

    target_ingredient.save()

    return target_ingredient


def delete_ingredient(current_employee: Employee, target_ingredient_id: int) -> None:
    if current_employee == None:
        raise EmployeeNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    try:
        target_ingredient = Ingredient.objects.get(pk=target_ingredient_id)
    except Ingredient.DoesNotExist:
        raise IngredientNotFoundError

    target_ingredient.delete()