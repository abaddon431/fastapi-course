from fastapi import FastAPI, Response, status
from database import engine
from routers import posts, users
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return Response(status_code=status.HTTP_204_NO_CONTENT)