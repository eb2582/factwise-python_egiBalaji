import json
from ..utils.file_handler import read_json, write_json

class UserBase:


    def create_user(self, request: str) -> str:
        data = json.loads(request)
        users = read_json('users.json')

        if any(user['name'] == data['name'] for user in users['users']):
            raise ValueError("User name must be unique")
        if len(data['name']) > 64:
            raise ValueError("Name can be max 64 characters")
        if len(data['display_name']) > 64:
            raise ValueError("Display name can be max 64 characters")

        user_id = len(users['users']) + 1
        users['users'].append({
            "id": user_id,
            "name": data['name'],
            "display_name": data['display_name'],
            "creation_time": data['creation_time']
        })
        write_json('users.json', users)
        return json.dumps({"id": user_id})

    def list_users(self) -> str:
        users = read_json('users.json')
        return json.dumps(users['users'])

    def describe_user(self, request: str) -> str:
        data = json.loads(request)
        users = read_json('users.json')

        user = next((user for user in users['users'] if user['id'] == data['id']), None)
        if not user:
            raise ValueError("User not found")

        return json.dumps(user)

    def update_user(self, request: str) -> str:
        data = json.loads(request)
        users = read_json('users.json')

        user = next((user for user in users['users'] if user['id'] == data['id']), None)
        if not user:
            raise ValueError("User not found")
        if len(data['user']['display_name']) > 128:
            raise ValueError("Display name can be max 128 characters")

        user.update(data['user'])
        write_json('users.json', users)
        return json.dumps({"status": "User updated successfully"})

    def get_user_teams(self, request: str) -> str:
        data = json.loads(request)
        teams = read_json('teams.json')

        user_teams = [team for team in teams['teams'] if data['id'] in team['members']]
        return json.dumps([{"name": team['name'], "description": team['description'], "creation_time": team['creation_time']} for team in user_teams])
