'''
Shopping list app

Given a menu list of meals for the week, gets what ingredients are needed, and
creates a shopping list. Given a target shop, it then splits up the list into
the aisles that will be needed in the shop.
'''

import json
from database import Database

database = Database('shopping_lists.json')
recipes = Database('recipes.json')


def get_sorted_list(shopping_list):
    return []


def get_shopping_list(menu):
    return []


def shopping_process(data):
    '''
    Given a dict "data" from the client, containing the information about the
    request (menu, potentially shopping list) and a request type ("looking-for")
    will then do the requested processing, and return the object.
    '''

    server_data = database[data['menukey']]
    extra = dict()
    extra['reply'] = 'ok'

    # data rec'd should overwrite anything in server
    for key in ['menu', 'list', 'sorted']:
        if key in data:
            server_data[key] = data[key]

    if 'looking-for' in data:
        wants = data['looking_for']
    else:
        wants = 'nothing'

    if wants == 'menu' and not server_data['menu']:
        server_data['menu'] = []
    if wants == 'list':
        if not server_data['menu']:
            extra['reply'] = 'not ok'
            extra['alert'] = 'Need to set a menu before a list can be made.'

        server_data['list'] = get_shopping_list(server_data['menu'])
    elif wants == 'sorted':
        if not server_data['list']:
            if not server_data['menu']:
                extra['reply'] = 'not ok'
                extra['alert'] = 'Need a menu before a list can be made, '
                extra['alert'] += 'and need a list before it can be sorted.'
            server_data['list'] = get_shopping_list(server_data['menu'])
        server_data['sorted'] = get_sorted_list(server_data['list'])

    reply = json.dumps({'menukey': data['menukey'], 'looking_for': wants, **extra, **server_data})

    database[data['menukey']] = server_data

    return reply
