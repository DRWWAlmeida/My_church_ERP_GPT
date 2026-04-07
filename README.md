# My Church ERP

Aplicacao Flask em desenvolvimento para gerenciamento financeiro de igreja, com banco SQLite e criacao automatica do schema na inicializacao.

## Requisitos

- Python 3.14 ou compativel
- `pip`

## Estrutura Atual

```text
app/
  api/
    routes/
  db/
    connections.py
    schema.py
  models/
    __init__.py
  run.py
```

## Como Executar

1. Clone o repositorio.
2. Acesse a raiz do projeto.
3. Crie e ative um ambiente virtual.
4. Instale o Flask.
5. Execute a aplicacao como modulo.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install flask
python -m app.run
```

## URL Local

Com a aplicacao em execucao, acesse:

```text
http://127.0.0.1:5000/
```

## Banco de Dados

O projeto usa SQLite.

- Caminho atual do banco: `app/models/igreja_erp.db`
- O arquivo do banco e criado automaticamente pelo SQLite, se nao existir
- As tabelas sao criadas automaticamente no startup pela funcao `create_schema()`

Tabelas criadas atualmente:

- `conta_corrente`
- `tipo_lancamento`
- `categoria`
- `lancamento`

## Fluxo de Inicializacao

Ao executar:

```powershell
python -m app.run
```

acontece o seguinte:

1. O modulo `app.run` cria a aplicacao Flask.
2. A funcao `create_schema()` e chamada.
3. O SQLite cria o arquivo `.db` se ele ainda nao existir.
4. As tabelas sao criadas com `CREATE TABLE IF NOT EXISTS`.
5. O servidor Flask sobe em modo debug.

## Observacoes Importantes

- Rode o projeto com `python -m app.run` a partir da raiz do repositorio.
- Nao rode `python app/run.py` se quiser manter os imports por pacote funcionando corretamente.
- O arquivo `.db` esta no `.gitignore`, entao cada ambiente recria seu proprio banco local.
- Como ainda nao existe `requirements.txt`, a instalacao de dependencias esta manual.

## Estado Atual da Aplicacao

No momento, a rota principal retorna apenas um texto simples:

```text
Hell
```

Isso indica que a estrutura base do projeto esta funcionando, mas as rotas e regras de negocio ainda estao em desenvolvimento.

## Proximos Passos Recomendados

- Criar um `requirements.txt`
- Mover a inicializacao da aplicacao para um app factory no futuro
- Adicionar rotas reais para contas correntes, categorias e lancamentos
- Criar scripts de seed para popular dados iniciais
- Adicionar testes
