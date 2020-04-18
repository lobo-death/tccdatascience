# TCC Data Science e Machine Learning  - FIB Bauru 2020

### Bot para Telegram 

#### Tecnologias utilizadas
1. Telebot - framework para desenvolvimento de bots para o Telegram
2. AWS Polly - speech-to-text com suporte a SSML
3. Peewee - Micro ORM para persistência de dados
4. psycopg2 - framework para conexão ao Postgres
5. environs - library para leitura de variáveis de ambiente e/ou arquivos .env
6. boto3 - framework para integração com AWS

#### Requisitos para execução

1. Instalar pipenv - https://pipenv-fork.readthedocs.io/en/latest/
2. Instalar dependências - pipenv install
3. Criar conta AWS free - criar AWS Access Key e AWS Secret key, para o serviço Polly
4. Configurar as variáveis de ambiente:

        export TELEGRAM_TOKEN_API=
        export DOWNLOAD_PATH=
        export POLLY_ACCESS_KEY=
        export POLLY_SECRET_KEY=
        export POSTGRES_DATABASE=
        export POSTGRES_USER=
        export POSTGRES_PASSWORD=
        export POSTGRES_HOST=
        
    4.1. Ou definir essas variáveis no arquivo .env, no diretório scripts
    
5. Rodar o script scripts/models/models.py, para criação das tabelas no banco Postgres e inserção de dados de produtos
6. Rodar o script scripts/talhoBot.py

