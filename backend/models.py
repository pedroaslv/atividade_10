from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field


Turno = Literal["manha", "tarde", "noite"]


class ReservaEntrada(BaseModel):
    """Contrato do JSON recebido pelo endpoint POST."""

    laboratorio: str = Field(min_length=3, max_length=40)
    responsavel: str = Field(min_length=3, max_length=80)
    data_reserva: date
    turno: Turno
    finalidade: str = Field(min_length=5, max_length=200)
    # Evolução da aula: a quantidade precisa estar entre 1 e 40.
    quantidade_alunos: int = Field(ge=1, le=40)


class ReservaSaida(ReservaEntrada):
    """Contrato da resposta, incluindo campos gerados pela API."""

    id: int
    criada_em: datetime
