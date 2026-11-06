# Decisões vigentes — ciclo de acesso F-004

Data: 04/11/2026. Revisão para uma única igreja e quatro papéis. Regras anteriores compatíveis foram preservadas; gestão de contas pelo Administrador confirmada explicitamente pelo solicitante. Não comprova implementação.

| ID | Regra vigente | Verificação de aceite |
|---|---|---|
| REQ-018 | Um papel por usuário na única igreja, dentre Administrador, Presidente, Tesoureiro e Membro. | F-004/AC-002: impedir dois papéis simultâneos; mudança de papel não mantém concessões anteriores. |
| REQ-019 | Administrador cria/convida contas e atribui papéis. Sem cadastro público; conta sem papel não acessa dados financeiros. | F-004/AC-003: conta sem papel não acessa dados; outros papéis não criam contas ou atribuem papéis. |
| REQ-020 | Administrador desativa/suspende acesso à conta, preservando registros e autoria. Não há distinção global/local. | F-004/AC-004: conta desativada perde acesso à única igreja, sem apagar registros financeiros. |
| REQ-021 | Recuperação por e-mail com link temporário de uso único; usuário define senha. Administrador pode iniciar envio, sem escolher/visualizar senha. | F-004/AC-005: link expirado/reutilizado falha; recuperação não reativa conta nem concede papel. |
| REQ-022 | Retirado: criação de igrejas não pertence ao MVP. | F-004/AC-006 retirado; sem fluxo de criação/seleção de igrejas. |
| REQ-023 | Primeiro Administrador provisionado na instalação por procedimento restrito, sem senha padrão. Administrador existente nomeia outros com confirmação de identidade e registro. Contas pessoais. | F-004/AC-007: impedir retirada/desativação do último Administrador ativo, inclusive sob concorrência; testar também AC-029 do PRD. |
| REQ-024 | Revogação vale na próxima requisição, sem novo login. Escrita em andamento revalida autoridade antes de confirmar; operação já confirmada permanece registrada. | F-004/AC-008: sessão aberta perde acesso após revogação; escrita sem autorização no momento de confirmar é revertida. |
| REQ-025 | Histórico mínimo registra autor, data, ação e registro afetado, cobrindo alterações financeiras, exclusões e gestão de acesso. A retenção do histórico de auditoria é eterna, sem descarte automático. Interface comum não edita histórico. Exclusão mantém identificador e motivo, sem cópia integral do conteúdo. | F-004/AC-009: mutação confirmada tem evento correspondente; falha não gera evento de sucesso; eventos não são eliminados; segredos não são registrados. Não exigir igreja_id. |
| REQ-026 | Inventariar legado antes de mudanças de identidade/histórico; ensaiar migração necessária em cópia, preservando IDs/referências e conferindo quantidades, valores e restauração. Associação multi-igreja foi retirada. | F-004/AC-010: ensaio sintético valida integridade e recuperação; não depende de mapeamento de registros entre igrejas. |

REQ-027/028 e AC-028/029 estão no [PRD](../../product/PRD.md). Critérios F-004/AC são locais. Os IDs retirados não serão reutilizados. Para REQ-023, o procedimento técnico de primeiro acesso ainda deve ser fechado em T-002.

## Pendências e planejamento

- Retenção eterna do histórico de auditoria confirmada em 04/11/2026; não implementar rotina de descarte. Retenção de logs operacionais permanece fora desta decisão.
- T-002 deve fechar autenticação, endpoints, payloads, persistência, expiração, entrega de e-mail, atomicidade da revogação/histórico, evolução de schema e recuperação.
- T-001 pode ser concluída quanto à decisão de produto; T-002 permanece pendente para fechar o contrato técnico, sem declarar implementação concluída.
- T-003 cobre identidade e recuperação; T-004, administração de contas/papéis e último Administrador; T-005/T-006, autorização e histórico; T-007, regressão autenticada; T-008/T-009 explicitam auditoria e migração.
- Nenhuma migração real ou ação externa está autorizada por este registro.
