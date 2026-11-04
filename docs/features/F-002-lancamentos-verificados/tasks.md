# Tarefas — F-002: Ciclo financeiro verificado

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Verificar criação e limites de dados | F-001/T-003 | AC-005, AC-006, AC-007, AC-008 | concluída |
| T-002 | Verificar busca e paginação | F-002/T-001 | AC-009, AC-010, AC-011 | concluída |
| T-003 | Verificar edição, exclusão e rollback | F-002/T-002 | AC-012, AC-013, AC-014, AC-015 | concluída |

## Detalhamento

### F-002/T-001 — Verificar criação e limites de dados

- **Estado:** concluída em 30/10/2026. Cobertura ampliada; 80 testes de lançamentos e 194 totais aprovados, sem alteração de produção.
- **Dependências:** F-001/T-003.
- **Critérios:** AC-005, AC-006, AC-007, AC-008.
- **Escopo e arquivos:** Inspecionar/completar test_lancamento.py e corrigir módulo somente diante de falha: valor máximo, tipos inválidos, descrição nos limites, datas e relacionamentos.
- **Verificação e conclusão:** Critérios demonstrados; criação válida persiste e toda rejeição mantém estado anterior. Evidências identificam código/testes alterados.
- **Evidencias:** [evidencias.md](evidencias.md) e [handoff-t001.md](handoff-t001.md); verificacoes concluidas sem mudanca de producao.

### F-002/T-002 — Verificar busca e paginação

- **Estado:** concluída em 03/11/2026; 94 testes de lançamentos e 208 totais aprovados. Evidências em [evidencias-t002.md](evidencias-t002.md).
- **Dependências:** F-002/T-001.
- **Critérios:** AC-009, AC-010, AC-011.
- **Escopo e arquivos:** Cobrir consulta individual, ausência, combinação de filtros, ordem com empate, busca literal e limites de página em test_lancamento.py e correções pontuais.
- **Verificação e conclusão:** Lista e total corretos, páginas vazias 200, ID ausente 404 e consultas inválidas 400; registrar resultados.
- **Evidencias:** [evidencias-t002.md](evidencias-t002.md) e [handoff-t002.md](handoff-t002.md); testes concluidos.

### F-002/T-003 — Verificar edição, exclusão e rollback

- **Estado:** concluída em 03/11/2026; 104 testes de lançamentos e 218 totais aprovados, sem mudança de produção.
- **Dependências:** F-002/T-002.
- **Critérios:** AC-012, AC-013, AC-014, AC-015.
- **Escopo e arquivos:** Testar PUT/PATCH, campos preservados, DELETE e erro operacional; induzir falha durante escrita e comprovar rollback, corrigindo apenas defeito reproduzido.
- **Verificação e conclusão:** Estado anterior preservado em falha; contrato atual de exclusão demonstrado sem aprovar uso compartilhado; suíte da funcionalidade passa.
- **Evidências após execução:** [evidencias-t003.md](evidencias-t003.md) e [handoff-t003.md](handoff-t003.md); falhas de commit verificadas depois da execução real das escritas em banco isolado.

## Próxima tarefa elegível

F-002 não possui tarefas pendentes. Próxima tarefa global: F-003/T-001 — Fechar contrato de configuração e inicialização. Essa tarefa não foi iniciada nesta execução.

