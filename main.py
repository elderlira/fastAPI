from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
import sys, os

dir_atual = os.path.dirname(os.path.abspath("main.py"))
caminho_pasta = os.path.join(dir_atual, "models")
sys.path.append(caminho_pasta)
import models

app = FastAPI()

cursos = {
    1: {"id": 1, "titulo": "Programacao para leigos", "aulas": 25, "horas": 80},
    2: {
        "id": 2,
        "titulo": "Algoritmos e logica de programacao",
        "aulas": 55,
        "horas": 110,
    },
}

mensagem_erro = "Curso nao encontrado na bd local"


@app.get("/cursos")
async def inictial_cursos():
    return cursos


@app.get("/cursos/{id}")
async def cursos_id(id: int):
    id = int(id)

    try:
        curso = cursos[id]
        return curso
    except KeyError:
        # maneira do curso
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado"
        )

    # uma maneira
    # if status != status.HTTP_200_OK:
    #     return "mensagem de erro"

    # uma maneira
    # if cursos.get(id) == None:
    #     return  'curso nao encontrado'


@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def adicionar_curso(curso: models.Curso):
    try:
        if curso.id not in cursos:
            size = len(cursos) + 1
            cursos[size] = curso
            curso.id = size
            return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Curso ja se encontra na base de dados",
        )


@app.put("/curso/{id}", status_code=status.HTTP_202_ACCEPTED)
async def atualizar_curso(id: int, curso: models.Curso):
    if id in cursos:
        cursos[id] = curso
        curso.id = id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem_erro)


@app.delete("/curso/{id}", status_code=status.HTTP_200_OK)
async def deletar_curso(id: int):
    if id in cursos:
        del cursos[id]
        return {
            "messagem": "Curso deletado com sucesso",
            "status": status.HTTP_204_NO_CONTENT,
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem_erro)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
