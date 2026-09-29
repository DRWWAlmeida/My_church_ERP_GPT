# My Church ERP

Aplicacao Flask em refatoracao, com foco atual na modularizacao de `category`, validacoes compartilhadas em `core` e persistencia em SQLite.

## Requisitos

- Python 3.14 ou compativel
- `pip`

## Estrutura Atual

```text
app/
  api/
    __init__.py
  core/
    database.py
    errors.py
    validators.py
  modules/
    category/
      repository.py
      routes.py
      schema.py
      services.py
  scripts/
    schema.py
  tests/
  config.py
  run.py
```

## Estado Atual

- A aplicacao usa app factory em `app.__init__.create_app`.
- Os blueprints registrados atualmente ficam em `app/api/__init__.py`.
- O modulo em refatoracao mais avancado e `category`.
- O banco continua sendo SQLite.
- A criacao do schema nao acontece no `create_app()`, mas e inicializada no fluxo de execucao de `app.run`.

## Configuracao

As configuracoes compartilhadas ficam em `app/config.py`.

Atualmente existem estas chaves:

- `BASE_DIR`
- `PROJECT_ROOT`
- `DEBUG`
- `TESTING`
- `DB_PATH`

O caminho atual do banco aponta para:

```text
app/db/igreja_erp.db
```

## Como Executar

1. Clone o repositorio.
2. Acesse a raiz do projeto.
3. Crie e ative um ambiente virtual.
4. Instale as dependencias.
5. Execute a aplicacao como modulo.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.run
```

Para desenvolvimento e execucao dos testes, instale:

```powershell
pip install -r requirements-dev.txt
python -m pytest
```

## Fluxo de Inicializacao

Ao executar:

```powershell
python -m app.run
```

acontece o seguinte:

1. O modulo `app.run` executa `create_schema()`.
2. `create_schema()` prepara as tabelas do banco antes de subir o servidor.
3. `app.run` chama `create_app()`.
4. `create_app()` instancia o `Flask` e carrega as configuracoes.
5. `register_blueprints(app)` registra os blueprints da API.
6. O servidor Flask sobe em modo debug.

Importante:

- O schema do banco continua fora do `create_app()`.
- A inicializacao do banco acontece no entrypoint `app.run`.
- Isso mantem o app factory limpo e deixa o fluxo operacional explicito no arquivo de execucao.

## Banco de Dados

O projeto usa SQLite.

- O arquivo do banco e criado pelo SQLite se nao existir.
- A conexao compartilhada fica em `app/core/database.py`.
- A criacao das tabelas fica em `app/scripts/schema.py`.

Tabelas previstas atualmente:

- `conta_corrente`
- `tipo_lancamento`
- `categoria`
- `lancamento`

## Endpoint Atual

O modulo `category` expõe atualmente:

- `GET /category`
- `POST /category`

O `GET /category` aceita os filtros opcionais `id` (inteiro positivo) e
`nome` (busca parcial). Consultas bem-sucedidas retornam HTTP 200.

O `POST /category` segue este fluxo:

1. A rota recebe o JSON.
2. O service chama o schema de validacao.
3. O repository grava no banco.
4. A rota devolve resposta JSON padronizada.

## Observacoes

- Rode o projeto com `python -m app.run` a partir da raiz do repositorio.
- O modo debug vem desativado. Para habilita-lo localmente, defina
  `FLASK_DEBUG=true`.
- O caminho do SQLite pode ser sobrescrito com a variavel `DATABASE_PATH`.
- Nao execute `python app/run.py` se quiser manter os imports por pacote funcionando corretamente.
- O `README` descreve o estado atual do codigo, nao o desenho final pretendido da arquitetura.
