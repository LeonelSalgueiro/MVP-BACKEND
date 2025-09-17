# MVP Backend - API de POST-IT

Este projeto é uma API simples para gerenciar Post-it, construída com Python, Flask e SQLite.

## Como instalar e rodar

### 1. Clone o repositório

```sh
git clone <URL-do-seu-repositório>
cd MVP-BACKEND
```

### 2. Crie um ambiente virtual

No Windows:

```sh
python -m venv venv
venv\Scripts\activate
```

No Linux/Mac:

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```sh
pip install -r requirements.txt
```

### 4. Execute a aplicação

```sh
python app.py
```

A API estará disponível em `http://localhost:5000`.

## Endpoints

- `POST /lembretes`  
  Cria um novo Post-it.  
  Parâmetros: `titulo`, `data`, `descricao` (form-data)

- `GET /lembretes`  
  Lista todos os Post-it.

- `GET /lembretes/<id>`  
  Consulta um Post-it pelo ID.

- `PUT /lembretes/<id>`  
  Edita um Post-it pelo ID.  
  Parâmetros: `titulo`, `data`, `descricao` (form-data)

- `DELETE /lembretes/<id>`  
  Exclui um Post-it pelo ID.

## Observações

- O banco de dados SQLite (`agenda.db`) será criado automaticamente na primeira execução.
- A documentação Swagger estará disponível em `/apidocs`.

---
Feito com [Flask](https://flask.palletsprojects.com/).
