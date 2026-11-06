# Tarefas — F-003: Banco configurável e migração recuperável

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Fechar contrato de configuração e inicialização | F-001/T-001 | F-003/AC-001; AC-016, AC-017 | concluída |
| T-002 | Alinhar preparação e acesso ao banco | F-003/T-001 | F-003/AC-001; AC-016, AC-017 | concluída |
| T-003 | Ensaiar migração e recuperação | F-003/T-002 | AC-016, AC-017; F-003/AC-002 | concluída |

## Detalhamento

### F-003/T-001 — Fechar contrato de configuração e inicialização

- **Estado:** concluída em 03/11/2026; contrato definido, sondagem concluída e 12 testes de dados aprovados.
- **Dependências:** F-001/T-001.
- **Critérios:** F-003/AC-001; AC-016, AC-017.
- **Escopo e arquivos:** Investigar precedência dentro/fora do contexto Flask; registrar em contrato-configuracao.md chave canônica, compatibilidade e preparação única antes do atendimento. Encaminhar decisão ao arquiteto se divergir da proposta.
- **Verificação e conclusão:** Contrato técnico reproduzível com casos de teste; não promover a proposta de unificação a mudança implementada. Registrar dependências de revisão técnica antes de T-002.
- **Evidências:** [evidencias.md](evidencias.md), [contrato](contrato-configuracao.md) e [handoff](handoff-t001.md). Nenhuma implementação de T-002.

### F-003/T-002 — Alinhar preparação e acesso ao banco

- **Estado:** concluída em 04/11/2026, com 240 testes aprovados; incidente inicial registrado nas evidências.
- **Dependências:** F-003/T-001.
- **Critérios:** F-003/AC-001; AC-016, AC-017.
- **Escopo e arquivos:** Aplicar contrato fechado aos arquivos de configuração/entrada e testes propostos. Preservar factory sem migração e execução local documentada; preparar schema de forma controlada.
- **Verificação e conclusão:** Teste de dois alvos passa e prova que o banco padrão não é tocado por configuração de teste; regressões de schema/migração passam.
- **Evidências:** [evidencias-t002.md](evidencias-t002.md) e [handoff-t002.md](handoff-t002.md). O incidente anterior à correção não comprova preservação do banco local; os testes posteriores demonstram isolamento.

### F-003/T-003 — Ensaiar migração e recuperação

- **Estado:** concluída em 04/11/2026; 243 testes aprovados, incluindo restauração sintética pós-commit.
- **Dependências:** F-003/T-002.
- **Critérios:** AC-016, AC-017; F-003/AC-002.
- **Escopo e arquivos:** Completar testes de consolidação, referências, sequência, arredondamento e rollback conforme lacunas; ensaiar restauração de cópia sintética e documentar procedimento.
- **Verificação e conclusão:** Comparações antes/depois comprovam preservação e rollback; recuperação pós-commit demonstrada no ensaio, sem alegar RPO/RTO ou recuperação real.
- **Evidências após execução:** [evidencias.md](evidencias.md), [procedimento](recuperacao-sintetica.md) e [handoff](handoff-t003.md).

## Próxima tarefa elegível

Nenhuma tarefa de implementação pendente em F-003. Revisão independente permanece pendente.
