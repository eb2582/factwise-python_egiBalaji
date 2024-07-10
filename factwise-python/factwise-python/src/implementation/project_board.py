import json
import os

from ..base.project_board_base import ProjectBoardBase
from ..utils.file_handler import read_json, write_json


class ProjectBoard(ProjectBoardBase):
    def create_board(self, request: str) -> str:
        data = json.loads(request)
        boards = read_json('boards.json')

        if any(board['name'] == data['name'] for board in boards['boards']):
            raise ValueError("Board name must be unique for a team")
        if len(data['name']) > 64:
            raise ValueError("Board name can be max 64 characters")
        if len(data['description']) > 128:
            raise ValueError("Description can be max 128 characters")

        board_id = len(boards['boards']) + 1
        boards['boards'].append({
            "id": board_id,
            "name": data['name'],
            "description": data['description'],
            "team_id": data['team_id'],
            "creation_time": data['creation_time'],
            "status": "OPEN",
            "tasks": []
        })
        write_json('boards.json', boards)
        return json.dumps({"id": board_id})

    def close_board(self, request: str) -> str:
        data = json.loads(request)
        boards = read_json('boards.json')
        tasks = read_json('tasks.json')

        board = next((board for board in boards['boards'] if board['id'] == data['id']), None)
        if not board:
            raise ValueError("Board not found")
        if any(task['status'] != 'COMPLETE' for task in tasks['tasks'] if task['id'] in board['tasks']):
            raise ValueError("All tasks must be marked as COMPLETE before closing the board")

        board['status'] = "CLOSED"
        board['end_time'] = data.get('end_time')
        write_json('boards.json', boards)
        return json.dumps({"status": "Board closed successfully"})

    def add_task(self, request: str) -> str:
        data = json.loads(request)
        boards = read_json('boards.json')
        tasks = read_json('tasks.json')

        board = next((board for board in boards['boards'] if board['id'] == data['board_id']), None)
        if not board or board['status'] != 'OPEN':
            raise ValueError("Can only add task to an OPEN board")
        if any(task['title'] == data['title'] for task in tasks['tasks'] if task['id'] in board['tasks']):
            raise ValueError("Task title must be unique for a board")
        if len(data['title']) > 64:
            raise ValueError("Title name can be max 64 characters")
        if len(data['description']) > 128:
            raise ValueError("Description can be max 128 characters")

        task_id = len(tasks['tasks']) + 1
        tasks['tasks'].append({
            "id": task_id,
            "title": data['title'],
            "description": data['description'],
            "user_id": data['user_id'],
            "creation_time": data['creation_time'],
            "status": "OPEN"
        })
        board['tasks'].append(task_id)
        write_json('tasks.json', tasks)
        write_json('boards.json', boards)
        return json.dumps({"id": task_id})

    def update_task_status(self, request: str):
        data = json.loads(request)
        tasks = read_json('tasks.json')

        task = next((task for task in tasks['tasks'] if task['id'] == data['id']), None)
        if not task:
            raise ValueError("Task not found")

        task['status'] = data['status']
        write_json('tasks.json', tasks)
        return json.dumps({"status": "Task status updated successfully"})

    def list_boards(self, request: str) -> str:
        data = json.loads(request)
        boards = read_json('boards.json')

        open_boards = [board for board in boards['boards'] if
                       board['team_id'] == data['id'] and board['status'] == 'OPEN']
        return json.dumps([{"id": board['id'], "name": board['name']} for board in open_boards])

    def export_board(self, request: str) -> str:
        data = json.loads(request)
        boards = read_json('boards.json')
        tasks = read_json('tasks.json')

        board = next((board for board in boards['boards'] if board['id'] == data['id']), None)
        if not board:
            raise ValueError("Board not found")

        board_tasks = [task for task in tasks['tasks'] if task['id'] in board['tasks']]
        output = f"Board: {board['name']}\nDescription: {board['description']}\nStatus: {board['status']}\n\nTasks:\n"
        for task in board_tasks:
            output += f"Task: {task['title']}\nDescription: {task['description']}\nStatus: {task['status']}\n\n"

        out_file = f"board_{data['id']}.txt"
        out_path = os.path.join('out', out_file)
        with open(out_path, 'w') as file:
            file.write(output)

        return json.dumps({"out_file": out_file})
