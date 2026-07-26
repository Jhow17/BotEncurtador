Aqui está uma estrutura de `README.md` padronizada e profissional baseada na arquitetura do seu projeto e nos arquivos que você forneceu.

Este documento serve como a porta de entrada para quem visitar o seu repositório, explicando o que o projeto faz, as tecnologias utilizadas e como a estrutura foi dividida.

---

# BotEncurtador

Um ecossistema assíncrono completo que une um Bot do Telegram e uma API web para o encurtamento, armazenamento e redirecionamento de URLs. Desenvolvido com foco em alta performance utilizando rotinas não bloqueantes.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.13
* **Interface Conversacional:** `python-telegram-bot`
* **Servidor Web e API:** FastAPI / Uvicorn
* **Banco de Dados:** PostgreSQL
* **Driver de Conexão:** `psycopg` (Assíncrono)
* **Gerenciamento de Ambiente:** `python-dotenv`

## 📂 Arquitetura do Projeto

O sistema adota uma separação clara de responsabilidades para facilitar a manutenção e escalabilidade, dividindo-se nos seguintes arquivos:

* **`bot_interface.py`**: Ponto de entrada do bot do Telegram. Responsável por escutar as mensagens, validar os comandos do usuário e enviar as respostas.


* **`bot_services.py`**: Camada de regras de negócio. Contém a lógica matemática de conversão de IDs em códigos de encurtamento (hashes em Base64) e orquestra a comunicação entre a interface e o banco de dados.


* **`bot_repository.py`**: Camada de persistência. Isola toda a comunicação assíncrona com o PostgreSQL, executando as queries de inserção, deleção e busca utilizando cursores e tratamento de exceções.


* **`bot_server_redirect.py`**: Servidor web da aplicação construído em FastAPI. Recebe as requisições HTTP dos links curtos, realiza a busca da URL original integrada aos serviços do bot e redireciona o tráfego do usuário, tratando rotas inexistentes com erros 404.


* **`.gitignore`** e **`README.md`**: Arquivos de configuração de versionamento e documentação base do repositório.



## ⚙️ Instalação e Execução

Para rodar o ambiente de desenvolvimento localmente você deve clonar este repositório e criar um arquivo `.env` na raiz contendo os tokens do Telegram e as credenciais de acesso ao PostgreSQL. Com o ambiente virtual ativado, instale as bibliotecas necessárias através do pip e inicie a escuta de mensagens executando o arquivo da interface do bot no Python. Em um terminal paralelo, inicie o servidor web utilizando o comando de desenvolvimento nativo do FastAPI apontando para o arquivo de redirecionamento, o que fará a API escutar requisições locais e interagir ativamente com o banco de dados alimentado pelo bot.


