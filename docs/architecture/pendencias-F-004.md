# Pendências — F-004

Atualizado em 04/11/2026 para [PRD v0.6](../product/PRD.md) e [ADR-004](decisions/ADR-004-igreja-unica-rbac.md). Diagnóstico anterior preservado no histórico. Esta revisão é documental.

## Resolvido

Igreja única; quatro papéis; Administrador gere contas e permissões; Presidente/Tesoureiro operam conforme matriz; Membro somente consulta. Sem Master, vínculos ou seletor de igrejas. Recuperação por e-mail, revogação na próxima requisição, proteção do último Administrador, exclusões e histórico mínimo com retenção eterna definidos no [ciclo de acesso](../features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md).

## Estado e pendências

- T-001: concluída documentalmente; retenção eterna do histórico de auditoria confirmada, sem descarte automático.
- T-002: mecanismo de autenticação web, primeiro acesso, sessões/links, e-mail, endpoints, erros, DDL de identidade e histórico, atomicidade e recuperação.
- Contratos para edição e exclusão dos três cadastros; não inferir implementação a partir da matriz.
- Migração de identidade/histórico, se necessária, com ensaio sintético. Mapeamento multi-igreja não é bloqueio.
- Q-005/Q-006/Q-007: concorrência/carga, operação e moeda continuam no planejamento operacional.

T-002 pode avançar nas partes independentes; implementação aguarda os contratos aplicáveis. F-001/F-002/F-003 mantêm suas evidências e estados anteriores, sem reexecução ou reabertura causada por esta revisão. Testes futuros devem usar quatro papéis em uma igreja, inclusive API direta, ausência de papel, autopromoção, revogação e último Administrador.
