from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi import Path
from time import sleep
from fastapi import Depends
from typing import Any
import sys, os
import models

from models import cursos, Curso

dir_atual = os.path.dirname(os.path.abspath("main.py"))
caminho_desejado = os.path.join(dir_atual, "models/curso")
sys.path.append(caminho_desejado)

app = FastAPI()
time = 1


async def conexao_db_fake():
    try:
        print("Conexao estabelecida")
        print(f"Aguarde {time}s")
        for x in range(1, time + 1):
            print(x)
            sleep(1)
        print("gerando os dados")
    except Exception as error:
        print(error)
    finally:
        sleep(1)
        print("Conexao finalizada")


mensagem_erro = "Curso nao encontrado na bd local"


@app.get(
    "/cursos",
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=list[models.Curso],
    description="Obtenha a lista contendo todos os cursos",
)
async def inictial_cursos(db: Any = Depends(conexao_db_fake)):
    return cursos


@app.get(
    "/cursos/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    description="Obter o curso conforme o ID",
)
async def cursos_id(
    id: int = Path(
        title="Id do curso",
        description="O valor numerico deve ser acima de zero",
        gt=0,
    )
):
    id = int(id)

    try:
        curso = models.cursos[id - 1]
        return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso nao encontrado"
        )


@app.post(
    "/cursos",
    status_code=status.HTTP_201_CREATED,
    description="Adicione um novo curso a lista",
    # response_model=models.Curso,
)
async def adicionar_curso(curso: Curso):
    try:
        if curso.id not in cursos:
            size = len(cursos) + 1
            cursos.append(curso)
            curso.id = size
            return curso
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Curso ja se encontra na base de dados",
        )


@app.put(
    "/curso/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    description="Atualize um curso já existente",
    response_model=Curso,
)
async def atualizar_curso(
    curso: models.Curso,
    id: int = Path(
        title="Id do curso",
        description="Informar o id do curso que deseja atualizar as informações",
        gt=0,
    ),
):
    if cursos[id] in cursos:
        cursos[id - 1] = curso
        curso.id = id
        return curso
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem_erro)


@app.delete(
    "/curso/{id}",
    status_code=status.HTTP_200_OK,
    description="Exclua um curso da lista",
)
async def deletar_curso(
    id: int = Path(
        title="Id do curso",
        description="Informar o id do curso que deseja excluir",
        gt=0,
    ),
):
    if cursos[id - 1] in cursos:
        del cursos[id - 1]
        return {
            "messagem": "Curso deletado com sucesso",
            "status": status.HTTP_204_NO_CONTENT,
        }
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem_erro)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
