from app.modules.category.schema import validate_create_category_payload
from app.modules.category.repository import create, get_category_filters

def create_category(payload):
    validated_data = validate_create_category_payload(payload)
    category_name = validated_data["categoria"]

    category = create(category_name)

    return category

def get_category(category_id, category_name):

    conditions = []
    params = []

    if category_id:
        conditions.append("id = ?")
        params.append(category_id)

    if category_name:
        conditions.append('nome LIKE ?')
        params.append(f'%{category_name}%')


    categories = get_category_filters(conditions, params)
    if categories:
        return [dict(category) for category in categories]
    return []

def update_category(payload):
    pass




