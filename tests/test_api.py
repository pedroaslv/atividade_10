import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))

import pytest
from fastapi.testclient import TestClient

import main

client = TestClient(main.app)

RESERVA = {
    "laboratorio": "Lab 02",
    "responsavel": "Ana Lima",
    "data_reserva": "2026-11-10",
    "turno": "tarde",
    "finalidade": "Aula de Banco de Dados",
    "quantidade_alunos": 25,
}


@pytest.fixture(autouse=True)
def limpar_reservas():
    main.reservas.clear()


def erro_do_campo(resposta, campo):
    return next(e for e in resposta.json()["detail"] if e["loc"] == ["body", campo])


# Parte C: contrato inicial

def test_post_valido_retorna_201_com_id_e_criada_em():
    resposta = client.post("/api/reservas", json=RESERVA)
    assert resposta.status_code == 201
    corpo = resposta.json()
    assert corpo["id"] == 1
    assert "criada_em" in corpo
    assert corpo["quantidade_alunos"] == 25


def test_get_lista_reserva_criada():
    client.post("/api/reservas", json=RESERVA)
    resposta = client.get("/api/reservas")
    assert resposta.status_code == 200
    assert len(resposta.json()) == 1


def test_turno_madrugada_retorna_422():
    resposta = client.post("/api/reservas", json={**RESERVA, "turno": "madrugada"})
    assert resposta.status_code == 422
    erro = erro_do_campo(resposta, "turno")
    assert erro["input"] == "madrugada"
    assert "'manha', 'tarde' or 'noite'" in erro["msg"]


# Parte E: quantidade_alunos

@pytest.mark.parametrize("quantidade", [25, 1, 40])
def test_quantidade_valida_retorna_201(quantidade):
    resposta = client.post("/api/reservas", json={**RESERVA, "quantidade_alunos": quantidade})
    assert resposta.status_code == 201
    assert resposta.json()["quantidade_alunos"] == quantidade


@pytest.mark.parametrize("quantidade", [0, 41])
def test_quantidade_fora_do_limite_retorna_422(quantidade):
    resposta = client.post("/api/reservas", json={**RESERVA, "quantidade_alunos": quantidade})
    assert resposta.status_code == 422
    assert erro_do_campo(resposta, "quantidade_alunos")["input"] == quantidade


def test_quantidade_ausente_retorna_422_field_required():
    sem_quantidade = {k: v for k, v in RESERVA.items() if k != "quantidade_alunos"}
    resposta = client.post("/api/reservas", json=sem_quantidade)
    assert resposta.status_code == 422
    assert erro_do_campo(resposta, "quantidade_alunos")["msg"] == "Field required"


# Pergunta de verificação: nome errado no JavaScript

def test_nome_quantidadeAlunos_nao_e_aceito():
    corpo = {k: v for k, v in RESERVA.items() if k != "quantidade_alunos"}
    corpo["quantidadeAlunos"] = 25
    resposta = client.post("/api/reservas", json=corpo)
    assert resposta.status_code == 422
    assert erro_do_campo(resposta, "quantidade_alunos")["msg"] == "Field required"
