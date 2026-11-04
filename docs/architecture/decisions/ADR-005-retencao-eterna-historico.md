# ADR-005 — Retenção eterna do histórico de auditoria

## Estado

Confirmado pelo solicitante em 04/11/2026. Implementação e contrato técnico ainda pendentes.

## Decisão

O histórico de auditoria do MVP deve ser retido eternamente. Eventos de alterações financeiras, exclusões e gestão de acesso não podem ser apagados, expirados ou removidos por rotina automática. A regra aplica-se ao histórico de auditoria persistido, não aos logs operacionais, cuja retenção e acesso continuam dependentes das decisões de operação.

O histórico não deve registrar segredos nem cópia integral do conteúdo excluído. Exclusões devem preservar o identificador afetado, o motivo quando exigido, o autor, a data e a ação, conforme REQ-025.

## Consequências

- O schema e as transações devem impedir exclusão acidental ou rotina de descarte do histórico.
- Backup, restauração e evolução do schema devem preservar todos os eventos históricos.
- Consultas comuns não editam nem removem eventos; permissões de consulta do histórico serão fechadas no contrato técnico.
- Crescimento indefinido do histórico exige planejamento de armazenamento e operação, sem converter retenção eterna em expurgo.

## Rastreabilidade

PRD REQ-025, F-004/AC-009, F-004/T-001 e F-004/T-008. A decisão complementa o [ADR-004](ADR-004-igreja-unica-rbac.md).
