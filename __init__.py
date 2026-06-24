from fastapi import FastAPI, APIRouter
from src.books.routes import api_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db


# Life-span function : to determine which code to run at the start of 
# our app and which code runs at the end of our app
@asynccontextmanager
# a co-routine that runs throughout the lifespan of our application 
async def life_span(app: FastAPI):
    print(f'Server is starting ...')
    
    # init_db is a coroutine (an async fn) so it needs to be called with await
    await init_db()  
    
    yield                         
    # the code on top runs at the start of app and code below runs at the end.
    
    print(f'Server has been stopped')



version = 'v1'


app = FastAPI(
    version = version,
    title = 'Bookly',
    description= "A Book inventory system"
)

app.include_router(api_router, prefix=f'/api/{version}/books', tags=['books'])
app.include_router(auth_router,prefix=f'/api/{version}/auth', tags = ['auth']   )


