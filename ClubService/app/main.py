from fastapi import FastAPI, Depends, HTTPException, status, Response 
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select 
from sqlalchemy.exc import IntegrityError 
 
from .database import engine, SessionLocal 
from .models import Base, ClubDB, MembershipDB
from .schemas import (
    ClubCreate,
    ClubRead,
    ClubUpdate,
    MembershipCreate,
    MembershipRead,
    MembershipUpdate,
    MembershipReadWithClub,
)

app = FastAPI()

Base.metadata.create_all(bind=engine)

def commit_or_rollback(db: Session, error_msg: str):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=error_msg) #Duplicate info

def get_db(): 
    db = SessionLocal() 
    try: 
        yield db 
    finally: 
        db.close() 

# ------------- Health Check ---------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "clubs"}

#--------------- Club Endpoints ------------------

# GET: All Clubs, Clubs by ID
@app.get("/api/clubs", response_model=list[ClubRead]) 
def List_All_Clubs(db: Session = Depends(get_db)): 
    stmt = select(ClubDB).order_by(ClubDB.id) 
    return list(db.execute(stmt).scalars()) 
 
@app.get("/api/clubs/{club_id}", response_model=ClubRead) 
def Get_Club_By_ID(club_id: int, db: Session = Depends(get_db)): 
    club = db.get(ClubDB, club_id) 
    if not club: 
        raise HTTPException(status_code=404, detail="Club not found") 
    return club 

#POST a new club
@app.post("/api/clubs", response_model=ClubRead, status_code=status.HTTP_201_CREATED)
def create_club(payload: ClubCreate, db: Session = Depends(get_db)):
    club = ClubDB(**payload.model_dump())
    db.add(club)
    commit_or_rollback(db, "Club with this name or description may already exist")
    db.refresh(club)
    return club

#PATCH Club Info
@app.patch("/api/clubs/{club_id}", response_model=ClubRead)
def Update_Club_Info(club_id: int,payload: ClubUpdate,db: Session = Depends(get_db)):
    club = db.get(ClubDB, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(club, field, value)

    commit_or_rollback(db, "Club update failed, maybe duplicate name or description")
    db.refresh(club)
    return club

#PUT club information - updates all club attributes
@app.put("/api/clubs/{club_id}", response_model=ClubRead)
def Update_Full_Club_Info(club_id: int, payload: ClubCreate, db: Session = Depends(get_db)):
    club = db.get(ClubDB, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")
    
    for field_name, field_value in payload.model_dump().items():
        setattr(club, field_name, field_value)

    commit_or_rollback(db, "Club update failed, maybe duplicate name or descripion")
    return club


#DELETE Club 
@app.delete("/api/clubs/{club_id}", status_code=status.HTTP_204_NO_CONTENT)
def Delete_Club(club_id: int, db: Session = Depends(get_db)) -> Response:
    club = db.get(ClubDB, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found")

    db.delete(club)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# GET: All Memberships, Membserhips by ID
@app.get("/api/memberships", response_model=list[MembershipRead]) 
def List_All_Memberships(db: Session = Depends(get_db)): 
    stmt = select(MembershipDB).order_by(MembershipDB.id) 
    return list(db.execute(stmt).scalars()) 
 
@app.get("/api/memberships/{membership_id}", response_model=MembershipRead) 
def Get_Membership_By_ID(membership_id: int, db: Session = Depends(get_db)): 
    membership = db.get(MembershipDB, membership_id) 
    if not membership: 
        raise HTTPException(status_code=404, detail="Membership not found") 
    return membership 
