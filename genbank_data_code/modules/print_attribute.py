def print_attribute_value (attribute_value):
    if hasattr(attribute_value, '__dict__'):
            print(vars(attribute_value))  # show its fields
    elif isinstance(attribute_value, list):
        for i, item in enumerate(attribute_value, start=1):
                print(f"[{i}] {item if not hasattr(item, '__dict__') else vars(item)}")
    else:
        print(attribute_value)