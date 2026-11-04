# My Church ERP

Aplicacao Flask em refatoracao, com foco atual na modularizacao de `category`, validacoes compartilhadas em `core` e persistencia em SQLite.

## Escopo planejado do MVP

Uma única igreja, com RBAC nos papéis Administrador, Presidente, Tesoureiro e Membro. Não inclui Master nem gestão de múltiplas igrejas. Identidade e autorização ainda são trabalho planejado; consulte o [PRD](docs/product/PRD.md) e a [matriz de acesso](docs/features/F-004-acesso-compartilhado/matriz-acesso.md).

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
    checking_account/
      repository.py
      routes.py
      schema.py
      services.py
    transaction_type/
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
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest
```

Esses comandos usam diretamente o ambiente virtual, sem depender da ativacao
do PowerShell ou do alias `python` do Windows. Se esse alias nao funcionar ao
criar a `.venv`, use o caminho de um interpretador Python instalado e validado
com `--version`, seguido de `-m venv .venv`.

Os testes criam bancos isolados e nao exigem executar `app.run`. O resultado
inicial verificado esta em [evidencias de F-001/T-001](docs/features/F-001-cadastros-confiaveis/evidencias.md).

## Fluxo de Inicializacao

Ao executar:

```powershell
python -m app.run
```

acontece o seguinte:

1. O modulo `app.run` cria a aplicacao com `create_app()`, carregando configuracoes e blueprints.
2. `main()` prepara o schema dentro do contexto dessa aplicacao.
3. Se a preparacao terminar, inicia o servidor com `app.config['DEBUG']`.
4. Falhas de preparacao interrompem a inicializacao antes do servidor.

Importante:

- O schema do banco continua fora do `create_app()`.
- Importar `app.run` apenas expoe `app`; nao conecta, migra ou inicia servidor.
- A inicializacao do banco acontece ao executar `main()` no entrypoint `app.run`.
- Isso mantem o app factory limpo e deixa o fluxo operacional explicito no arquivo de execucao.

Schema e API usam a mesma resolucao: no contexto Flask, `DATABASE` explicito
tem precedencia sobre `app.config['DB_PATH']`; fora dele, usa-se `app.config.DB_PATH`
do modulo de configuracao. `DATABASE_PATH` e lido do ambiente na importacao desse
modulo. Caminhos podem ser strings ou `Path`; valores vazios ou de tipo invalido
geram `ValueError`, sem fallback. Diretorios pais precisam existir. Caminhos
relativos continuam relativos ao diretorio de trabalho e foreign keys ficam ativas.

Ao usar WSGI com `app.run:app`, prepare o banco uma vez antes de iniciar os
processos, com a mesma configuracao de ambiente. Exemplo da etapa explicita
(pode migrar dados existentes; exige backup e parada conforme abaixo):

```python
from app.run import app
from app.scripts.schema import create_schema

with app.app_context():
    create_schema()
