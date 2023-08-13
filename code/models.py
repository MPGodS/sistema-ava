from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Curso(Base):
    __tablename__ = "cursos_prova_final"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(255), nullable=False)
    carga_horaria = Column(Integer, nullable=False)
    qtd_exercicios = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    alunos = relationship("Aluno", back_populates="aluno_curso")


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    idade = Column(Integer, nullable=False)
    cpf = Column(Integer, nullable=False)
    id_curso = Column(Integer, ForeignKey(
        "cursos_prova_final.id"), nullable=False)

    aluno_curso = relationship("Curso", back_populates="alunos")
