from typing import Optional
from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int


cursos = [
    Curso(id=1, titulo="Programacao para leigos", aulas=25, horas=80),
    Curso(id=2, titulo="Algoritmos e logica de programacao", aulas=55, horas=110),
    Curso(id=3, titulo="Programa em Python", aulas=89, horas=105),
]
