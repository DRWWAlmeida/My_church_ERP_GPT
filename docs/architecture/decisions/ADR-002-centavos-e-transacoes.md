# ADR-002 — Preservar centavos inteiros e transações por operação

## Estado

Proposta de continuidade, 28/10/2026. Registra escolha já presente no código, sem presumir aprovação retroativa de produto.

## Contexto

[PRD](../../product/PRD.md): REQ-004, REQ-010 e REQ-012 exigem valores inteiros em centavos, migração e integridade. `transaction.repository` abre transações explícitas; `schema.py` envolve a atualização do banco em uma transação.

## Alternativas

| Opção | Benefício | Custo/limite |
|---|---|---|
| Centavos inteiros e transação por operação | Representação já contratada, validação de relações e rollback conjuntos | Escala fixa; moeda não registrada; limite numérico explícito |
| Retornar ao valor decimal legado | Evitaria conversão em instalações antigas | Quebra contrato atual e reabre o tratamento da representação monetária |
| Separar cada instrução em commits | Escritas isoladas simples | Perde atomicidade de atualização e migração |

## Decisão

Propor preservação dos centavos e das unidades atuais: escrita de lançamento com BEGIN IMMEDIATE, contagem/página na mesma transação de leitura e migração global transacional. Repositórios detêm a conexão e encerram a operação. Não distribuir uma operação atômica entre repositórios com commits independentes.

## Consequências

O contrato exige valor positivo até 9223372036854775807 e não calcula saldo. Não há proteção contra edição de cliente desatualizado ou repetição de POST; essas propriedades não decorrem de atomicidade. Não há retry próprio para disputa de escrita. Detalhes oficiais consultados em 28/10/2026: [transações SQLite](https://www.sqlite.org/lang_transaction.html); versão do SQLite da implantação não verificada.

A conversão atual usa ROUND_HALF_UP, preserva IDs dos lançamentos e não tem downgrade automático. Recuperação após commit exige backup/código compatíveis e parada do atendimento; estratégia completa em [data-model.md](../data-model.md). Nenhuma migração é executada por este ADR.

## Pendências

Q-005/Q-006/Q-007: concorrência, recuperação e moeda. Registrar versão real do runtime e testar carga/rollback antes de concluir adequação operacional. Alterações de moeda, escala ou controle de versão requerem contrato e estratégia para dados existentes.
