# pipeline-openweather

Pipeline ETL em Python que extrai dados climáticos da [OpenWeather API](https://openweathermap.org/api), transforma e normaliza as informações com Pandas, e carrega os dados em um banco MySQL via SQLAlchemy.

## Como funciona

O pipeline segue o fluxo clássico **Extract → Transform → Load**, orquestrado em `main.py`:

```
main.py
  ├── extract()    → busca dados da API OpenWeather e salva o JSON bruto em data/raw
  ├── transform()  → lê o JSON mais recente, normaliza e salva em data/processed
  └── load()       → cria as tabelas (se necessário) e insere os dados no MySQL
```

Cada etapa é logada em `logs/pipeline-etl.log` e no console, com timestamp.

## Pré-requisitos

- Python 3.10+
- Docker e Docker Compose (para o banco MySQL)
- Uma chave de API gratuita da [OpenWeather](https://openweathermap.org/api)

## Instalação

1. Clone o repositório:

```bash
   git clone https://github.com/MIguelYohan/pipeline-openweather.git
   cd pipeline-openweather
```

2. Crie e ative um ambiente virtual:

```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Linux/Mac
```

3. Instale as dependências:

```bash
   pip install -r requirements.txt
```

## Configuração do .env

1. Crie um arquivo .env na raiz do projeto:

```bash
   cp .env.example .env
```

2. Depois, preencha os valores:

```env
   API_KEY=sua_chave_openweather

   # Endereço e porta do banco (usado só pelo Python, não é lido pelo container)
   DB_HOST=localhost
   DB_PORT=3306

   # Usuário com acesso restrito ao banco DB_NAME — usado pela aplicação no dia a dia
   DB_USER=seu_usuario
   DB_USER_PASSWORD=sua_senha
   DB_NAME=pipeline_clima

   # Senha do usuário root — acesso total ao servidor, só para uso administrativo manual
   DB_ROOT_PASSWORD=senha_root
```

## Execução

1. Suba o banco de dados (certifique-se de mudar as variáveis de ambiente antes):

```bash
   docker-compose up
```

2. Execute a pipeline por completo:

```bash
   python main.py
```

## Documentação

- [Visão geral da pipeline](docs/overview.png)
