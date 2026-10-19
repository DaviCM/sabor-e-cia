from core.models import Ingredient
from core.serializers import CreateIngredientSerializer, UpdateIngredientSerializer, QueryIngredientSerializer
from core.errors import InvalidQuantityError, IngredientNotFoundError
from users.models import Employee
from users.errors import UserNotFoundError, UserHasNoPermissionError

def create_ingredient(current_employee: Employee, params: CreateIngredientSerializer) -> Ingredient:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if params.quantity < 0:
        raise InvalidQuantityError

    new_ingredient = Ingredient(
        description=params.description,
        quantity=params.quantity,
        unit=params.unit,
        provider=params.provider
    )

    new_ingredient.save()

    return new_ingredient

 
def list_ingredients(current_employee: Employee, params: QueryIngredientSerializer):
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if (params.minimum_quantity != None) and (params.maximum_quantity != None):
        if params.minimum_quantity < 0:
            raise InvalidQuantityError

    if params.maximum_quantity < 0:
        raise InvalidQuantityError
        
    if params.minimum_quantity > params.maximum_quantity:
        raise InvalidQuantityError

    ingredients = Ingredient.objects.all()

    if params.description != None:
        ingredients = ingredients.filter(description__icontains=params.description)

    if params.minimum_quantity != None:
        ingredients = ingredients.filter(quantity__gte=params.minimum_quantity)

    if params.minimum_quantity != None:
        ingredients = ingredients.filter(quantity__lte=params.maximum_quantity)

    if params.unit != None:
        ingredients = ingredients.filter(unit=params.unit)

    if params.provider != None:
        ingredients = ingredients.filter(provider__icontains=params.provider)

    if ingredients.exists() == False:
        raise IngredientNotFoundError
    
    return ingredients


def update_ingredient(current_employee: Employee, params: UpdateIngredientSerializer) -> Ingredient:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    if (params.quantity != None) and (params.quantity < 0):
        raise InvalidQuantityError

    target_ingredient = Ingredient.objects.filter(pk=params.id)
    
    if target_ingredient.exists == False:
        raise IngredientNotFoundError

    if params.description != None:
        target_ingredient.description = params.description

    if params.quantity != None:
        target_ingredient.quantity = params.quantity

    if params.unit != None:
        target_ingredient.unit = params.unit

    if params.provider != None:
        target_ingredient.provider = params.provider

    target_ingredient.save()

    return target_ingredient


def delete_ingredient(current_employee: Employee, target_ingredient_id: int) -> None:
    if current_employee == None:
        raise UserNotFoundError

    if current_employee.user.is_staff == False:
        raise UserHasNoPermissionError

    target_ingredient = Ingredient.objects.filter(pk=target_ingredient_id)

    if target_ingredient.exists() == False:
        raise IngredientNotFoundError

    target_ingredient.delete()