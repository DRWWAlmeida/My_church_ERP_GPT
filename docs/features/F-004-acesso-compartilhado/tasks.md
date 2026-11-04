# Tarefas — F-004: Identidade, permissões e gestão de acessos

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa de implementação foi executada; T-001 foi concluída documentalmente nesta revisão.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Fechar matriz e decisões restantes | — | F-004/AC-001; AC-018, AC-019, AC-021, AC-022 | concluída documentalmente |
| T-002 | Fechar contrato técnico de identidade e permissões | F-004/T-001 para fechamento; desenho independente pode avançar | F-004/AC-001; AC-018, AC-019, AC-021, AC-022 | bloqueada |
| T-003 | Implementar identidade e negação anônima | F-004/T-002, F-003/T-003 | AC-018 | bloqueada |
| T-004 | Implementar concessão e retirada de acessos | F-004/T-003 | AC-021, AC-022 | bloqueada |
| T-005 | Autorizar cadastros e suas consultas | F-004/T-004, F-001/T-003 | AC-019, AC-021, AC-022 | bloqueada |
| T-006 | Autorizar lançamentos e referências | F-004/T-005, F-002/T-003 | AC-019, AC-021, AC-022 | bloqueada |
| T-007 | Validar regressão autenticada completa | F-004/T-006, F-004/T-008, F-004/T-009 | AC-018, AC-019, AC-021, AC-022 | bloqueada |
| T-008 | Persistir histórico de alterações | F-004/T-002 | F-004/AC-009 | bloqueada |
| T-009 | Ensaiar evolução e recuperação | F-004/T-002, T-003, T-008; F-003/T-003 | F-004/AC-010 | bloqueada |

## Detalhamento

### F-004/T-001 — Fechar matriz e decisões restantes

- **Estado:** concluída documentalmente; implementação não iniciada.
- **Dependências:** —.
- **Critérios:** F-004/AC-001; AC-018, AC-019, AC-021, AC-022.
- **Escopo e arquivos:** Consolidar quatro papéis, autoridade do Administrador, ciclo de acesso e retenção eterna do histórico de auditoria. Atualizar PRD/matriz-acesso.md com fonte e data.
- **Verificação e conclusão:** Matriz, políticas e retenção eterna confirmadas. Não há rotina de descarte; retenção de logs operacionais permanece separada. Implementação do histórico depende de T-002/T-008.
- **Evidências:** PRD v0.6, matriz RBAC, decisões de ciclo, ADR-004/ADR-005 e handoff vigente; inspeção documental realizada. Testes de aplicação não se aplicam a esta decisão e não foram executados.

### F-004/T-002 — Fechar contrato técnico de identidade e permissões

- **Estado:** bloqueada.
- **Dependências:** F-004/T-001.
- **Critérios:** F-004/AC-001; AC-018, AC-019, AC-021, AC-022.
- **Escopo e arquivos:** Solicitar desenho ao arquiteto: método de identidade para web, primeiro acesso, ciclo de contas, granularidade, esquema, respostas HTTP e efeito da revogação. Arquivos: contrato-identidade.md e arquitetura correspondente.
- **Verificação e conclusão:** Contrato de API e migração/recuperação de dados suficiente para implementar; caminhos propostos confirmados e tarefas repartidas se necessário. Bloqueio: matriz e decisão arquitetural.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-004/T-003 — Implementar identidade e negação anônima

- **Estado:** bloqueada.
- **Dependências:** F-004/T-002, F-003/T-003.
- **Critérios:** AC-018.
- **Escopo e arquivos:** Implementar mecanismo/lifecycle aprovados e contexto confiável em rotas financeiras, com fixtures. Arquivos: módulo de identidade definido, registro de blueprints, erros e test_access.py.
- **Verificação e conclusão:** Chamadas financeiras sem identidade válida são negadas sem dados/efeito; login e fim de acesso seguem contrato. Bloqueio: contrato técnico. Entrega intermediária não deve ser publicada como MVP.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-004/T-004 — Implementar concessão e retirada de acessos

- **Estado:** bloqueada.
- **Dependências:** F-004/T-003.
- **Critérios:** AC-021, AC-022.
- **Escopo e arquivos:** Implementar operações de gestão somente para Administrador, incluindo contas, atribuição de papéis e proteção do último Administrador; persistência, validação e política de revogação conforme contrato. Arquivos: módulo identity e test_permissions.py.
- **Verificação e conclusão:** Administrador define acessos; usuário sem concessão não concede a si próprio nem falsifica papel. Efeito de retirada vale na próxima requisição, conforme política de revogação vigente. Bloqueio: contrato.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-004/T-005 — Autorizar cadastros e suas consultas