```

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

Nas consultas de categorias, contas correntes e tipos de lancamento, o filtro
`id` aceita valores de 1 a 9223372036854775807. Valores fora desse intervalo
retornam HTTP 400 com erro JSON; um ID valido sem registro retorna lista vazia.

O `POST /category` segue este fluxo:

1. A rota recebe o JSON.
2. O service chama o schema de validacao.
3. O repository grava no banco.
4. A rota devolve resposta JSON padronizada.

O modulo `checking_account` segue a mesma estrutura e expoe:

- `GET /checking-account`
- `POST /checking-account`

O `GET` aceita os filtros opcionais `id` e `nome`. O `POST` recebe:

```json
{
  "conta_corrente": "Banco Principal"
}
```

O modulo `transaction_type` expoe:

- `GET /transaction-type`
- `POST /transaction-type`

O `GET` aceita os filtros opcionais `id` e `nome`. O `POST` recebe:

```json
{
  "tipo_lancamento": "Entrada"
}
```

## Lancamentos

O modulo `app/modules/transaction` separa rotas, validacao, servicos e persistencia.

| Metodo | Endpoint | Comportamento |
| --- | --- | --- |
| POST | `/transaction` | Cria e retorna HTTP 201 |
| GET | `/transaction` | Lista paginada, HTTP 200 |
| GET | `/transaction/<id>` | Consulta individual, HTTP 200 |
| PUT | `/transaction/<id>` | Substitui todos os campos, HTTP 200 |
| PATCH | `/transaction/<id>` | Atualiza campos enviados, HTTP 200 |
| DELETE | `/transaction/<id>` | Exclusao definitiva, HTTP 204 sem corpo |

Corpo de POST e PUT (todos os campos obrigatorios):

```json
{
  "tipo_lancamento_id": 1,
  "categoria_id": 1,
  "conta_corrente_id": 1,
  "data": "2026-10-06",
  "valor_centavos": 12590,
  "descricao": "Oferta semanal"
}
```

`valor_centavos` e um inteiro positivo: 12590 representa R$ 125,90, inclusive
para saidas. O limite e 9223372036854775807. Numeros fracionarios, strings e
booleanos nao sao aceitos para valores ou IDs. A data deve ser valida em
`YYYY-MM-DD` e pode ser futura. A descricao e aparada e deve ter 3 a 255
caracteres. Os tres IDs devem existir. PATCH exige ao menos um campo; campos
desconhecidos sao rejeitados. Nao ha calculo de saldo nem transferencia entre
contas; o tipo e apenas a classificacao cadastrada.

Respostas de leitura e escrita usam `status`, `message` e `data`. O objeto em
`data` contem `id`, `data`, `valor_centavos`, `descricao` e as relacoes
`tipo_lancamento`, `categoria` e `conta_corrente`, cada uma com `id` e `nome`.
GET da colecao retorna `data` como lista e `pagination` com `page`, `per_page`,
`total` e `total_pages`. Paginas vazias retornam lista vazia com HTTP 200.

Filtros combinaveis: `tipo_lancamento_id`, `categoria_id`, `conta_corrente_id`,
`data_inicio`, `data_fim` (limites inclusivos) e `descricao` (trecho literal).
Ordenacao: data decrescente e ID decrescente. `page` inicia em 1; `per_page`
padrao 20, maximo 100. Parametros invalidos ou repetidos retornam HTTP 400.
Recursos inexistentes retornam 404; validacoes e relacionamentos invalidos,
400; falhas do banco, 500 com mensagem generica.

### Migracao de valores antigos

Ao inicializar pelo `python -m app.run`, o schema converte `valor` em
`valor_centavos`, preservando IDs, referencias e sequencia de IDs. A conversao
usa decimal com arredondamento de meio centavo para cima (1.005 vira 101).
O processo e transacional e idempotente. Valores invalidos, nao positivos,
fora do limite ou vinculos inexistentes interrompem a migracao com rollback.
Corrija os dados indicados antes de tentar novamente; nenhuma linha e descartada
para contornar erros. Faca backup do banco e pare os processos da aplicacao
antes de atualizar: versoes antigas que usam `valor` nao sao compativeis com o
schema convertido. Os testes usam bancos isolados; nao migram o banco local.

O [ensaio de recuperacao sintetica](docs/features/F-003-dados-e-migracao/recuperacao-sintetica.md)
documenta backup, restauracao apos commit e comparacoes de schema, registros e
sequencia. Ele nao valida recuperacao de dados reais nem define RPO/RTO.

### Fluxo de desenvolvimento

Crie features a partir da `develop`. Integre e teste nessa branch antes de
promover para `main`, conforme o fluxo acordado do projeto.

## Observacoes gerais

- Rode o projeto com `python -m app.run` a partir da raiz do repositorio.
- O modo debug vem desativado. Para habilita-lo localmente, defina
  `FLASK_DEBUG=true`.
- O caminho do SQLite pode ser sobrescrito com a variavel `DATABASE_PATH`.
- Nao execute `python app/run.py` se quiser manter os imports por pacote funcionando corretamente.
- O `README` descreve o estado atual do codigo, nao o desenho final pretendido da arquitetura.
