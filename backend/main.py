from datetime import datetime

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from models import ReservaEntrada, ReservaSaida


app = FastAPI(
    title="API de Reservas de Laboratórios",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

reservas: list[ReservaSaida] = []


@app.get("/api/status")
def consultar_status():
    return {"status": "online"}


@app.get("/api/reservas", response_model=list[ReservaSaida])
def listar_reservas():
    return reservas


@app.post(
    "/api/reservas",
    response_model=ReservaSaida,
    status_code=status.HTTP_201_CREATED,
)
def criar_reserva(dados: ReservaEntrada):
    reserva = ReservaSaida(
        id=len(reservas) + 1,
        criada_em=datetime.now(),
        **dados.model_dump(),
    )
    reservas.append(reserva)
    return reserva
