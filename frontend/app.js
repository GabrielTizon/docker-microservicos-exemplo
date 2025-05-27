const express = require('express');
const axios = require('axios');
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Rota para exibir o formulário
app.get('/form', (req, res) => {
  res.send(`
    <h2>Cadastro de Usuário</h2>
    <form action="/user" method="post">
      Nome: <input name="nome" /><br/>
      Idade: <input name="idade" type="number" /><br/>
      Cidade: <input name="cidade" /><br/>
      <button type="submit">Cadastrar</button>
    </form>
    <br/>
    <a href="/users">Ver lista de usuários</a>
  `);
});

// Rota para receber o form e enviar para o backend
app.post('/user', async (req, res) => {
  try {
    const { nome, idade, cidade } = req.body;
    // Aqui o endereço backend:5001 funciona no Docker Compose!
    await axios.post('http://backend:5001/user', { nome, idade, cidade });
    res.send(`Usuário cadastrado! <a href="/form">Voltar</a>`);
  } catch (err) {
    res.send(`Erro ao cadastrar: ${err.message} <a href="/form">Voltar</a>`);
  }
});

// Rota para exibir usuários cadastrados
app.get('/users', async (req, res) => {
  try {
    // Aqui também!
    const response = await axios.get('http://backend:5001/users');
    let lista = '<h2>Usuários Cadastrados</h2><ul>';
    response.data.forEach(u => {
      lista += `<li>${u.nome} (${u.idade}) - ${u.cidade}</li>`;
    });
    lista += '</ul><a href="/form">Voltar</a>';
    res.send(lista);
  } catch (err) {
    res.send('Erro ao buscar usuários');
  }
});

app.listen(3000, () => console.log("Frontend rodando na porta 3000"));
