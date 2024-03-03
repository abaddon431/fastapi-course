from fastapi import FastAPI, Response, status
from database import engine
from routers import posts, users, auth, vote
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return Response(status_code=status.HTTP_204_NO_CONTENT)