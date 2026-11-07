const API = "http://127.0.0.1:8000/api/reservas";

const formulario = document.querySelector("#form-reserva");
const mensagem = document.querySelector("#mensagem");
const lista = document.querySelector("#lista-reservas");


async function interpretarResposta(resposta) {
  const dados = await resposta.json();

  if (!resposta.ok) {
    const detalhe = Array.isArray(dados.detail)
      ? dados.detail.map((erro) => erro.msg).join("; ")
      : dados.detail;
    throw new Error(detalhe || "Não foi possível concluir a operação.");
  }

  return dados;
}


function criarCartao(reserva) {
  const artigo = document.createElement("article");
  artigo.innerHTML = `
    <h3>${reserva.laboratorio}</h3>
    <p><strong>Responsável:</strong> ${reserva.responsavel}</p>
    <p><strong>Data:</strong> ${reserva.data_reserva}</p>
    <p><strong>Turno:</strong> ${reserva.turno}</p>
    <p><strong>Alunos:</strong> ${reserva.quantidade_alunos}</p>
    <p><strong>Finalidade:</strong> ${reserva.finalidade}</p>
  `;
  return artigo;
}


async function carregarReservas() {
  try {
    const resposta = await fetch(API);
    const reservas = await interpretarResposta(resposta);

    lista.replaceChildren();
    reservas.forEach((reserva) => lista.appendChild(criarCartao(reserva)));
  } catch (erro) {
    mensagem.textContent = `Erro: ${erro.message}`;
    mensagem.className = "erro";
  }
}


formulario.addEventListener("submit", async (evento) => {
  evento.preventDefault();

  const dados = {
    laboratorio: document.querySelector("#laboratorio").value.trim(),
    responsavel: document.querySelector("#responsavel").value.trim(),
    data_reserva: document.querySelector("#data-reserva").value,
    turno: document.querySelector("#turno").value,
    finalidade: document.querySelector("#finalidade").value.trim(),
    // value é texto; Number converte o campo para o inteiro esperado pela API.
    quantidade_alunos: Number(
      document.querySelector("#quantidade-alunos").value
    ),
  };

  try {
    const resposta = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dados),
    });

    await interpretarResposta(resposta);
    mensagem.textContent = "Reserva criada com sucesso.";
    mensagem.className = "sucesso";
    formulario.reset();
    await carregarReservas();
  } catch (erro) {
    mensagem.textContent = `Erro: ${erro.message}`;
    mensagem.className = "erro";
  }
});


carregarReservas();
