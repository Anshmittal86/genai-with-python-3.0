from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    age: int
    gender: str

user_one = {
    "id": 10,
    "name": "John",
    "age": 18,
    "gender": "male"
}

first_user = User(**user_one)

print(first_user.name)