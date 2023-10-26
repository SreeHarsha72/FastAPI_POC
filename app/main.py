from fastapi import FastAPI
from . import models #imports models from current directory
from .database import engine  #imports engine from .database file
from .routers import post,user, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#from .config import Settings

app=FastAPI()

origins = ["*"]


#this allows to make the communication smooth between client and server that are hoisted on different domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#below includes the routers in the post, user files to app()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


'''
#create the database tables from  models.py using the engine 
models.Base.metadata.create_all(bind=engine)'''


@app.get("/") #decorator: attaches the function to a path operation, it has http method
async def root():
    return {"message": "Hello World! Welcome to my API"}



