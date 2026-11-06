# Evidências — F-002/T-003

Data: 03/11/2026. Estado: concluída. Base Git: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo: diff local desta tarefa em `app/tests/test_lancamento.py` e documentos de acompanhamento. Alterações de tarefas anteriores preservadas; nenhum commit.

## Resultado e critérios

Acrescentados dez casos: substituição completa seguida de PATCH, exclusão com preservação dos demais registros e oito combinações de operação/falha de commit. Reforçado o teste existente de atualizações inválidas para conferir que o registro permanece integralmente igual.

| Critério | Evidência |
|---|---|
| AC-012 | PUT troca todos os campos, inclusive as três relações; consulta confirma persistência. PATCH normaliza descrição e mantém integralmente os campos omitidos. Testes existentes de corpo incompleto, vazio, desconhecido e recurso ausente seguem passando |
| AC-013 | Testes de relação inválida preservados. Para POST/PUT/PATCH/DELETE, SQL real altera a transação; commit injetado falha com OperationalError ou IntegrityError. Nova conexão observa somente o registro original e nova escrita funciona |
| AC-014 | DELETE retorna 204 sem corpo; consulta e repetição retornam 404 JSON. Segundo lançamento e os três cadastros relacionados são preservados |
| AC-015 | Erro operacional de commit retorna 500; integridade retorna 400; ambos JSON com status error sem marcador interno. Casos anteriores de erro na abertura do banco continuam passando |

A injeção substitui apenas `commit()` em uma subclasse de `sqlite3.Connection` usada pela conexão do repositório. O SQL de produção é executado em banco isolado: antes de lançar a exceção, o teste verifica transação ativa, alterações efetuadas e conteúdo ainda não confirmado. Depois, restaura a conexão normal e verifica persistência e ausência de bloqueio residual mediante nova escrita. Não se trata de falha simulada antes de qualquer alteração.

Não foi encontrado defeito novo nos cenários verificados. O gerenciamento transacional existente já atende às expectativas; nenhuma linha de produção foi alterada nesta tarefa.

## Verificações

Ambiente existente: Python 3.14.3, pytest 9.0.3, `.venv`; sem dependências adicionais.

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_lancamento.py -q
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

- Direcionados: **104 passed in 2.61s**, saída 0.
- Suíte completa: **218 passed in 3.91s**, saída 0.
- Fixtures usam bancos isolados; sem servidor ou migração de dados reais.

## Limites

As três tarefas de F-002 estão concluídas tecnicamente. Exclusão definitiva foi verificada como contrato atual; não foi aprovada a política de remoção para uso compartilhado (Q-003). Os testes não simulam queda de energia, processo encerrado durante commit ou disputa concorrente real. Revisão independente e aceite do produto não foram presumidos. Nenhum commit, push ou deploy executado.

Próxima tarefa: F-003/T-001, contrato de configuração e inicialização, ainda pendente.
