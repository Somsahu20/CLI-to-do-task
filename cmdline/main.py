# import sys
# from pathlib import Path

# # Add parent directory to Python path
# parent_dir = Path(__file__).parent.parent
# sys.path.insert(0, str(parent_dir))

import typer as ty
from typing import Optional
import time
from rich.progress import track
import random
import requests
URL = "http://127.0.0.1:8000"

app = ty.Typer()

# @app.command()
# def intro(name: str, iq: int, display: bool = True):
#     print(f'Hello {name}')
#     if display:
#         print(f'Your iq is {iq}')


# @app.command()
# def outro(name: str):
#     print(f'Goodbye {name}')
def animation():
    total = 0
    for value in track(range(100), description="Processing"):
        time.sleep(0.001)
        total += random.randint(0, 4)

@app.command()
def add_task(title: str, content: Optional[str | None] = None):
    animation()
    # print("Title:", title)
    # if content is not None:
    #     print("Content:", content)
    task_dict = {"title": title}

    if content is not None:
        task_dict["content"] = content

    web = URL + '/task'
    response = requests.post(web, json=task_dict)

    if response.status_code == 201:
        print('Successfully created the task')
        data = response.json()
        print(f"The id of the task is {data.get("id")}")
    else:
        print(f"Whoops, something went wrong. The status code is {response.status_code}")
        print(f"Server said {response.text}")

    

@app.command()
def get_all_task(completed: Optional[bool | None] = None):

    animation()
    web = URL + '/task'
    params = {}
    if completed is not None:
        params.update({"status": completed})
    # if completed is not None:
    #     web = web + '?status=' + str(completed) #! never do it manually. Use params of requests
    
    
    response = requests.get(web, params=params)

    if response.status_code == 200:
        data = response.json()

        for datum in data:
            print('------------------------------------------------------------------------')
            for key, value in datum.items():
                print(f"{key}: {value}")
            print('------------------------------------------------------------------------')

    else:
        print(f"Whoops, something went wrong. The status code is {response.status_code}")
        print(f"Server said {response.text}")
            
    

@app.command()
def delete_task(id :int):
    animation()

    web = URL + f'/task/{id}'
    response = requests.delete(web)

    if response.status_code == 204:
        print(f'Task with id {id} is deleted')
    else:
        print(f"Whoops, something went wrong. The status code is {response.status_code}")
        print(f"Server said {response.text}")

@app.command()
def update_task(id: int,
                title: str | None = None, 
                content: str | None = None,
                completed: bool | None = None):
    animation()

    print(f"Task with id {id} will be updated")
    payload = {}

    if title is not None:
        payload.update({"title": title})
    if content is not None:
        payload.update({"content": content})
    if completed is not None:
        payload.update({"completed": completed})

    web = URL + f'/task/{id}'
    response = requests.patch(web, json=payload)

    if response.status_code == 200:
        print("The task is updated")
        data = response.json()
        print('------------------------------------------------------------------------')
        for key, value in data.items():
            print(f"{key}: {value}")
        print('------------------------------------------------------------------------')
    else:
        print(f"Whoops, something went wrong. The status code is {response.status_code}")
        print(f"Server said {response.text}")




if __name__ == "__main__":
    app()