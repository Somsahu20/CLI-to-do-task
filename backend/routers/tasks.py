from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import NoResultFound
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from ..database import get_db
from ..models import Tasks
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..schema import ReturnTask, CreateTask, UpdateTask
from typing import List

route = APIRouter()


@route.get('/task', response_model=List[ReturnTask])
def get_all_tasks(res: Response, status: bool = None, db : Session = Depends(get_db)):

    try:
        stmt = select(Tasks)
        
        if status is not None:
            stmt = stmt.where(Tasks.completed == status)

        result = db.execute(stmt).scalars().all()
        res.status_code = HTTP_200_OK
        return result

    except Exception as err:
        print("Error at get_all_tasks")
        print("Error is", err)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Error at get_all_tasks')

@route.post("/task", response_model=ReturnTask)
def add_task(res: Response, task: CreateTask, db: Session = Depends(get_db)):

    try:
        task_dict = task.model_dump()
        new_task = Tasks(**task_dict)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        res.status_code = HTTP_201_CREATED
        return new_task

    except Exception as err:
        db.rollback()
        print("Error in add_task")
        print("Error is", err)
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Couldn\'t add the task')

@route.patch('/task/{id}', response_model=ReturnTask)
def update_task(id: int, task: UpdateTask, db: Session = Depends(get_db)):

    try:
        check_q = select(Tasks).where(Tasks.id == id)
        og_task = db.execute(check_q).scalar_one() #! No need to make it a dictionary. sqlalachmey already is the bridge between the databse and the router
        task_update = task.model_dump(exclude_unset=True)

        for key, value in task_update.items():
            setattr(og_task, key, value)

        db.commit()
        db.refresh(og_task)
        
        return og_task
        

    except NoResultFound:
        print(f"The post with id {id} is not there in the database")
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Couldn\'t update the task beacuse id does not exist')
    except Exception as err:
        print("Error in update_task")
        print("Error is", err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Couldn\'t update the task')


@route.delete('/task/{id}', status_code=HTTP_204_NO_CONTENT)
def delete_task(id: int, db : Session = Depends(get_db)):
    try:
        check_q = select(Tasks).where(Tasks.id == id)
        task = db.execute(check_q).scalar_one_or_none()

        if task is None:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f"Task with id {id} does not exist")

        db.delete(task)
        db.commit()

        return None

    except Exception as err:
        db.rollback()
        print("Error in delete_task")
        print("Error is", err)
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail='Could not perform the delete operation on the task')