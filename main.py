from fastapi import FastAPI,Response,status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published : bool = True
    rating : Optional[int] = None

my_post = [{"titile":"title of post 1","content":"content of post 1", "id":1},{"title":"favorite foods","content":"i like pizza","id":2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p 

def find_index_post(id):
    for i,p in enumerate(my_post):
        if p['id'] == id:
            return i

@app.get("/")
def root():

    return {"message": "welcome to the api!!!"}


@app.get("/posts")
def get_post():
    return{"data": my_post}

@app.get("/posts/latest")
def get_latest_post():
    post1 = my_post[len(my_post)-1]
    return {"data": post1}

@app.get("/posts/{id}")
def get_post(id : int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id : {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message': f"post with id : {id} was not found "}
    print(post)
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0 , 1000000)
    my_post.append(post_dict)
    return {"data":post_dict}


@app.post("/posts")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content:{payload['content']}"}

# title str , content str , category , Boolean published 
@app.post("/posts")
def create_post(new_post:Post):
    post_dict = new_post.dict
    post_dict['id'] = randrange(0 , 1000000)
    my_post.append(post_dict)
    return {"data":post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # deleting the post 
    # find that index in that array which have a required id
    # my _post.pop()
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} doesnot exist")

    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int , post: Post):

    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} doesnot exist")
    

    post_dict = post.dict()
    post_dict['id'] = id
    my_post [index] = post_dict
    return {'data':post_dict}

