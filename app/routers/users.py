from time import time, ctime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.dependencies import get_token_header

router = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

fake_base = {
    1: {"name": "Chuck Norris", "password": "roundhousekick", "role": "Karate Master"},
    2: {"name": "Mona Lisa", "password": "smile123", "role": "Art Enthusiast"},
    3: {"name": "Captain Crunch", "password": "cereallover", "role": "Cereal Connoisseur"},
    4: {"name": "Princess Sparkle", "password": "unicorn123", "role": "Unicorn Tamer"},
    5: {"name": "Scooby Doo", "password": "mysteryinc", "role": "Mystery Solver"},
    6: {"name": "Darth Vader", "password": "iamyourfather", "role": "Galactic Villain"}
}


# Background Task
def user_logs(user_id: int, user_name: str):
    with open("log.txt", mode="a") as log_file:
        content = f"{user_id}: {user_name} [{ctime(time())}]\n"
        log_file.write(content)


@router.get("/")
async def show_fake_base():
    return fake_base


@router.get("/{user_id}")
async def get_user(user_id: int, background_tasks: BackgroundTasks):
    if user_id not in fake_base:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    background_tasks.add_task(user_logs, user_id=user_id, user_name=fake_base[user_id]["name"])
    return {"User ID": user_id, "UserName": fake_base[user_id]["name"]}
