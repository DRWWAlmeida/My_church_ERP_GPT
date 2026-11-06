# ADR-001 — Preservar o monólito modular e a stack

## Estado

Proposta, 28/10/2026. A estrutura descrita já existe; sua continuidade é recomendação arquitetural, sem registrar nova aceitação pelo usuário.

## Contexto

O [PRD](../../product/PRD.md) delimita quatro módulos financeiros e pede preservar a stack. REQ-001 a REQ-012 compartilham dados e transações. Não há requisito de implantação independente nem carga definida em Q-005. Manifestos fixam Flask 3.1.3 e pytest 9.0.3; Python 3.14 ou compatível consta no README.

## Alternativas

| Opção | Benefício | Custo/limite |
|---|---|---|
| Manter módulos no mesmo aplicativo e SQLite | Preserva contratos e reduz mudanças para resolver requisitos atuais | Banco/processo compartilhados; capacidade e operação precisam de avaliação |
| Reorganizar toda a aplicação em nova arquitetura/ORM | Pode uniformizar abstrações | Migração transversal sem necessidade demonstrada pelo PRD |
| Separar serviços/bancos | Implantação independente | Contratos distribuídos e consistência mais complexos, sem justificativa atual |

## Decisão

Propor continuidade do monólito modular: rotas, validação, serviços e repositórios por domínio; core restrito ao compartilhamento real. Preservar Flask, SQLite e SQL parametrizado. Não impor refatoração geral das diferenças internas dos módulos.

## Consequências

Não requer migração ou mudança de contrato por si só. Correções de configuração e validação podem ser planejadas isoladamente. Capacidade compartilhada e mecanismo de acesso são avaliados separadamente; não há promessa de escala. Hospedagem e servidor de operação permanecem abertos, conforme [overview](../overview.md).

## Pendências

Q-004/Q-005/Q-006: interface, carga e operação. Reavaliar persistência ou topologia somente com requisitos e medições. Não instalar infraestrutura nesta etapa.
