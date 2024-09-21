from fastapi import FastAPI, HTTPException, Depends
from fastapi.routing import APIRoute
from sqlalchemy import ARRAY, Column, String
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional
from datetime import date, datetime
import os
from openai import OpenAI
from sqlalchemy import func

# Database setup
password = "UszjTuqY85uFhh_"
user = "postgres.wwlyuwpshpbjbmnjnzhf"
host = "aws-0-ap-southeast-1.pooler.supabase.com"
port = "6543"
dbname = "postgres"

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine = create_engine(DATABASE_URL)

# Models


class PersonBase(SQLModel):
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    profession: str = Field(index=True)
    location: str = Field(index=True)
    skills: List[str] = Field(sa_column=Column(ARRAY(String)))
    years_of_experience: Optional[int] = Field(default=None)
    education: Optional[str] = Field(default=None)
    bio: Optional[str] = Field(default=None)
    linkedin_profile: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    availability: Optional[str] = Field(default=None)
    hourly_rate: Optional[float] = Field(default=None)
    last_active: Optional[date] = Field(default=None)


class Person(PersonBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: date = Field(default_factory=date.today)
    updated_at: date = Field(default_factory=date.today)


class SearchQuery(SQLModel):
    query: str


class SearchResult(SQLModel):
    results: List[Person]


# FastAPI app
app = FastAPI()


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name  # in this case, 'read_items'


# Dependency


def get_session():
    with Session(engine) as session:
        yield session

# API endpoints


@app.post("/api/search", response_model=SearchResult)
async def search(query: SearchQuery, session: Session = Depends(get_session)):

    # Initialize OpenAI client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Get all unique skills from the database
    all_skills = session.query(func.unnest(Person.skills)).distinct().all()
    all_skills = [skill[0] for skill in all_skills]  # Flatten the result

    # Use OpenAI to find relevant skills
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that identifies relevant skills based on a search query."},
            {"role": "user", "content": f"Given the search query '{query.query}' and the following list of skills: {
                ', '.join(all_skills)}, what are the most relevant skills? Return only a Python list of strings."}
        ]
    )

    # Extract relevant skills from the OpenAI response
    relevant_skills = eval(response.choices[0].message.content)

    # Use the relevant skills to filter the database query
    results = session.exec(
        select(Person).where(Person.skills.overlap(relevant_skills)).limit(10)
    ).all()
    return SearchResult(results=results)


@app.get("/api/person/{person_id}", response_model=Person)
async def get_person(person_id: int, session: Session = Depends(get_session)):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person


@app.post("/api/person", response_model=Person)
async def create_person(person: Person, session: Session = Depends(get_session)):
    db_person = Person.model_validate(person)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person


@app.put("/api/person/{person_id}", response_model=Person)
async def update_person(person_id: int, person: Person, session: Session = Depends(get_session)):
    db_person = session.get(Person, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="Person not found")
    person_data = person.dict(exclude_unset=True)
    for key, value in person_data.items():
        setattr(db_person, key, value)
    session.add(db_person)
    session.commit()
    session.refresh(db_person)
    return db_person


@app.delete("/api/person/{person_id}")
async def delete_person(person_id: int, session: Session = Depends(get_session)):
    person = session.get(Person, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    session.delete(person)
    session.commit()
    return {"message": f"Person with id {person_id} has been deleted"}


@app.get("/api/suggestions")
async def get_suggestions(partial_query: str):
    # TODO: Implement suggestion logic
    # This is a placeholder implementation
    suggestions = ["marketing professional",
                   "freelance designer", "software engineer"]
    return {"suggestions": suggestions}


@app.get("/api/recent-searches")
async def get_recent_searches():
    # TODO: Implement recent searches retrieval
    # This is a placeholder implementation
    recent_searches = ["marketing professional in New York",
                       "freelance designer in San Francisco"]
    return {"recent_searches": recent_searches}

# Create tables
SQLModel.metadata.create_all(engine)
use_route_names_as_operation_ids(app)
