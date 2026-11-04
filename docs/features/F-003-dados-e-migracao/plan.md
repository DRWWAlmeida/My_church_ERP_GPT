# Plano — F-003: Banco configurável e migração recuperável

## Referências e abordagem

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: `app/config.py`, `app/core/database.py`, `app/run.py`, `app/scripts/schema.py`, `transaction_migration.py`, `app/tests/conftest.py`, `test_schema.py`, `test_transaction_migration.py`. Propostos: `app/tests/test_database_config.py`, `contrato-configuracao.md` e `evidencias.md` neste diretório.

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Código antigo é incompatível com valor_centavos. Reversão pós-commit exige backup compatível e parada. Desde T-002, importar app.run não prepara o banco; main() prepara no contexto da aplicação. Ver evidencias-t002.md para o incidente anterior à correção.

## Estratégia de verificação

`python -m pytest app/tests/test_schema.py app/tests/test_transaction_migration.py`; novos testes são executados por `python -m pytest`. Usar dois bancos temporários para provar seleção e ausência de escrita no alvo não escolhido.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-003/T-001 | F-003/AC-001; AC-016, AC-017 | Contrato técnico reproduzível com casos de teste; não promover a proposta de unificação a mudança implementada. Registrar dependências de revisão técnica antes de T-002. |
| F-003/T-002 | F-003/AC-001; AC-016, AC-017 | Teste de dois alvos passa e prova que o banco padrão não é tocado por configuração de teste; regressões de schema/migração passam. |
| F-003/T-003 | AC-016, AC-017; F-003/AC-002 | Comparações antes/depois comprovam preservação e rollback; recuperação pós-commit demonstrada no ensaio, sem alegar RPO/RTO ou recuperação real. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.


## Contrato fechado por T-001

Implementar T-002 conforme [contrato-configuracao.md](contrato-configuracao.md), incluindo CFG-01 a CFG-12. Contrato implementado por T-002 em 04/11/2026, conforme evidencias-t002.md. Revisão independente permanece pendente.
