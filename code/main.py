from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from models import Curso, Aluno
from database import engine, Base, get_db
from repositories import CursoRepository, AlunoRepository
from schemas import CursoRequest, CursoResponse, AlunoRequest, AlunoResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/api/cursos", response_model=CursoResponse, status_code=status.HTTP_201_CREATED)
def create(request: CursoRequest, db: Session = Depends(get_db)):
    curso = CursoRepository.save(db, Curso(**request.dict()))
    return CursoResponse.from_orm(curso)


@app.get("/api/cursos", response_model=list[CursoResponse])
def find_all(db: Session = Depends(get_db)):
    cursos = CursoRepository.find_all(db)
    return [CursoResponse.from_orm(curso) for curso in cursos]


@app.get("/api/cursos/{curso_id}", response_model=CursoResponse)
def read_item(curso_id: int, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, curso_id)
    if curso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
    else:
        return CursoResponse.from_orm(curso)


@app.delete("/api/cursos/{curso_id}", response_model=CursoResponse)
def delete_item(curso_id: int, db: Session = Depends(get_db)):
    curso = CursoRepository.find_by_id(db, curso_id)

    CursoRepository.delete_by_id(db, curso_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/api/cursos/{curso_id}", response_model=CursoResponse)
def update_item(curso_id: int, request: CursoRequest, db: Session = Depends(get_db)):
    existe_curso = CursoRepository.exists_by_id(db, curso_id)
    if existe_curso is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    curso = CursoRepository.save(db, Curso(**request.dict(), id=curso_id))
    return CursoResponse.from_orm(curso)


# CRUD alunos

@app.post("/api/alunos", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def create_aluno(request: AlunoRequest, db: Session = Depends(get_db)):
    aluno = AlunoRepository.save(db, Aluno(**request.dict()))
    return AlunoResponse.from_orm(aluno)


@app.get("/api/alunos", response_model=list[AlunoResponse])
def find_all_alunos(db: Session = Depends(get_db)):
    alunos = AlunoRepository.find_all(db)
    return [AlunoResponse.from_orm(aluno) for aluno in alunos]


@app.get("/api/alunos/{aluno_id}", response_model=AlunoResponse)
def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, aluno_id)
    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")
    else:
        return AlunoResponse.from_orm(aluno)


@app.delete("/api/alunos/{aluno_id}", response_model=AlunoResponse)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = AlunoRepository.find_by_id(db, aluno_id)

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    if aluno.aluno_curso is not None:
        curso = CursoRepository.find_by_id(db, aluno.id_curso)
        if curso and curso.active:
            raise HTTPException(
                status_code=status.HTTP_400_NOT_FOUND, detail="Nao foi possivel excluir o aluno, pois ele esta vinculado a um curso ativo.")

    AlunoRepository.delete_by_id(db, aluno_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/api/alunos/{aluno_id}", response_model=AlunoResponse)
def update_aluno(aluno_id: int, request: AlunoRequest, db: Session = Depends(get_db)):
    existe_aluno = AlunoRepository.exists_by_id(db, aluno_id)
    if existe_aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado")

    aluno = AlunoRepository.save(db, Aluno(**request.dict(), id=aluno_id))
    return AlunoResponse.from_orm(aluno)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Ambiente Virtual de Aprendizagem",
        version="1.0.0",
        summary="Alunos EAD",
        description="Sistema de Ambiente Virtual de Aprendizagem para auxiliar alunos 100% EAD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
