from typing import Any
from core.models import Ingredient
from core.errors import InvalidQuantityError, IngredientNotFoundError
from users.models import Employee
from users.errors import EmployeeNotFoundError, UserHasNoPermissionError

def create_ingredient(current_employee: Employee, params: dict[str, Any]) -> Ingredient:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    if params["quantity"] < 0:
        raise InvalidQuantityError

    new_ingredient = Ingredient(
        description=params["description"],
        quantity=params["quantity"],
        unit=params["unit"],
        provider=params["provider"]
    )

    new_ingredient.save()

    return new_ingredient

 
def list_ingredients(current_employee: Employee, params: dict[str, Any]):
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    minimum_quantity = params.get("minimum_quantity")
    maximum_quantity = params.get("maximum_quantity")

    if (minimum_quantity is not None) and (maximum_quantity is not None):
        if minimum_quantity < 0:
            raise InvalidQuantityError
        
        if minimum_quantity > maximum_quantity:
            raise InvalidQuantityError

    ingredients = Ingredient.objects.all()

    description = params.get("description")
    if description is not None:
        ingredients = ingredients.filter(description__icontains=description)

    if minimum_quantity is not None:
        ingredients = ingredients.filter(quantity__gte=minimum_quantity)

    if maximum_quantity is not None:
        ingredients = ingredients.filter(quantity__lte=maximum_quantity)

    unit = params.get("unit")
    if unit is not None:
        ingredients = ingredients.filter(unit=unit)

    provider = params.get("provider")
    if provider is not None:
        ingredients = ingredients.filter(provider__icontains=provider)

    if not ingredients.exists():
        raise IngredientNotFoundError
    
    return ingredients


def update_ingredient(current_employee: Employee, params: dict[str, Any]) -> Ingredient:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    quantity = params.get("quantity")
    if (quantity is not None) and (quantity < 0):
        raise InvalidQuantityError

    try:
        target_ingredient = Ingredient.objects.get(pk=params["id"])
    except Ingredient.DoesNotExist:
        raise IngredientNotFoundError

    description = params.get("description")
    if description is not None:
        target_ingredient.description = description

    if quantity is not None:
        target_ingredient.quantity = quantity

    unit = params.get("unit")
    if unit is not None:
        target_ingredient.unit = unit

    provider = params.get("provider")
    if provider is not None:
        target_ingredient.provider = provider

    target_ingredient.save()

    return target_ingredient


def delete_ingredient(current_employee: Employee, target_ingredient_id: int) -> None:
    if current_employee is None:
        raise EmployeeNotFoundError

    if not current_employee.user.is_staff:
        raise UserHasNoPermissionError

    try:
        target_ingredient = Ingredient.objects.get(pk=target_ingredient_id)
    except Ingredient.DoesNotExist:
        raise IngredientNotFoundError

    target_ingredient.delete()