- **Estado:** bloqueada.
- **Dependências:** F-004/T-004, F-001/T-003.
- **Critérios:** AC-019, AC-021, AC-022.
- **Escopo e arquivos:** Aplicar política aos GET/POST dos três cadastros e escopos das consultas; testes de acesso direto, ação permitida e negada. Arquivos: rotas/services/repositories dos cadastros e test_access.py.
- **Verificação e conclusão:** Matriz dos cadastros demonstrada e concessões efetivas; nenhum filtro do cliente amplia escopo. Bloqueio: identidade e regras.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-004/T-006 — Autorizar lançamentos e referências

- **Estado:** bloqueada.
- **Dependências:** F-004/T-005, F-002/T-003.
- **Critérios:** AC-019, AC-021, AC-022.
- **Escopo e arquivos:** Aplicar ação/escopo em lista, total, ID, criação, atualização e exclusão aprovada; validar relações autorizadas dentro da transação. Arquivos: módulo transaction e testes de acesso.
- **Verificação e conclusão:** Negativas não alteram dados nem revelam contagem/nomes; cada um dos quatro papéis exerce somente suas operações autorizadas. Exclusões respeitam a autorização e geram histórico de auditoria com retenção eterna. Bloqueio: implementação e contrato.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-004/T-007 — Validar regressão autenticada completa

- **Estado:** bloqueada.
- **Dependências:** F-004/T-006, F-004/T-008, F-004/T-009.
- **Critérios:** AC-018, AC-019, AC-021, AC-022.
- **Escopo e arquivos:** Executar suíte com fixtures autorizadas e negativas explícitas; conferir lifecycle, concessão/revogação, chamadas diretas e casos de cada célula da matriz.
- **Verificação e conclusão:** Evidência por célula e por critério; sem bypass global de autorização nos testes. Bloqueio: implementação anterior.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

## Próxima tarefa elegível

F-004/T-001 está concluída documentalmente. Trabalho independente: F-001/T-001.

## Revisão de escopo e cobertura — 04/11/2026

Responsável por esta revisão documental: agente principal, sem delegação. Resultado: planejamento atualizado; implementação permanece bloqueada pelos contratos. T-001 fechou a decisão de retenção eterna; T-002 pode preparar partes independentes, sem encerrar o contrato antes das decisões necessárias. Não há tarefas de isolamento multi-igreja a executar.

| Tarefa existente | Complemento obrigatório | Critérios adicionais |
|---|---|---|
| T-002 | Contrato para igreja única, quatro papéis, primeiro Administrador, identidade, histórico e edição/exclusão dos cadastros; sem igreja_id/vínculos | AC-025/028/029; F-004/AC-002 a AC-010 vigentes |
| T-003 | Recuperação por e-mail e conta sem papel/inativa | F-004/AC-003/004/005 |
| T-004 | Gestão de contas e papéis pelo Administrador; último Administrador e revogação | AC-028/029; F-004/AC-002/003/004/007/008 |
| T-005 | Edição e exclusão dos três cadastros, respeitando integridade e matriz; integrar eventos de histórico | AC-023/024/025; F-004/AC-008/009 |
| T-006 | Autorizar lançamentos e integrar histórico na mesma transação | AC-025; F-004/AC-008/009 |
| T-007 | Quatro papéis, negativas diretas, catálogo, último Administrador, revogação, histórico e recuperação | AC-023/024/025/028/029; F-004/AC-002 a AC-010 exceto AC-006 |

### F-004/T-008 — Persistir histórico de alterações

- **Estado:** bloqueada; depende de F-004/T-002. A retenção eterna foi definida em T-001.
- **Escopo e arquivos previstos:** módulo de histórico a definir no contrato, schema e testes próprios; integração financeira em T-005/T-006 e administrativa em T-004, serializada quando houver arquivos comuns.
- **Critérios:** REQ-025, F-004/AC-009.
- **Verificação:** evento e mutação confirmam atomicamente; rollback não registra sucesso; exclusão conserva identificador/motivo sem cópia integral ou segredos; eventos de auditoria permanecem retidos sem descarte automático.

### F-004/T-009 — Ensaiar evolução de identidade/histórico e recuperação

- **Estado:** bloqueada; depende de F-004/T-002, T-003, T-008 e F-003/T-003.
- **Escopo e arquivos previstos:** scripts de evolução e testes definidos no contrato, evidências sintéticas; sem migração real.
- **Critérios:** REQ-026, F-004/AC-010.
- **Verificação:** preservar IDs/referências, contagens/valores; falhas e restauração verificadas. Não incluir mapeamento multi-igreja.
