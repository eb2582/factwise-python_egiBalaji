import json
from src.base.user_base import UserBase
from src.utils.file_handler import read_json, write_json


class User(UserBase):
    def create_user(self, request: str) -> str:
        data = json.loads(request)
        users = read_json('users.json')

        if any(user['email'] == data['email'] for user in users['users']):
            raise ValueError("Email must be unique")
        if len(data['name']) > 64:
            raise ValueError("Name can be max 64 characters")

        user_id = len(users['users']) + 1
        users['users'].append({
            "id": user_id,
            "name": data['name'],
            "email": data['email'],
            "creation_time": data['creation_time']
        })
        write_json('users.json', users)
        return json.dumps({"id": user_id})

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        users = read_json('users.json')

        user = next((user for user in users['users'] if user['id'] == data['id']), None)
        if not user:
            raise ValueError("User not found")

        return json.dumps(user)

    def list_users(self) -> str:
        users = read_json('users.json')
        return json.dumps(users['users'])
