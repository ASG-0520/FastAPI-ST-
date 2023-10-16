from fastapi import FastAPI
from app.routers import users, tasks

description = """
🔒 X-token = fake-super-secret-token 🔑 

## Tasks:

You can view **ToDoList, Create, Edit, and Delete** the tasks.

## Users:

You can view the entire user database and access users by their ID.
(When viewing a user, a log will be created in the BackgroundTasks.)

You will be able to:
* **Create users** (_not implemented_).
* **Edit users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "Update task",
        "description": "PUT используется для получения данных, которые должны заменить существующие данные.<br>"
                       "PATCH - операция по частичному обновлению данных - это означает, что вы можете отправлять только те данные,"
                       "которые хотите обновить, оставляя остальные нетронутыми.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/ru/tutorial/body-updates/",
        },
    },
]
app = FastAPI(
    openapi_tags=tags_metadata,
    title="FastAPI-ST-",
    description=description,
    summary="This app is created for educational purposes... 🚀",
    version="0.0.1",
    terms_of_service="https://fastapi.tiangolo.com",
)

app.include_router(users.router)
app.include_router(tasks.router)
