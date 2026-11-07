# Atividade 10 – Encontro 2
**Projeto:** Sistema de Reservas de Laboratórios
**Alunos:** Douglas Vignoli, Kaylan Lorete e Pedro Almeida

Missão: acompanhar uma requisição completa e acrescentar ao contrato o campo obrigatório `quantidade_alunos`, com valores de 1 a 40.

---

## Como executar
API (terminal 1):
```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```
Se o PowerShell bloquear a ativação da venv:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```
Front-end (terminal 2):
```powershell
cd frontend
python -m http.server 5500
```
- Interface: `http://localhost:5500`
- Swagger: `http://127.0.0.1:8000/docs`

---

## 1. Contrato preliminar do POST /api/reservas
| Parte | Valor |
|---|---|
| URL | `http://127.0.0.1:8000/api/reservas` |
| Método | `POST` |
| Corpo | JSON com os dados da reserva |
| Sucesso | `201 Created` com a reserva criada (inclui `id` e `criada_em`) |
| Falha de contrato | `422 Unprocessable Content` |

Campos do corpo (`ReservaEntrada` em `backend/models.py`):
| Campo | Tipo | Regra |
|---|---|---|
| `laboratorio` | texto | 3 a 40 caracteres |
| `responsavel` | texto | 3 a 80 caracteres |
| `data_reserva` | data | formato `AAAA-MM-DD` |
| `turno` | texto | `manha`, `tarde` ou `noite` |
| `finalidade` | texto | 5 a 200 caracteres |
| `quantidade_alunos` | inteiro | **1 a 40 (campo novo)** |

Exemplo de corpo enviado:
```json
{
  "laboratorio": "Lab 02",
  "responsavel": "Ana Lima",
  "data_reserva": "2026-11-10",
  "turno": "tarde",
  "finalidade": "Aula de Banco de Dados",
  "quantidade_alunos": 25
}
```

---

## 2. Código final em execução
As evidências desta entrega são **testes automatizados** (`tests/test_api.py`), que executam a API final e conferem os códigos HTTP e as respostas. Para rodar, a partir da raiz do projeto e com a venv ativada:
```powershell
python -m pytest tests -v
```
Resultado obtido (saída completa em [`resultado_testes.txt`](resultado_testes.txt)):
```
tests/test_api.py::test_post_valido_retorna_201_com_id_e_criada_em PASSED [ 10%]
tests/test_api.py::test_get_lista_reserva_criada PASSED                  [ 20%]
tests/test_api.py::test_turno_madrugada_retorna_422 PASSED               [ 30%]
tests/test_api.py::test_quantidade_valida_retorna_201[25] PASSED         [ 40%]
tests/test_api.py::test_quantidade_valida_retorna_201[1] PASSED          [ 50%]
tests/test_api.py::test_quantidade_valida_retorna_201[40] PASSED         [ 60%]
tests/test_api.py::test_quantidade_fora_do_limite_retorna_422[0] PASSED  [ 70%]
tests/test_api.py::test_quantidade_fora_do_limite_retorna_422[41] PASSED [ 80%]
tests/test_api.py::test_quantidade_ausente_retorna_422_field_required PASSED [ 90%]
tests/test_api.py::test_nome_quantidadeAlunos_nao_e_aceito PASSED        [100%]

======================== 10 passed, 1 warning in 0.44s ========================
```
O aviso (`warning`) é só uma mensagem de versão da biblioteca de testes e não afeta o resultado.

---

## 3. Evidência de uma resposta 201
Teste `test_post_valido_retorna_201_com_id_e_criada_em`: envia o `POST /api/reservas` com o corpo do item 1 e confere que a resposta é **201**, com `id`, `criada_em` e `quantidade_alunos`.

