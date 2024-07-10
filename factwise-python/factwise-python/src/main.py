import json
from implementation.user import User
from implementation.team import Team
from implementation.project_board import ProjectBoard

def main():
    user_api = User()
    team_api = Team()
    board_api = ProjectBoard()

    # Example usage:
    # Creating a user
    user_request = '{"name": "EGI Balaji", "display_name": "EGI", "creation_time": "2024-07-10"}'
    user_response = user_api.create_user(user_request)
    print("Created user:", user_response)

    # Creating a team
    team_request = '{"name": "Development Team", "description": "Handles all development tasks.", "admin": 1, "creation_time": "2024-07-10"}'
    team_response = team_api.create_team(team_request)
    print("Created team:", team_response)

    # Creating a board
    board_request = '{"name": "Project Alpha", "description": "Project Alpha Tasks", "team_id": 1, "creation_time": "2024-07-10T10:00:00Z"}'
    board_response = board_api.create_board(board_request)
    print("Created board:", board_response)

    # Listing all users
    all_users = user_api.list_users()
    print("All users:", all_users)

    # Describing a user
    describe_user_request = '{"id": 1}'
    user_description = user_api.describe_user(describe_user_request)
    print("User description:", user_description)

    # Listing all teams
    all_teams = team_api.list_teams()
    print("All teams:", all_teams)

    # Describing a team
    describe_team_request = '{"id": 1}'
    team_description = team_api.describe_team(describe_team_request)
    print("Team description:", team_description)

    # Listing all boards
    list_boards_request = '{"id": 1}'
    all_boards = board_api.list_boards(list_boards_request)
    print("All boards for team id 1:", all_boards)

if __name__ == "__main__":
    main()
