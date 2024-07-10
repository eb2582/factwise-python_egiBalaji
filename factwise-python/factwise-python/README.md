###PROJECT - MY THOUGHT PROCESS
*KEY FEATURES-->
1. MANAGING USERS:
--> Add, Update, Delete and Retrieve user information (CURD Operations)
--> Each user will have attributes like user ID, name, email and role
2. MANAGING TEAMS:
--> Create, Update, Delete and Retrieve team information.
--> Assign users to teams and manage team members.
3. MANAGING TEAM BOARDS AND TASKS:
--> Create, update, delete, and retrieve boards.
-->Each board can have multiple tasks.
-->Tasks can be assigned to users, and have attributes like task ID, title, description, status, and due date.


PROJECT STRUCTURE:

factwise-python/
│
├── db/
│   ├── users.json
│   ├── teams.json
│   ├── boards.json
│   └── tasks.json
│
├── out/
│   └── output files or logs
│
├── src/
│   ├── base/
│   │   ├── __init__.py
│   │   ├── project_board_base.py
│   │   ├── team_base.py
│   │   └── user_base.py
│   │
│   ├── implementation/
│   │   ├── __init__.py
│   │   ├── project_board.py
│   │   ├── team.py
│   │   └── user.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── file_handler.py
│   │
│   └── main.py
│
├── README.md
├── requirements.txt
└── setup.py