Resposta obtida da API:
```json
{
  "laboratorio": "Lab 02",
  "responsavel": "Ana Lima",
  "data_reserva": "2026-11-10",
  "turno": "tarde",
  "finalidade": "Aula de Banco de Dados",
  "quantidade_alunos": 25,
  "id": 1,
  "criada_em": "2026-11-07T11:03:28.196382"
}
```

---

## 4. Evidência de uma resposta 422
Teste `test_turno_madrugada_retorna_422`: envia `"turno": "madrugada"` e confere que a resposta é **422**, com:
- **loc:** `["body", "turno"]`
- **msg:** `Input should be 'manha', 'tarde' or 'noite'`
- **input:** `"madrugada"`

---

## 5. Arquivos alterados
| Arquivo | Alteração | Responsabilidade |
|---|---|---|
| `frontend/index.html` | novo campo `<input id="quantidade-alunos" type="number" min="1" max="40" required>` | coletar a quantidade no formulário |
| `frontend/app.js` | `quantidade_alunos: Number(...)` no objeto enviado | ler o campo, converter texto em número e mandar no JSON |
| `backend/models.py` | `quantidade_alunos: int = Field(ge=1, le=40)` em `ReservaEntrada` | validar o novo campo na API (422 se inválido) |
| `frontend/app.js` | `<p><strong>Alunos:</strong> ...</p>` no cartão | mostrar a quantidade na interface |
| `backend/requirements.txt` | `pytest` e `httpx` | dependências para rodar os testes |
| `tests/test_api.py` | arquivo novo | testes automatizados usados como evidência |

O `main.py` não precisou mudar: o `ReservaSaida` herda de `ReservaEntrada`, então a resposta já passa a trazer o campo novo.

Tirando o `requirements.txt` e os testes, o código final ficou igual ao `02_resultado_final` do pacote.

---

## Testes (Parte E)
| Caso | Entrada | Esperado | Teste | Resultado |
|---|---|---|---|---|
| sucesso | quantidade 25 | 201 | `test_quantidade_valida_retorna_201[25]` | ✅ 201 |
| limite inferior | quantidade 1 | 201 | `test_quantidade_valida_retorna_201[1]` | ✅ 201 |
| limite superior | quantidade 40 | 201 | `test_quantidade_valida_retorna_201[40]` | ✅ 201 |
| zero | quantidade 0 | 422 | `test_quantidade_fora_do_limite_retorna_422[0]` | ✅ 422 `Input should be greater than or equal to 1` |
| acima do limite | quantidade 41 | 422 | `test_quantidade_fora_do_limite_retorna_422[41]` | ✅ 422 `Input should be less than or equal to 40` |
| campo ausente | sem `quantidade_alunos` | 422 | `test_quantidade_ausente_retorna_422_field_required` | ✅ 422 `Field required` |

---

## Perguntas de verificação

**Por que a validação HTML não substitui o Pydantic?**
Porque a validação do HTML só existe no navegador e pode ser burlada (pelo Swagger, pelo F12 ou por qualquer outro cliente que chame a API direto). O Pydantic valida no servidor, então todo dado que chega é conferido.

**Por que JSON.stringify é necessário?**
O `fetch` envia texto no corpo da requisição. O `JSON.stringify` transforma o objeto JavaScript em texto JSON, que é o formato que o FastAPI espera ler.

**Onde o código 201 é definido?**
No `main.py`, no decorador da rota: `@app.post("/api/reservas", ..., status_code=status.HTTP_201_CREATED)`.

**O que acontece se o JavaScript enviar quantidadeAlunos?**
A API responde 422 `Field required` em `quantidade_alunos`, porque o nome não bate com o campo do modelo. O `quantidadeAlunos` é ignorado. Testamos e foi exatamente isso que aconteceu.

**Como provar que a requisição alcançou o servidor?**
Pela linha no terminal do Uvicorn, por exemplo `"POST /api/reservas HTTP/1.1" 201 Created`. O Network mostra que o navegador enviou, e o terminal mostra que a API recebeu.
