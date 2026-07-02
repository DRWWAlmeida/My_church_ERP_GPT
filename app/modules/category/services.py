from app.modules.category.schema import validate_create_category_payload
from app.modules.category.repository import create

def create_category(payload):
    validated_data = validate_create_category_payload(payload)
    category_name = validated_data["categoria"]

    category = create(category_name)

    return category


