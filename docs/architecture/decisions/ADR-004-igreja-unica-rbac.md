# ADR-004 — Igreja única e RBAC no MVP

## Estado

04/11/2026. Escopo de produto confirmado pelo solicitante; consequências técnicas propostas, sem implementação. Substitui a proposta multi-igreja em isolamento-igrejas.md e as autoridades antigas do ADR-003. A separação entre identidade e autorização do ADR-003 permanece proposta.

## Contexto e decisão

O solicitante retirou múltiplas igrejas do MVP e fixou quatro papéis: Administrador, Presidente, Tesoureiro e Membro. Confirmou que Administrador assume criação/convite de usuários, desativação e nomeação de Administradores, preservando ao menos um ativo.

Manter RBAC para usuários da mesma igreja. Eliminar do planejamento Master, vínculos usuario_igreja, contexto ativo e seleção/cadastro de igrejas. Não exigir igreja_id nos dados financeiros nem nos eventos de histórico. Preservar regras financeiras, recuperação por e-mail, revogação e histórico mínimo com retenção eterna conforme [ADR-005](ADR-005-retencao-eterna-historico.md).

## Alternativas e consequências

- Manter infraestrutura multi-igreja latente acrescentaria schema, migração e testes sem necessidade do MVP; não adotado.
- Remover controle de acesso não atende ao RBAC explicitamente mantido; não adotado.
- Igreja única com RBAC reduz o escopo; uma expansão futura exigirá nova decisão, modelo e migração, sem compromisso antecipado.

Preservar Flask/SQLite e o schema financeiro atual. Novos dados de identidade/histórico dependem de contrato técnico. Não executar migração nem alterar código por esta revisão.

## Rastreabilidade e verificação prevista

PRD REQ-014/016/018 a REQ-028, com REQ-017/022 retirados; AC-025/028/029 e critérios locais F-004 vigentes. Validar quatro papéis, negativas por API direta, revogação, último Administrador, integridade, ausência de seletor de igreja e retenção eterna do histórico de auditoria. O contrato técnico permanece pendente.
