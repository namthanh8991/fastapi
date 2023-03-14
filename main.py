from fastapi import FastAPI
import pandas as pd
from fastapi import HTTPException
from pydantic import BaseModel
app = FastAPI()

# tao bang du lieu pandas
data = {
    "id": [1, 2, 3],
    "name": ["nguyenvanA", "TranvanB", "NguyenvanC"],
    "description": ["description1", "description2", "description3"]
}

df = pd.DataFrame(data)

# tao cac duong dan (endpoints) va cac phuong thuc
@app.get("/items")
def read_items():
    return df.to_dict(orient="records")

@app.get("/items/{item_id}")
def read_item(item_id: int):
    item = df[df["id"] == item_id].to_dict(orient="records")
    if len(item) == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return item[0]

@app.post("/items")
def create_item(item: dict):
    global df
    new_item = pd.DataFrame.from_records([item])
    new_item["id"] = df["id"].max() + 1
    df = pd.concat([df, new_item])
    return {"message": "Item created successfully"}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: dict):
    if item_id not in df["id"].values:
        raise HTTPException(status_code=404, detail="Item not found")
    df.loc[df["id"] == item_id, ["name", "description"]] = [item["name"], item["description"]]
    return {"message": "Item updated successfully"}


# ///////////////////////////////////////////////////

class Person(BaseModel):
    name: str
    age: int
    profession: str

people = []

@app.get("/")
async def root():
    return {"message": "chuc ban ngay moi tot lanh"}

@app.post("/people/")
async def create_person(person: Person):
    people.append(person)
    return {"message": "Person created successfully"}

@app.get("/people/")
async def read_people():
    return people

@app.get("/people/{person_id}")
async def read_person(person_id: int):
    return people[person_id - 1]

@app.put("/people/{person_id}")
async def update_person(person_id: int, person: Person):
    people[person_id - 1] = person
    return {"message": f"Person {person_id} updated successfully"}

@app.delete("/people/{person_id}")
async def delete_person(person_id: int):
    people.pop(person_id - 1)
    return {"message": f"Person {person_id} deleted successfully"}

# @app.get("/people/stats")
# async def get_people_stats():
#     df = pd.DataFrame([p.dict() for p in people])
#     age_mean = np.mean(df["age"])
#     age_std = np.std(df["age"])
#     profession_counts = df["profession"].value_counts().to_dict()
#     return {
#         "age_mean": age_mean,
#         "age_std": age_std,
#         "profession_counts": profession_counts
#     }

