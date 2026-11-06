# Evidências — F-001/T-001

Data: 29/10/2026. Estado: concluída. Escopo: preparar ambiente isolado, conferir fixtures e registrar baseline; nenhuma correção funcional solicitada nesta tarefa.

## Base e alvo

- Branch: `feature/api-transaction`.
- Base: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`.
- Alvo: estado local após preparação da `.venv` e alterações documentais desta tarefa, sem novo commit.
- `app/`, `requirements.txt`, `requirements-dev.txt`, `pytest.ini` e `.gitignore` permanecem iguais à base. Diretórios `.agents/`, `docs/`, `templates/` e AGENTS.md já estavam sem rastreamento antes desta execução e foram preservados.
- Critérios AC-001, AC-002, AC-003, AC-004 e AC-015 são apoiados por esta preparação; não estão integralmente aceitos só porque o baseline passou. O limite superior de ID de AC-004 segue pendente em T-002.

## Ambiente observado

Windows, Python 3.14.3, SQLite 3.50.4. Interpretador base funcional: `$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe`. O comando `python` encontrado no PATH aponta para WindowsApps; os comandos de execução usaram o caminho direto da `.venv`.

`sys.prefix != sys.base_prefix` retornou `True`. A `.venv` foi criada nesta tarefa, sem herdar pacotes globais. `git check-ignore .venv/pyvenv.cfg` confirmou que o ambiente está ignorado pelo Git.

Versões observadas com `pip freeze` (registro do ambiente, não novo lockfile):

```text
blinker==1.9.0
click==8.5.0
colorama==0.4.6
Flask==3.1.3
iniconfig==2.3.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.4
packaging==26.3
pluggy==1.7.0
Pygments==2.21.0
pytest==9.0.3
Werkzeug==3.1.9
```

Flask e pytest mantêm as versões dos manifestos. Dependências transitivas não estão fixadas no projeto; uma instalação futura pode resolvê-las de modo diferente. Nenhuma atualização geral dos manifestos foi feita.

## Comandos e resultados

Executados na raiz, em PowerShell:

```powershell
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" --version
& "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe" -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt --disable-pip-version-check
.\.venv\Scripts\python.exe -m pip freeze
.\.venv\Scripts\python.exe -m pip check
git check-ignore .venv/pyvenv.cfg
.\.venv\Scripts\python.exe -m pytest
```

| Verificação | Resultado |
|---|---|
| Interpretador e criação de ambiente | Python 3.14.3; criação concluída, código de saída 0 |
| Primeira instalação sob restrição de rede | Falhou com WinError 10013; não foi incompatibilidade de versão demonstrada |
| Repetição da instalação com acesso autorizado | Sucesso, código de saída 0; todas as dependências instaladas apenas na `.venv` |
| `pip check` | `No broken requirements found.`, código de saída 0 |
| `python -m pytest` pela `.venv` | 152 coletados; **152 passed in 2.39s**, código de saída 0 |

Distribuição observada da suíte:

| Arquivo | Testes aprovados |
|---|---:|
| `app/tests/test_categoria.py` | 26 |
| `app/tests/test_conta_corrente.py` | 20 |
| `app/tests/test_lancamento.py` | 74 |
| `app/tests/test_schema.py` | 3 |
| `app/tests/test_tipo_lancamento.py` | 20 |
| `app/tests/test_transaction_migration.py` | 9 |
| **Total** | **152** |

## Isolamento verificado

Antes da execução, foram inspecionados `conftest.py`, `test_schema.py`, `test_transaction_migration.py` e os pontos de acesso ao banco na suíte:

- A fixture de cliente configura `DATABASE` com arquivo `test_<uuid>.db`, prepara o schema no contexto da aplicação e remove o arquivo no encerramento.
- Os testes de consolidação usam `migration_<uuid>.db` e limpeza própria.
- Os testes de conversão substituem a conexão por banco em memória.
- Nenhum teste importa `app.run`; o servidor não foi iniciado.

SHA-256 de `app/db/igreja_erp.db` antes e depois da suíte permaneceu igual:

```text
3D02C0A098D0918B725C2507791B258AA6A373651326B98FEC87C2FB80C1977B
```

Após a suíte, o único arquivo `.db` listado em `app/db` era `igreja_erp.db`. Não houve inspeção de dados pessoais, migração do banco local ou alteração de dados reais. Migrações de teste ocorreram apenas nas bases isoladas previstas.

## Limitações e próximo trabalho

A suíte passou no código existente, sem alteração de testes. Isso não demonstra que todos os critérios do PRD estejam cobertos; o defeito de IDs grandes já identificado não faz parte dos testes atuais e segue para F-001/T-002. F-001/T-003 e o restante do MVP permanecem pendentes.

Não há comandos configurados de lint, tipos ou build nesta base; não foram inventados ou executados. A verificação foi proporcional à tarefa de ambiente: instalação, integridade de dependências, suíte completa e inspeção documental. Não houve revisão independente, commit, merge, push ou deploy.
