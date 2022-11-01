"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields, Namespace
import werkzeug.exceptions as wz

import db.groc_types as gtyp
import db.groc_lists as glst
import db.users as usr

app = Flask(__name__)
api = Api(app)

# string constants
GROC = 'groc'
USERS = 'users'
LIST = 'list'
DETAILS = 'details'
ADD = 'add'
DICT = 'dict'
TYPES = 'types'
MAIN_PAGE = '/main_page'
MAIN_PAGE_NM = 'Main Page'
GROC_TYPES = f'{GROC}_{TYPES}'
GROC_LIST = f'{GROC}_{LIST}'
USER_DICT_NM = f'{USERS}_{DICT}'
USER_LIST_NM = f'{USERS}_{LIST}'
GROC_TYPE_LIST_NM = f'{GROC_TYPES}_{LIST}'

# routes of endpoints with namespaces
GROC_LIST_ADD_W_NS = f'/{GROC_LIST}/{ADD}'
GROC_TYPE_LIST_W_NS = f'{GROC_TYPES}/{LIST}'
GROC_TYPE_DETAILS_W_NS = f'{GROC_TYPES}/{DETAILS}'
USER_LIST_W_NS = f'/{USERS}/{LIST}'
USER_DICT_W_NS = f'/{USERS}/{DICT}'
USER_ADD_W_NS = f'/{USERS}/{ADD}'

# name spaces
groc_types = Namespace(GROC_TYPES, 'Grocery Types')
api.add_namespace(groc_types)
groc_lists = Namespace(GROC_LIST, 'Grocery Lists')
api.add_namespace(groc_lists)
users = Namespace(USERS, 'Users')
api.add_namespace(users)
groceries = Namespace(GROC, 'Groceries')
api.add_namespace(groceries)
# note to self/team: focusing just on users namespace rn
# until we figure out the organization for groceries and such


# api namespace endpoints
@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = ''
        # sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(MAIN_PAGE)
class MainPage(Resource):
    """
    This will deliver our main app page
    """
    def get(self):
        """
        Gets the main homepage
        """
        return {'Title': MAIN_PAGE_NM,
                'Default': 0,
                'Choices': {
                    '1': {'text': 'List Grocery Types'},
                    }}


# grocery types namespace endpoints
@groc_types.route(f'/{LIST}')
class GrocTypeList(Resource):
    """
    This will get a list of grocery types.
    """
    def get(self):
        """
        Returns a list of grocery types.
        """
        # leads to "grocery_types_list" key error which is GROC_TYPE_LIST_NM
        return {GROC_TYPE_LIST_NM: gtyp.get_groc_types}


@groc_types.route(f'/{DETAILS}/<groc_type>')
class GroceryTypeDetails(Resource):
    """
    This will get the items by the type..
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, groc_type):
        gt = gtyp.get_groc_items_by_type(groc_type)
        if gt is not None:
            return {groc_type: gt}
        else:
            raise wz.NotFound(f'{groc_type} not found.')


# users namespace endpoints
@users.route(f'/{DICT}')
class UserDict(Resource):
    """
    This will get a dict of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {'Data': usr.get_users_dict(),
                'Type': 'Data',
                'Title': 'Active Users'}


@users.route(f'/{LIST}')
class UserList(Resource):
    """
    This will get a list of currrent users.
    """
    def get(self):
        """
        Returns a list of current users.
        """
        return {USER_LIST_NM: usr.get_usernames()}


USER_FIELDS = api.model('NewUser', {
    usr.USER_NAME: fields.String,
    usr.EMAIL: fields.String,
    usr.PASSWORD: fields.String,
})


@users.route(f'/{ADD}')
class AddUser(Resource):
    """
    Add a user.
    """
    @users.expect(USER_FIELDS)
    def post(self):
        """
        Add a user.
        """
        print(f'{request.json}')
        name = request.json[usr.USER_NAME]
        print("Name:", name)
        del request.json[usr.USER_NAME]
        usr.add_user(name, request.json)


# grocery lists namespace endpoints
class GrocListType(fields.Raw):
    """
    This is a custom data type for the grocery list to be used
    for checking the input type.
    """
    def output(self, key, obj, **kwargs):
        try:
            dct = getattr(obj, self.attribute)
        except AttributeError:
            return {}
        return dct or {}


GROC_FIELDS = api.model('GROC_LIST_ADD', {
    glst.USER_NAME: fields.String,
    glst.LIST_NAME: fields.String,
    glst.NUM_ITEMS: fields.Integer,
    glst.GROC_LIST: GrocListType,
})


@groc_lists.route(GROC_LIST_ADD_W_NS)
class AddGroceryList(Resource):
    """
    This will add a new grocery list to the database.
    """
    @api.expect(GROC_FIELDS)
    def post(self):
        """
        Add list to groc_list database.
        """
        print(f'{request.json=}')
        name = request.json[glst.USER_NAME]
        del request.json[glst.USER_NAME]
        glst.add_groc(name, request.json)
