from flask import Blueprint, request, jsonify
from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return jsonify(search_users(request.args.to_dict()))

@bp.route("/all")
def show_all():
    return jsonify(USERS), 200

def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string

    Returns:
        a list of users that match the search parameters
    """
    id_param = args.get('id')
    name_param = args.get('name', '').lower()
    age_param = args.get('age')
    occupation_param = args.get('occupation', '').lower()

    matched_users = []
    for user in USERS:
        match_priority = 0

        if id_param and user['id'] == id_param:
            match_priority = 1
        elif name_param and name_param in user['name'].lower():
            match_priority = 2
        elif age_param:
            age = int(age_param)
            if age - 1 <= user['age'] <= age + 1:
                match_priority = 3
        elif occupation_param and occupation_param in user['occupation'].lower():
            match_priority = 4

        if match_priority:
            matched_users.append((match_priority, user))

    if not matched_users:
        return {"message": "No users found"}, 404

    # Sort by match_priority, then by id for consistent ordering within same priority
    matched_users.sort(key=lambda x: (x[0], x[1]['id']))

    # Extract sorted users from the tuple list
    sorted_users = [user for _, user in matched_users]

    return sorted_users
