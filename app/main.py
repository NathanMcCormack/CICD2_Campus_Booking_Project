from fastapi import FastAPI, HTTPException, status, Response
from .schemas import User

app = FastAPI()
users: list[User] = []  

@app.get("/api/users")
def get_users():
    return users

@app.get("/api/users/{user_id}") # get user by id
def get_user(user_id: int):
    for u in users: # search through list
        if u.user_id == user_id: # Check id matches
            return u # Return the found user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

@app.post("/api/users", status_code=status.HTTP_201_CREATED) # Create a new user (201)
def add_user(user: User): # Body validated as User
    if any(u.user_id == user.user_id for u in users): # Enforce unique user_id
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="user_id already exists") # Conflict on duplicate
    users.append(user) # Append to in-memory list
    return user

@app.put("/api/users/{user_id}") # Update existing user
def update_user(user_id: int, updated: User): 
    for i, u in enumerate(users): 
        if u.user_id == user_id: 
            users[i] = updated # Replace the stored object
            return users[i] # Return updated user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.user_id == user_id:
            users.pop(i)
 # 204 No Content should return an empty body
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    # If we didn’t find the user, return 404
    raise HTTPException(status_code=404, detail="User not found")