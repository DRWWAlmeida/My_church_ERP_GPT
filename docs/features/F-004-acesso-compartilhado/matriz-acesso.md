# Matriz RBAC — F-004

Data: 04/11/2026. Estado: regras de produto confirmadas; implementação e contrato técnico pendentes. Fonte: pedido de igreja única e quatro papéis, com confirmação de transferência da gestão de contas ao Administrador.

## Papéis e concessões

| Papel | Ver | Criar/Editar | Excluir | Gerir contas, papéis e permissões |
|---|---|---|---|---|
| Administrador | Sim | Sim | Sim | Sim |
| Presidente | Sim | Sim | Sim | Não |
| Tesoureiro | Sim | Sim | Sim | Não |
| Membro | Sim | Não | Não | Não |

A matriz preserva as concessões operacionais anteriormente confirmadas. Ver e Ler são a mesma permissão; Criar/Editar é uma concessão conjunta. As permissões são associadas a papéis por recurso (categorias, contas, tipos e lançamentos), configuradas pelo Administrador. O nome Presidente não concede gestão administrativa. Não presumir concessões individuais adicionais.

REQ-018 mantém um papel por usuário, agora na única igreja. Administrador é um dos quatro papéis, sem necessidade de acumular papel operacional. Contas sem papel ou inativas não acessam dados financeiros. Não existe Master nem vínculo multi-igreja no MVP. REQ-027/AC-028 fixam o catálogo.

Administrador cria/convida usuários, desativa contas, atribui papéis e nomeia outros Administradores (REQ-028/AC-029). Preservar o último Administrador ativo. Não há cadastro público. Detalhes em [ciclo de acesso](decisoes-ciclo-acesso.md).

## Regras de operação e verificação

- Autenticar e autorizar cada ação no backend, incluindo consultas, listas, contagens, acesso por ID e chamadas diretas.
- Presidente e Tesoureiro executam ações concedidas; retirar uma concessão produz negativa mesmo com sessão aberta. Membro não cria, edita nem exclui.
- Somente Administrador gere acessos; os outros três papéis não se autopromovem nem atribuem papéis por payload forjado.
- Rejeitar Master e outros papéis fora do catálogo sem modificar a conta.
- Exclusão de lançamento não tem limite de data; exclusão de cadastro exige ausência de lançamentos vinculados.
- Testar todos os quatro papéis com dados sintéticos de uma única igreja; não há seletor de igreja.
- Edição/exclusão dos cadastros ainda exigem contrato e implementação; a matriz não comprova sua existência.

## Pendências

Retenção eterna do histórico de auditoria está confirmada; não há descarte automático. Permanece pendente o contrato técnico F-004/T-002 e a implementação. Retenção de logs operacionais é uma decisão operacional separada. Histórico anterior preservado em [decisões substituídas](../../history/2026-11-04-decisoes-substituidas.md).
