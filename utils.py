from bson import ObjectId

def convert_to_dict(item):
    if isinstance(item, dict):
        return {key: convert_to_dict(value) for key, value in item.items()}
    elif isinstance(item, (list, tuple)):
        return [convert_to_dict(element) for element in item]
    elif isinstance(item, ObjectId):
        return str(item)
    elif hasattr(item, '__dict__'):
        # objects with __dict__ attribute (such as instances of custom classes)
        return {key: convert_to_dict(value) for key, value in item.__dict__.items() if not key.startswith('_')}
    else:
        return item