from fastapi import FastAPI
import databases
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
user, password, host, port, database = (
    os.environ.get('user'),
    os.environ.get('password'),
    os.environ.get('host'),
    os.environ.get('port'),
    os.environ.get('database')
)

# Create a database URL
DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
# Create a database object
database = databases.Database(DATABASE_URL)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/dormitory")
async def get_dormitory(dorm_id: int):
    query = "SELECT * FROM dormitory WHERE id = :dorm_id"
    dormitory = await database.fetch_one(query=query, values={"dorm_id": dorm_id})
    return dormitory

@app.get("/machine")
async def get_machines(dorm_id: int,type: str):
    if type == "w":
        typeText = "washing_machine"
    elif type == "d":
        typeText = "drying_machine"
    else:
        return {"Error":"unexpected type"}
    query = f"SELECT * FROM {typeText} WHERE dormitory_id = :dorm_id"
    machines = await database.fetch_all(query=query, values={"dorm_id": dorm_id})
    print(query)
    return machines

# @app.get("/cycle")
# async def get_cycles(dorm_id: int,type: str,):



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)