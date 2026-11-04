# ADR-003 — Separar identidade de política de acesso

## Estado

Proposta condicionada, 28/10/2026. Uso compartilhado foi confirmado no [PRD](../../product/PRD.md); escopo e papéis foram definidos no [ADR-004](ADR-004-igreja-unica-rbac.md). Mecanismo técnico ainda não aprovado ou implementado.

## Contexto

REQ-011 e AC-018/019 exigem definir acesso para uso compartilhado. O aplicativo atual não tem contexto de usuário e permite chamadas financeiras anônimas. O MVP terá interface web para uma igreja e quatro papéis; o contrato de identidade ainda precisa ser fechado.

## Alternativas

| Opção | Benefício | Custo/limite |
|---|---|---|
| Autenticação comum e política aplicada às operações e recursos | Pontos consistentes de controle e testes de acesso direto | Exige contexto confiável, matriz de ações e escopo definidos |
| Apenas ocultar ações no frontend | Apresentação simples | Chamadas diretas à API continuam possíveis; não atende REQ-011 |
| Apenas exigir login, sem checar ação/recurso | Identifica o usuário | Não atende restrições por perfil ou escopo que venham a ser definidas |

## Decisão

Propor autenticação na entrada da API e autorização junto às operações de aplicação. Aplicar escopo também em consultas, contagens e relações de lançamentos; negar operações sem regra. Aplicar RBAC com os quatro papéis do ADR-004; provedor e tokens/sessões permanecem pendentes. Não implementar modelo multi-igreja.

## Consequências

Clientes anônimos atuais deixarão de acessar as operações protegidas quando o requisito for implementado. Será necessário definir provisionamento, expiração/revogação e atualizar testes/consumidores. Evolução de identidade e histórico deve preservar registros legados; mapeamento entre igrejas não se aplica ao MVP.

Não planejar recuperação removendo autorização e reabrindo dados. A mudança deve ter versão/configuração compatíveis e caminho de manutenção controlado. Detalhes e limites estão em [security.md](../security.md).

## Pendências

Fechar contrato técnico de identidade e histórico; retenção eterna do histórico está definida no ADR-005 e Q-002/Q-004 estão resolvidas. O desenho dos pontos de integração pode ser planejado; contratos definitivos de identidade e dados dependem dessas respostas.
