# Especificação — F-004: Identidade, permissões e gestão de acessos

## Estado e referências

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-011, REQ-014, REQ-016, REQ-018 a REQ-028 (REQ-022 retirado); compatibilidade com REQ-001 a REQ-012. Critérios AC sem prefixo pertencem ao PRD; critérios F-004/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Entregar núcleo financeiro protegido para uma igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas e permissões; matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão definidos, com contrato técnico pendente.

## Regras e contratos

Aplicar autenticação comum e autorização por ação/recurso conforme contrato arquitetural a fechar. Gestão de acessos pelo Administrador foi explicitamente solicitada; não implica cadastro público, painel genérico, outros perfis ou escolha de JWT/cookie. Acesso geral abrange as funções aprovadas do MVP, sem resolver a política de exclusão.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
| AC-018 | Proposto: sem identidade verificada, tentativas de consulta, criação, edição e exclusão são negadas sem revelar dados financeiros nem alterar registros. Fluxo de autenticação e respostas exatas dependem de Q-001 |
| AC-019 | Condicional à matriz aprovada: testar cada combinação de perfil, operação e escopo de dados, incluindo acesso direto por ID; permitidas funcionam e negadas não revelam nem alteram registros. Q-002 está resolvida: igreja única; contrato e implementação ainda precisam ser verificados |
| AC-021 | Administrador configura permissões; Presidente e Tesoureiro operam conforme matriz, sem gerir acessos; Membro somente consulta. Verificar aplicação na API e interface |
| AC-022 | Usuário sem concessão não consegue executar a operação nem conceder privilégios a si mesmo por chamada direta ou payload forjado; ao retirar uma concessão, seu efeito segue a política de atualização/revogação acordada. Critério depende de fechar Q-001 |
| F-004/AC-001 | Critério técnico/local proposto: Matriz especifica ações, escopos, concessão/revogação e provisionamento, confirmados pelo solicitante; contrato técnico define mecanismo e dados sem decisão oculta. |

## Cenários e pendências

Após desenho aprovado, `python -m pytest`, com identidades sintéticas dos quatro papéis em uma única igreja. Exercitar chamadas diretas por ID, contagens, referências inválidas, concessão/revogação e tentativa de elevação de privilégio; preservar regressões do núcleo.

Q-002/Q-008 resolvidas: igreja única, sem vínculos entre igrejas. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão definidos; contrato técnico permanece pendente. T-002 pode avançar nas partes independentes. Migração/recuperação de identidade e histórico deve constar do contrato antes de código; não há associação multi-igreja a realizar.

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

## Critérios complementares vigentes

AC-025: única igreja sem seleção de contexto, mantendo autorização por ação. AC-028: catálogo fechado de quatro papéis. AC-029: somente Administrador gere contas/nomeações, preservando o último ativo. AC-026/027 e F-004/AC-006 retirados do MVP, sem reutilização de IDs.

F-004/AC-002 a AC-010, exceto AC-006, têm regra e verificação em [ciclo de acesso](decisoes-ciclo-acesso.md). REQ-015/AC-023/024 preservam exclusão de cadastro apenas sem vínculos. Edição de cadastros integra a concessão Criar/Editar e exige contrato/implementação na T-005.
