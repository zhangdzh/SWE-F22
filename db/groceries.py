"""
This module is for a singular grocery list structure. It contains functions
necessary to interact with a grocery list.
"""

import groc_types as gtyp

GROC_TYPE = 'grocery_type'
QUANTITY = 'quantity'
EXPIRATION_DATE = 'expiration_date'

REQUIRED_FIELDS = [GROC_TYPE, QUANTITY, EXPIRATION_DATE]
# example of a grocery list structure
grocery_list = {
    "item1": {
        GROC_TYPE: gtyp.BAKED_GOODS,
        QUANTITY: 10,
        EXPIRATION_DATE: "10-20-2022"
    }
}


def get_items():
    """
    returns a list of all items in the grocery list
    """
    return list(grocery_list.keys())


def get_grocery_list():
    """
    returns the entire grocery list
    """
    return grocery_list


def exists(item):
    """
    returns True if item exists in the grocery list
    """
    return item in grocery_list


def get_details(item):
    """
    returns a dictionary of details for a singular grocery item
    """
    return grocery_list[item]


def get_types():
    """
    returns all unique grocery types in the grocery list
    """
    return list(set([item[GROC_TYPE] for item in grocery_list.values()]))


def add_item(item, details):
    """
    adds an item to the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if exists(item):
        raise ValueError(f'Item {item=} already exists in grocery list.')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    if details[GROC_TYPE] not in gtyp.get_groc_types():
        raise ValueError(f'Invalid {details[GROC_TYPE]=} in details. '
            + f'Must be one of: {gtyp.get_groc_types()}')
    if not isinstance(details[QUANTITY], int):
        raise TypeError(f'Wrong type for quantity: {type(details[QUANTITY])=}')
    grocery_list[item] = details


def remove_item(item):
    """
    removes an item from the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists:
        raise ValueError(f'Item {item=} not in grocery list.')
    del grocery_list[item]


def update_item(item, details):
    """
    updates an item in the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(details, dict):
        raise TypeError(f'Wrong type for details: {type(details)=}')
    for field in REQUIRED_FIELDS:
        if field not in details:
            raise ValueError(f'Required {field=} missing from details.')
    if details[GROC_TYPE] not in gtyp.get_groc_types():
        raise ValueError(f'Invalid {details[GROC_TYPE]=} in details. '
            + f'Must be one of: {gtyp.get_groc_types()}')
    if not isinstance(details[QUANTITY], int):
        raise TypeError(f'Wrong type for quantity: {type(details[QUANTITY])=}')
    grocery_list[item] = details


def update_quantity(item, quantity):
    """
    updates the quantity of an item in the grocery list
    """
    if not isinstance(item, str):
        raise TypeError(f'Wrong type for item: {type(item)=}')
    if not exists(item):
        raise ValueError(f'Item {item=} not in grocery list.')
    if not isinstance(quantity, int):
        raise TypeError(f'Wrong type for quantity: {type(quantity)=}')
    grocery_list[item][QUANTITY] = quantity


def main():
    print(get_items())
    print(get_details("item1"))
    print(get_types())


if __name__ == '__main__':
    main()
