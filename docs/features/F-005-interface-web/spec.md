# Especificação — F-005: Interface web das jornadas do MVP

## Estado e referências

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-013, REQ-014; integração de REQ-001 a REQ-009 e REQ-011. Critérios AC sem prefixo pertencem ao PRD; critérios F-005/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Construir interface web nova, confirmada pelo usuário, para acessar o sistema, operar cadastros/lançamentos e gerir acessos conforme perfil. Não existe frontend atual para reaproveitar.

## Regras e contratos

Consumir API e política aprovadas; representar centavos sem perda, apresentar erro/vazio/paginação/negação. UI não substitui autorização do backend. Não incluir dashboard, relatórios, transferências ou domínio novo.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
| AC-020 | Pela interface web, uma identidade autorizada acessa o sistema, cria/consulta cadastros, registra, localiza e edita lançamento; realiza a ação de remoção somente conforme política aprovada. Erros, resultados vazios e negativas são observáveis; dados e centavos coincidem com a API. Verificar também gestão de acessos para os perfis autorizados |
| AC-021 | Administrador configura permissões; Presidente e Tesoureiro operam conforme matriz, sem gerir acessos; Membro somente consulta. Verificar aplicação na API e interface |
| AC-022 | Usuário sem concessão não consegue executar a operação nem conceder privilégios a si mesmo por chamada direta ou payload forjado; ao retirar uma concessão, seu efeito segue a política de atualização/revogação acordada. Critério depende de fechar Q-001 |
| F-005/AC-001 | Critério técnico/local proposto: Desenho web define arquitetura/arquivos, estados das jornadas, integração de identidade, representação numérica e verificações; permite decomposição sem decisões ocultas. |

## Cenários e pendências

Demonstrar jornadas com dados sintéticos pelo navegador e testar chamadas diretas negativas na API. Comandos de build/lint/E2E não existem no repositório: serão descobertos/definidos após escolha técnica e registrados em T-001, sem apresentar comandos hipotéticos como executados.

Q-004 resolvida: web nova. Tecnologia, organização de arquivos e mecanismo de autenticação ainda pendentes; não trocar stack por iniciativa do planejador. Nenhuma migração financeira esperada; compatibilidade de identidade em F-004.

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

T-001 desenha os quatro papéis sem seletor de igreja; T-004 cobre edição/exclusão de cadastros e lançamento; T-005 cobre gestão exclusiva do Administrador, negativas dos outros papéis e proteção do último Administrador (AC-028/029), conforme API F-004. Não apresentar permissões na interface como substituto da autorização no backend.
