import json
from ..base.team_base import TeamBase
from ..utils.file_handler import read_json, write_json


class Team(TeamBase):
    def create_team(self, request: str) -> str:
        data = json.loads(request)
        teams = read_json('teams.json')

        if any(team['name'] == data['name'] for team in teams['teams']):
            raise ValueError("Team name must be unique")
        if len(data['name']) > 64:
            raise ValueError("Team name can be max 64 characters")
        if len(data['description']) > 128:
            raise ValueError("Description can be max 128 characters")

        team_id = len(teams['teams']) + 1
        teams['teams'].append({
            "id": team_id,
            "name": data['name'],
            "description": data['description'],
            "creation_time": data['creation_time'],
            "admin": data['admin'],
            "members": []
        })
        write_json('teams.json', teams)
        return json.dumps({"id": team_id})

    def list_teams(self) -> str:
        teams = read_json('teams.json')
        return json.dumps(teams['teams'])

    def describe_team(self, request: str) -> str:
        data = json.loads(request)
        teams = read_json('teams.json')

        team = next((team for team in teams['teams'] if team['id'] == data['id']), None)
        if not team:
            raise ValueError("Team not found")

        return json.dumps(team)

    def update_team(self, request: str) -> str:
        data = json.loads(request)
        teams = read_json('teams.json')

        team = next((team for team in teams['teams'] if team['id'] == data['id']), None)
        if not team:
            raise ValueError("Team not found")
        if any(other_team['name'] == data['team']['name'] for other_team in teams['teams'] if
               other_team['id'] != data['id']):
            raise ValueError("Team name must be unique")
        if len(data['team']['name']) > 64:
            raise ValueError("Team name can be max 64 characters")
        if len(data['team']['description']) > 128:
            raise ValueError("Description can be max 128 characters")

        team.update(data['team'])
        write_json('teams.json', teams)
        return json.dumps({"status": "Team updated successfully"})

    def add_users_to_team(self, request: str):
        data = json.loads(request)
        teams = read_json('teams.json')

        team = next((team for team in teams['teams'] if team['id'] == data['id']), None)
        if not team:
            raise ValueError("Team not found")
        if len(team['members']) + len(data['users']) > 50:
            raise ValueError("Cannot add more than 50 users to a team")

        team['members'].extend(data['users'])
        write_json('teams.json', teams)
        return json.dumps({"status": "Users added to team successfully"})

    def remove_users_from_team(self, request: str):
        data = json.loads(request)
        teams = read_json('teams.json')

        team = next((team for team in teams['teams'] if team['id'] == data['id']), None)
        if not team:
            raise ValueError("Team not found")

        team['members'] = [user for user in team['members'] if user not in data['users']]
        write_json('teams.json', teams)
        return json.dumps({"status": "Users removed from team successfully"})

    def list_team_users(self, request: str):
        data = json.loads(request)
        teams = read_json('teams.json')
        users = read_json('users.json')

        team = next((team for team in teams['teams'] if team['id'] == data['id']), None)
        if not team:
            raise ValueError("Team not found")

        team_users = [user for user in users['users'] if user['id'] in team['members']]
        return json.dumps(team_users)
