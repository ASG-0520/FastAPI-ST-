from fastapi import APIRouter, Path, Query, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Annotated

from app.dependencies import get_token_header

router = APIRouter(
    prefix="/task",
    # tags=["Task"],
    dependencies=[Depends(get_token_header)]
)


class Task(BaseModel):
    name: str = "name"
    description: str = "description"
    detail: str | None = None
    status: bool = True  # True - in progress


# to_do_list
to_do_list = {}


# show ToDoList
@router.get("/todolist", tags=["Show todolist"])
async def show_todolist():
    return to_do_list


# Create task
@router.post("/{task_id}", tags=["Create task"])
async def post_task(task_id: Annotated[int, Path(description="Add task")], task: Task):
    if task_id in to_do_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This ID already exist")
    to_do_list[task_id] = task
    return to_do_list[task_id]


# get task via id
@router.get("/{task_id}", tags=["Get task"])
async def get_task_via_id(task_id: Annotated[int, Path(description="Get task")]):

    if task_id in to_do_list:
        return to_do_list[task_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")


# get task via name
@router.get("/", tags=["Get task"])
async def get_task_via_name(name: Annotated[str | None,
                            Query(description="Get task via query name", title="Name")] = None
                            ):
    for task_id in to_do_list:
        if to_do_list[task_id].name == name:
            return to_do_list[task_id]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")


# Update task via ID
@router.put("/{task_id}", tags=["Update task"])
async def update_task_via_id(task_id: Annotated[int, Path(description="Update task, used to receive data that should replace the existing data.")],
                             updated_task: Task
                             ):
    if task_id not in to_do_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")

    to_do_list[task_id] = updated_task
    return to_do_list[task_id]

# Update task via ID
# @router.put("/update-task/{task_id}")
# async def update_task_via_id(task_id: Annotated[int, Path(description="Update task via ID")],
#                              updated_task: Task
#                              ):
#     if task_id not in to_do_list:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found")
#
#     if updated_task.name:
#         to_do_list[task_id].name = updated_task.name
#
#     if updated_task.description:
#         print(to_do_list[task_id].description)
#         print(updated_task.description)
#         to_do_list[task_id].description = updated_task.description
#
#     if updated_task.status:
#         to_do_list[task_id].status = updated_task.status
#
#     return to_do_list[task_id]


# Update task

@router.patch("/{task_id}", response_model=Task, tags=["Update task"])
async def update_task_via_id(task_id: Annotated[int, Path(description="Update task, send only the data that you want to update")],
                             update_task: Task):
    if task_id not in to_do_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID not found")

    stored_task_model = to_do_list[task_id]  # object
    update_data = update_task.model_dump(exclude_unset=True)  # dict(excluding default values)
    updated_item = stored_task_model.copy(update=update_data)  # object
    to_do_list[task_id] = updated_item
    return updated_item


# delete task
@router.delete("/{task_id}", tags=["Delete task"])
async def delete_task_via_id(task_id: Annotated[int, Path(description="Delete task")]):
    if task_id not in to_do_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID notFound")
    del to_do_list[task_id]


# PUT используется для получения данных, которые должны заменить существующие данные.
# PATCH - операция по частичному обновлению данных - это означает, что вы можете отправлять только те данные,
# которые хотите обновить, оставляя остальные нетронутыми.
# https://fastapi.tiangolo.com/ru/tutorial/body-updates/


