# Pipeline ETL Santander com IA Generativa

Pipeline de **ETL (Extract, Transform, Load)** em Python que busca usuários em uma API REST, gera uma mensagem de marketing personalizada para cada um com a **API da OpenAI** e grava o resultado de volta na API.

Projeto desenvolvido no bootcamp de **Ciência de Dados da DIO em parceria com o Santander**, como parte do módulo de Python.

## Visão geral

```
CSV com UserIDs ──► GET /users/{id} ──► OpenAI (mensagem) ──► PUT /users/{id}
     Extract              Extract            Transform              Load
```

1. **Extract:** lê os `UserID` de um arquivo CSV com `pandas` e busca cada usuário na API com `requests`.
2. **Transform:** envia o nome do usuário a um modelo da OpenAI, que devolve uma mensagem curta sobre a importância de investir. A mensagem é adicionada à lista `news` do usuário.
3. **Load:** envia o usuário atualizado de volta para a API com `PUT`.

## Por que existe uma API própria neste repositório

O exercício usa como referência a [API da Santander Dev Week 2023](https://github.com/digitalinnovationone/santander-dev-week-2023-api), feita em Java com Spring Boot. Como o serviço hospedado dela saiu do ar, criei uma **API equivalente em Python** (FastAPI + SQLite), que roda dentro do próprio notebook. Ela reproduz o comportamento que importa para o projeto:

- o servidor gera o `id` automaticamente;
- o número do cartão é `UNIQUE` (cartão repetido retorna `409`);
- o usuário é criado informando apenas `name` e `card_number`.

> A estrutura dos dados é uma versão simplificada da API original (nome, cartão, saldo e `news`).

## Endpoints da API

| Método | Rota | O que faz | Respostas |
|---|---|---|---|
| `POST` | `/users` | Cria um usuário (`name`, `card_number`) | `201`, `409` se o cartão já existe |
| `GET` | `/users` | Lista todos os usuários | `200` |
| `GET` | `/users/{id}` | Busca um usuário | `200`, `404` |
| `POST` | `/users/{id}/news` | Adiciona uma notícia ao usuário | `200`, `404` |
| `PUT` | `/users/{id}` | Substitui a lista `news` do usuário | `200`, `404` |

Com o servidor ligado, a documentação interativa (Swagger) fica em `/docs`.

## Tecnologias

- Python
- pandas
- requests
- FastAPI e Uvicorn
- SQLite
- API da OpenAI (biblioteca `openai`)
- Google Colab

## Estrutura do repositório

```
.
├── api.py                         # API FastAPI + SQLite
├── BootcampCienciadeDados.ipynb   # Notebook com o pipeline (Extract, Transform, Load)
├── BootCamp_Ciencia_de_Dados.csv  # IDs dos usuários processados
└── README.md
```


## Como executar no Google Colab

1. Abra o notebook no Colab e envie para ele o `BootCamp_Ciencia_de_Dados.csv`.
2. Instale as dependências:
   ```python
   !pip install fastapi uvicorn openai -q
   ```
3. **Configure a chave da OpenAI** no cofre de *Secrets* do Colab (ícone de chave na barra lateral):
   - nome: `OPENAI_API_KEY`
   - ative o acesso ao notebook.
   ```python
   from google.colab import userdata
   open_api_key = userdata.get("OPENAI_API_KEY")
   ```
4. Crie o `api.py` com a célula `%%writefile api.py` (ou envie o arquivo) e ligue o servidor em segundo plano:
   ```python
   import subprocess, time

   subprocess.run(["pkill", "-f", "uvicorn"])
   time.sleep(2)
   servidor = subprocess.Popen(["python", "-m", "uvicorn", "api:app", "--port", "8000"])
   time.sleep(5)
   ```
5. Cadastre os usuários com `POST /users` (apenas uma vez por sessão, porque cartões repetidos retornam `409`).
6. Execute as células na ordem: **Extract**, **Transform** e **Load**.

Para confirmar o resultado, busque um usuário e veja a mensagem dentro de `news`:

```python
print(json.dumps(get_user(3), indent=2, ensure_ascii=False))
```

## Segurança

- **Nenhuma chave de API está neste repositório.** A chave fica no cofre de *Secrets* do Colab, fora do notebook.
- Antes de publicar um notebook, limpe as saídas das células (*Editar → Limpar todas as saídas*), pois mensagens de erro podem exibir trechos da chave.
- Os usuários e números de cartão usados são **fictícios**.

## O que aprendi

- Como funciona uma API REST: verbos HTTP (`GET`, `POST`, `PUT`), códigos de status (`200`, `201`, `404`, `409`) e JSON.
- Como consumir APIs com `requests` e como criar uma com FastAPI.
- Constraints de banco de dados (`UNIQUE`, id autoincrementado) e como a API as expõe.
- Como integrar um modelo de IA generativa a um pipeline de dados.
- Boas práticas com credenciais: segredos fora do código e do controle de versão.

## Autor

**João Vitor Oliveira Nogueira**
Estudante de Engenharia de Software
Linkedin: [www.linkedin.com/in/jvonogueira](www.linkedin.com/in/jvonogueira)

## Créditos

Projeto proposto pelo bootcamp de Ciência de Dados da [DIO](https://www.dio.me/) em parceria com o Santander. API de referência: [santander-dev-week-2023-api](https://github.com/digitalinnovationone/santander-dev-week-2023-api).
