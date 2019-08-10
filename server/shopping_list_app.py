'''
Shopping list app

Given a menu list of meals for the week, gets what ingredients are needed, and
creates a shopping list. Given a target shop, it then splits up the list into
the aisles that will be needed in the shop.
'''

import json

def shopping_process(data):
    '''
    Given a dict "data" from the client, containing the information about the
    request (menu, potentially shopping list) and a request type ("looking-for")
    will then do the requested processing, and return the object.
    '''

    # TODO this
    reply = json.dumps({'reply': 'no', 'menukey': data['menukey']})
    print(reply)

    return reply
