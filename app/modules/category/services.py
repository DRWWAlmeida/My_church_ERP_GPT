from app.modules.category.schema import validate_create_category_payload
from app.modules.category.repository import create, get_all

def create_category(payload):
    validated_data = validate_create_category_payload(payload)
    category_name = validated_data["categoria"]

    category = create(category_name)

    return category

def get_all_category():

    categories = get_all()
    categories = [dict(category) for category in categories]

    return categories
    

def update_category(payload):
    pass




