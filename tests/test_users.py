import pytest 
from fastapi.testclient import TestClient 
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
 
from app.main import app, get_db 
from app.models import Base 
 
TEST_DB_URL = "sqlite:///./app.db" 
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False}) 
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False) 
Base.metadata.create_all(bind=engine) 
 
@pytest.fixture 
def client(): 
    def override_get_db(): 
        db = TestingSessionLocal() 
        try: 
            yield db 
        finally: 
            db.close() 
    app.dependency_overrides[get_db] = override_get_db 
    with TestClient(app) as c: 
        # hand the client to the test 
        yield c 
        # --- teardown happens when the 'with' block exits --- 
 
def test_create_user(client): 
    r = client.post("/api/users", json={"name":"Darragh","email":"Darragh@atu.ie","age":21,"student_id":"G00123456"}) 
    assert r.status_code == 201 


# import pytest 

# def user_payload(uid=1, name="Nathan", email="G00414780@atu.ie", age=21, sid="G00414780"): 
#     return {"user_id": uid, "name": name, "email": email, "age": age, "student_id": sid} 
 
# def test_create_user_ok(client): 
#     r = client.post("/api/users", json=user_payload()) 
#     assert r.status_code == 201 
#     data = r.json() 
#     assert data["user_id"] == 1 
#     assert data["name"] == "Nathan" 
 
# def test_duplicate_user_id_conflict(client): 
#     client.post("/api/users", json=user_payload(uid=2)) 
#     r = client.post("/api/users", json=user_payload(uid=2)) 
#     assert r.status_code == 409  # duplicate id -> conflict 
#     assert "exists" in r.json()["detail"].lower() 
 
# @pytest.mark.parametrize("bad_sid", ["BAD123", "s1234567", "S123", "S12345678"]) 
# def test_bad_student_id_422(client, bad_sid): 
#     r = client.post("/api/users", json=user_payload(uid=3, sid=bad_sid)) 
#     assert r.status_code == 422  # pydantic validation error 

 
# def test_get_user_404(client): 
#     r = client.get("/api/users/999") 
#     assert r.status_code == 404 
 
# def test_delete_then_404(client): 
#     client.post("/api/users", json=user_payload(uid=10)) 
#     r1 = client.delete("/api/users/10") 
#     assert r1.status_code == 204 
#     r2 = client.delete("/api/users/10") 
#     assert r2.status_code == 404 

# def test_put_then_404(client): 
#     client.post("/api/users", json=user_payload(uid=10)) #posting user with id 10 
#     r1 = client.put("/api/users/10", json=user_payload(name = "Nathan")) 
#     assert r1.status_code == 200 
#     r2 = client.put("/api/users/11", json=user_payload(uid = 11, name = "EOIN")) #Must format as a put, can't just have user id (like delete)
#     assert r2.status_code == 404 