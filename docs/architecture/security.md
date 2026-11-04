# Identidade, acesso e fronteiras de confiança

Base: [PRD](../product/PRD.md), REQ-011, AC-018/019 e Q-001 a Q-006. Estado: diagnóstico do código e proposta; nenhuma autenticação ou autorização foi implementada nesta etapa.

## Estado existente

- Todas as rotas financeiras registradas podem ser chamadas sem identidade verificada. Não há usuários, perfis, sessões, tokens, política de recurso ou escopo organizacional.
- Validação de entradas, SQL parametrizado para valores e chaves estrangeiras ajudam a preservar integridade; não limitam quem pode ler ou escrever.
- DELETE é definitivo e não registra autor/motivo. Não há trilha de auditoria persistente.
- `DEBUG` é desativado por padrão; isso não restringe operações financeiras.
- Erros de validação podem devolver o valor recebido. Logs de falhas usam logging e podem conter detalhes internos; não há política de acesso/retencão configurada.

## Fronteiras e proposta mínima

| Fronteira | Controle proposto | Decisão pendente |
|---|---|---|
| Cliente → API | Verificar identidade em ponto comum antes das operações financeiras; produzir contexto confiável de usuário | Método de autenticação, ciclo de conta e canal: Q-001/Q-004 |
| Rota → operação de aplicação | Autorizar ação de leitura/criação/edição/exclusão, inclusive chamada direta à API | Matriz por perfil: Q-001 |
| Operação → registro consultado/alterado | Conferir visibilidade/propriedade na leitura por ID e na escrita, dentro da unidade transacional quando necessário | Igreja única, sem subdivisão; contrato técnico pendente |
| Operação → consultas de coleção | Aplicar escopo antes de contar e paginar; não buscar globalmente e filtrar a resposta depois | Mesma regra de escopo aprovada |
| Lançamento → relações | Validar que tipo, categoria e conta são permitidos ao contexto, além de existentes | Mesma base da única igreja; integridade referencial preservada |
| Processo → arquivo SQLite/backups/logs | Restringir acesso operacional e separar dados de material público; definir backup/recuperação e gestão de segredos | Ambiente e responsáveis: Q-006 |

Autenticação responde quem está operando; autorização decide quais ações e registros estão disponíveis. Um usuário autenticado não ganha acesso global por padrão. IDs ou perfis enviados no JSON não devem ser aceitos como prova de autorização. Para operações sem regra definida, a proposta é negar, não inferir permissão.

O contexto autenticado é uma interface futura conceitual, não um schema de usuário aprovado. Recomenda-se concentrar política de acesso junto aos serviços para evitar decisões diferentes entre rotas; repositories recebem restrições derivadas de contexto confiável. Filtros de escopo não substituem a checagem da ação. RBAC confirmado com quatro papéis; não criar tabelas de organizações ou vínculos multi-igreja. Somente Administrador gere acessos.

Não foram escolhidos JWT, cookie de sessão ou provedor externo. Se houver autenticação por cookie em navegador, será necessário definir proteção contra requisições forjadas; se houver tokens, definir armazenamento, expiração e revogação. Transporte protegido e servidor de operação pertencem à definição de implantação. Não confundir ausência de escolha com inexistência da necessidade.

## Política de dados e falhas

Valores, contas e descrições são dados financeiros. Evitar registrar payloads completos ou credenciais em logs; exemplos desta documentação são sintéticos. O histórico de auditoria tem retenção eterna, sem descarte automático. A retenção e o acesso aos logs operacionais continuam dependentes de Q-006 e são separados do histórico.

Proposta de contrato futuro: identidade ausente/inválida resulta em 401; identidade válida sem ação permitida, 403. Para recurso fora do escopo, decidir entre 403 e 404 com regra uniforme para não expor existência. Esses códigos não estão implementados e dependem do contrato de identidade; não alteram hoje os contratos documentados.

Não ocultar falha operacional sob resposta de autorização. Registrar negações sem revelar dados do recurso. Em escrita negada, nenhuma mudança deve ocorrer; em leitura negada, não retornar dados, contagens globais ou nomes de relações.

## Aceite e dependências

AC-018 exige negativas sem identidade em todas as operações. AC-019 exige matriz real aprovada, incluindo chamadas diretas por ID, alteração de relações para recursos fora do escopo e contagem/paginação restritas. Revogação e expiração precisam de cenários quando o método for escolhido.

Uma futura arquitetura de acesso pode avançar nos pontos de integração acima. O contrato técnico de identidade e histórico ainda precisa ser fechado; igreja única, gestão de usuários, exclusões e retenção eterna do histórico já estão definidos. [ADR-003](decisions/ADR-003-acesso-compartilhado.md) registra as alternativas; nenhuma permissividade atual é tratada como aprovação de produto.

## Escopo vigente

[ADR-004](decisions/ADR-004-igreja-unica-rbac.md): uma igreja, quatro papéis e autorização por ação/recurso. Consultar [matriz](../features/F-004-acesso-compartilhado/matriz-acesso.md) e [ciclo de acesso](../features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md) para autoridade, revogação e proteção do último Administrador. Contrato técnico pendente; controles ainda não implementados.
