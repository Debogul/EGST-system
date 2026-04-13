
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Skill(BaseModel):
    skill_name: str
    required_level: int
    current_level: int
    weight: int

class Employee(BaseModel):
    name: str
    role: str
    department: str
    skills: List[Skill]

def calculate_sgi(skills):
    return sum(max(0, s.required_level - s.current_level) * s.weight for s in skills)

def calculate_proficiency(skills):
    max_score = sum(s.required_level * s.weight for s in skills)
    current = sum(min(s.current_level, s.required_level) * s.weight for s in skills)
    return int((current / max_score) * 100) if max_score else 0

@app.post("/analyze")
def analyze(employee: Employee):
    sgi = calculate_sgi(employee.skills)
    proficiency = calculate_proficiency(employee.skills)

    status = "EXCEEDING" if proficiency >= 85 else "DEVELOPING" if proficiency >= 50 else "CRITICAL GAP"

    return {
        "name": employee.name,
        "sgi": sgi,
        "proficiency": proficiency,
        "status": status
    }
