# Especificação — F-003: Banco configurável e migração recuperável

## Estado e referências

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-010, REQ-012. Critérios AC sem prefixo pertencem ao PRD; critérios F-003/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Demonstrar preparação e uso do banco correto e atualização recuperável de base legada sintética. Pré-requisito operacional explícito do MVP.

## Regras e contratos

Preservar DATABASE_PATH, isolamento de testes, conversão em centavos e factory sem criação de schema. Resolver precedência DATABASE/DB_PATH e fronteira de inicialização antes de codificar. Nenhuma migração de dados reais.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
| AC-016 | Em base legada sintética válida, converter 0.29→29, 1.005→101 e 125.90→12590; preservar IDs dos lançamentos e continuidade da sequência mesmo após remoção de ID alto; segunda execução não altera o resultado. Cadastros duplicados são consolidados no menor ID e referências são redirecionadas |
| AC-017 | Em base legada com valor inválido, não positivo, arredondado a zero, acima do limite ou referência inexistente, a migração falha com rollback; comparar schema, registros e cadastros antes/depois e confirmar que não houve atualização parcial |
| F-003/AC-001 | Critério técnico/local proposto: Preparação e API usam o mesmo alvo configurado em dois cenários isolados, sem tocar banco não selecionado. |
| F-003/AC-002 | Critério técnico/local proposto: Backup sintético restaurado após conversão reproduz schema, linhas e sequência salvos; limitações são registradas. |

## Cenários e pendências

`python -m pytest app/tests/test_schema.py app/tests/test_transaction_migration.py`; novos testes são executados por `python -m pytest`. Usar dois bancos temporários para provar seleção e ausência de escrita no alvo não escolhido.

Código antigo é incompatível com valor_centavos. Reversão pós-commit exige backup compatível e parada. Desde T-002, importar app.run não migra; main() prepara o banco. O ensaio de T-003 está descrito em [recuperacao-sintetica.md](recuperacao-sintetica.md).

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

