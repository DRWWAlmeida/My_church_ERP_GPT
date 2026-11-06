# Evidências — F-001/T-003

Data: 30/10/2026. Estado: concluída. Base Git: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, branch `feature/api-transaction`; alvo: estado local após esta tarefa, sem novo commit. Alterações de T-001/T-002 e documentos não rastreados foram preservados.

## Alteração delimitada

Uma linha de produção alterada em `app/modules/category/repository.py`: retirada a interpolação do erro SQLite no fallback público de integridade. A mensagem continua indicando categoria duplicada ou inválida; status 400, campo e valor continuam no contrato. Os tratamentos específicos de UNIQUE/NOT NULL e os logs do servidor permanecem intactos.

Novo arquivo `app/tests/test_cadastros_contract.py`, com 24 casos parametrizados, cobre garantias compartilhadas. Usar arquivo comum evita triplicar o mesmo código de teste. As consultas, duplicidade e validações já verificadas pelos testes específicos foram reaproveitadas na execução direcionada.

## Critérios e evidências

| Critério | Verificação |
|---|---|
| AC-001 | Nomes aparados de 3 e 100 caracteres criados com 201 e envelope completo; ID retornado usado para consultar o registro persistido nos três cadastros |
| AC-002 | Rejeições de corpo inválido, campo ausente/nulo, não textual, branco, comprimento 2/101 e duplicidade sem alterar registro existente; testes anteriores mantêm verificação de JSON inválido |
| AC-003 | Testes existentes de consulta total, ordenação, ID, trecho, combinação e vazio; novos testes verificam combinação sem correspondência mesmo com ID existente |
| AC-004 (regressão de T-002) | Casos de limites e erros de ID incluídos nos 102 testes direcionados |
| AC-015, escopo dos cadastros | GET/POST com OperationalError e DatabaseError retornam 500 JSON genérico; erro de integridade real induzido em banco sintético retorna 400 sem detalhe interno nem gravação |

O erro de integridade foi induzido por trigger SQLite na base isolada da fixture, que executa RAISE(ABORT) com marcador sintético. Não houve mudança no schema de produção. Antes da correção, apenas categoria expunha esse marcador; os outros dois módulos já ocultavam o detalhe.

## Comandos e resultados

Executados na raiz, usando a `.venv` existente (Python 3.14.3, pytest 9.0.3):

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_cadastros_contract.py -q --tb=short
.\.venv\Scripts\python.exe -m pytest app/tests/test_categoria.py app/tests/test_conta_corrente.py app/tests/test_tipo_lancamento.py app/tests/test_cadastros_contract.py -q
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

| Momento | Resultado |
|---|---|
| Antes da correção, novos testes | **1 failed, 23 passed in 0.59s**; marcador `synthetic-private-constraint` exposto no corpo HTTP de categoria |
| Após correção, testes dos cadastros | **102 passed in 1.32s**, saída 0 |
| Após correção, suíte completa | **188 passed in 2.84s**, saída 0 |
| Diff/whitespace | Sem erro; avisos de conversão LF/CRLF da configuração local do Git |

SHA-256 do banco local permanece igual ao registrado nas tarefas anteriores: `3D02C0A098D0918B725C2507791B258AA6A373651326B98FEC87C2FB80C1977B`. Os testes usam bases isoladas; não foi iniciado servidor nem migrado o banco real.

## Limitações e conclusão

As três tarefas de F-001 estão concluídas tecnicamente, com evidências; isso não constitui revisão independente ou aceite do MVP. Não foi implementado handler universal para erros do roteador. Política de acesso/retencão dos logs continua pertencendo ao trabalho de segurança/operação. Não houve atualização de dependências, commit, merge, push ou deploy.

Próxima tarefa sugerida: F-002/T-001, ainda pendente. F-003/T-001 também é elegível por dependências, sem início automático.
