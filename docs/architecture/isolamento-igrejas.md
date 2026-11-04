# Escopo organizacional — igreja única

Atualizado em 04/11/2026. O caminho foi mantido para preservar referências. A proposta anterior de isolamento entre igrejas foi retirada do MVP; histórico em [decisões substituídas](../history/2026-11-04-decisoes-substituidas.md).

## Decisão vigente e consequências

O MVP atende uma única igreja, com RBAC: Administrador, Presidente, Tesoureiro e Membro. Não há Master, cadastro/seleção de igrejas nem múltiplos vínculos por usuário. REQ-016/AC-025 foram revisados; REQ-017/AC-026/AC-027 foram retirados do MVP.

O desenho mínimo preserva o schema financeiro e a unicidade global de nomes existentes. Não adicionar igreja_id obrigatório, tabela de igrejas, usuario_igreja, índices por igreja ou migração de propriedade multi-igreja por esta entrega. Identidade, papéis, permissões e histórico terão schema próprio a fechar em F-004/T-002.

Todos os usuários autorizados operam sobre os dados da mesma igreja, sem subdivisão por unidade ou conta; RBAC continua obrigatório em cada ação. IDs e papéis recebidos do cliente não comprovam autorização. Referências financeiras devem continuar existentes e íntegras na transação.

A interface não terá seletor de igreja. Somente Administrador gere usuários e permissões. Negativas devem ser verificadas também por chamada direta à API.

Não há mapeamento de legado entre igrejas a obter. Inventário, backup, ensaio, validação de IDs/referências e restauração continuam necessários para migrações efetivamente exigidas por identidade/histórico. Nenhuma migração foi executada nesta revisão.

Ver [ADR-004](decisions/ADR-004-igreja-unica-rbac.md), [matriz](../features/F-004-acesso-compartilhado/matriz-acesso.md) e [ciclo de acesso](../features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md).
