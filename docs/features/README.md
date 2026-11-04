# Plano de entregas até o MVP

## Estado e base

Versão 0.1 — 29/10/2026. Base de código: branch `feature/api-transaction`, commit `02d08b4`. Entradas: [PRD vigente](../product/PRD.md), [arquitetura](../architecture/overview.md), [contratos](../architecture/contracts.md) e [segurança](../architecture/security.md).

Planejamento com **6 entregas e 25 tarefas**. Atualização de 29/10/2026: F-001/T-001 concluída, com ambiente isolado e 152 testes aprovados; [evidências](F-001-cadastros-confiaveis/evidencias.md). Atualização de 30/10/2026: F-001/T-002 concluída com 164 testes aprovados; [evidências de T-002](F-001-cadastros-confiaveis/evidencias-t002.md). F-001/T-003 concluída em 30/10/2026, com 188 testes aprovados; [evidências de T-003](F-001-cadastros-confiaveis/evidencias-t003.md). F-001 possui suas três tarefas concluídas; F-002/T-001 também concluída, com 194 testes aprovados ([evidências](F-002-lancamentos-verificados/evidencias.md)); F-002/T-002 concluída em 03/11/2026 com 208 testes aprovados ([evidências](F-002-lancamentos-verificados/evidencias-t002.md)); F-002/T-003 concluída em 03/11/2026 com 218 testes aprovados ([evidências](F-002-lancamentos-verificados/evidencias-t003.md)). F-001 e F-002 estão tecnicamente concluídas; F-003/T-001 concluída em 03/11/2026 com [contrato de configuração](F-003-dados-e-migracao/contrato-configuracao.md), sondagem e 12 testes de dados aprovados; F-003/T-002 concluída em 04/11/2026 com 240 testes aprovados ([evidências e incidente inicial](F-003-dados-e-migracao/evidencias-t002.md)); as demais 17 tarefas não foram executadas. Não tratar funcionalidades presentes como trabalho a reescrever nem aprovação da suíte como aceite de todos os critérios do MVP.

Confirmado: interface web, igreja única, RBAC com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas e permissões. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria definidos na F-004; contrato técnico pendente.

## Ordem sugerida

| Entrega | Resultado demonstrável | Documentos | Situação |
|---|---|---|---|
| F-001 — Cadastros confiáveis | Demonstrar criação e consulta dos três cadastros com respostas consistentes, corrigindo o limite de IDs já identificado. O ambiente isolado é pré-requisito, não a entrega funcional. | [spec](F-001-cadastros-confiaveis/spec.md), [plan](F-001-cadastros-confiaveis/plan.md), [tasks](F-001-cadastros-confiaveis/tasks.md) | Planejamento executável por dependências |
| F-002 — Ciclo financeiro verificado | Demonstrar cadastro de relações → lançamento → busca → edição → exclusão atual em banco sintético. Reaproveitar CRUD existente; corrigir somente desvios de critérios demonstrados. | [spec](F-002-lancamentos-verificados/spec.md), [plan](F-002-lancamentos-verificados/plan.md), [tasks](F-002-lancamentos-verificados/tasks.md) | Planejamento executável por dependências |
| F-003 — Banco configurável e migração recuperável | Demonstrar preparação e uso do banco correto e atualização recuperável de base legada sintética. Pré-requisito operacional explícito do MVP. | [spec](F-003-dados-e-migracao/spec.md), [plan](F-003-dados-e-migracao/plan.md), [tasks](F-003-dados-e-migracao/tasks.md) | Planejamento executável por dependências |
| F-004 — Identidade, permissões e gestão de acessos | Entregar núcleo financeiro protegido para uma igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas e permissões; matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão definidos, com contrato técnico pendente. | [spec](F-004-acesso-compartilhado/spec.md), [plan](F-004-acesso-compartilhado/plan.md), [tasks](F-004-acesso-compartilhado/tasks.md) | Planejamento condicionado às decisões e contratos indicados |
| F-005 — Interface web das jornadas do MVP | Construir interface web nova, confirmada pelo usuário, para acessar o sistema, operar cadastros/lançamentos e gerir acessos conforme perfil. Não existe frontend atual para reaproveitar. | [spec](F-005-interface-web/spec.md), [plan](F-005-interface-web/plan.md), [tasks](F-005-interface-web/tasks.md) | Planejamento condicionado às decisões e contratos indicados |
| F-006 — Aceite integrado e preparação operacional | Demonstrar MVP integrado em homologação com recuperação ensaiada, metas/limites conhecidos e aceite rastreável. Preparar entrega revisável; implantação real não está autorizada por este planejamento. | [spec](F-006-aceite-operacional/spec.md), [plan](F-006-aceite-operacional/plan.md), [tasks](F-006-aceite-operacional/tasks.md) | Planejamento condicionado às decisões e contratos indicados |

F-001/T-001 vem primeiro. Após o baseline, F-003/T-001 pode avançar independentemente das correções de cadastros; F-002 segue F-001. As decisões de acesso e operação podem ser resolvidas enquanto o núcleo é verificado. F-004 protege a API e a gestão de acessos, F-005 entrega as jornadas web, e F-006 reúne homologação e aceite. Essa ordem de trabalho não aciona agentes nem autoriza execução em paralelo automaticamente.

F-003 é pré-requisito operacional, não entrega funcional ao usuário final. Todas as outras entregas técnicas precisam culminar em jornadas demonstráveis. F-006 prepara o candidato; não contém deploy autorizado.

## Cobertura do produto

| Requisitos | Critérios do PRD | Tarefas responsáveis | Verificação |
|---|---|---|---|
| REQ-001, REQ-002 | AC-001, AC-002, AC-003, AC-004 | F-001/T-002, F-001/T-003 | Fluxos de cadastro, vazio, duplicidade e limites; testes dos três módulos |
| REQ-003, REQ-004, REQ-005 | AC-005, AC-006, AC-007, AC-008 | F-002/T-001 | Criação, relações, valores e datas; test_lancamento |
| REQ-006 | AC-009, AC-010, AC-011 | F-002/T-002 | Consulta individual, filtros, ordenação e paginação |
| REQ-007, REQ-008, REQ-012 | AC-012, AC-013, AC-014 | F-002/T-003 | Atualização, exclusão herdada e rollback; Q-003 para política compartilhada |
| REQ-009 | AC-015 | F-001/T-003, F-002/T-003 | Erros e envelopes observáveis sem detalhes internos nos fluxos tratados |
| REQ-010, REQ-012 | AC-016, AC-017 | F-003/T-003 | Migração, sequência, referências e recuperação sintética |
| REQ-011 | AC-018, AC-019 | F-004/T-003, F-004/T-005, F-004/T-006, F-004/T-007 | Negativas anônimas, matriz por ação/recurso e regressão autenticada |
| REQ-013 | AC-020 | F-005/T-002, F-005/T-003, F-005/T-004, F-005/T-005 | Jornadas pela web com vazio, erro, permissão e valores conferidos |
| REQ-014, REQ-011 | AC-021, AC-022 | F-004/T-004, F-004/T-007, F-005/T-005 | Administrador, Presidente, Tesoureiro e Membro testados separadamente; concessão/retirada e proibição de autopromoção |

F-006/T-003 verifica o conjunto AC-001 a AC-022 após integração. Critérios técnicos locais usam prefixo da entrega (por exemplo F-003/AC-001) e têm tarefas/verificações nos respectivos documentos; não renumeram os critérios do PRD.

## Decisões e investigações antes das partes condicionadas

| Questão | Já conhecido | Falta decidir / evidência esperada | Tarefa |
|---|---|---|---|
| Q-001 | Quatro papéis, gestão pelo Administrador e retenção eterna confirmados | Contrato técnico | F-004/T-002 |
| Q-002 | Resolvida: igreja única | Nenhum vínculo ou seletor multi-igreja | F-004/T-002 |
| Q-003 | Resolvida: exclusões, histórico mínimo e retenção eterna confirmados | Nenhuma rotina de descarte; logs operacionais são separados | F-004/T-002/T-008 |
| Q-004 | Resolvida: web nova | Arquitetura de interface, paths, identidade e comandos de verificação | F-005/T-001 e F-004/T-002 |
| Q-005 | Sem carga ou política de conflito definida | Volume, simultaneidade, atualização concorrente/reenvios e critérios verificáveis | F-006/T-001 |
| Q-006 | Backup/parada constam no README para migração | Ambiente, responsáveis, metas de recuperação e execução de homologação | F-006/T-001 |
| Q-007 | Exemplos usam BRL e tipos livres | Confirmar moeda e semântica no MVP; não introduzir saldo ou multimoeda por inferência | F-006/T-001 |
| Configuração do banco | DATABASE/DB_PATH divergem | Contrato de precedência e inicialização que preserve compatibilidade | F-003/T-001 |

As respostas não recebidas mantêm tarefas bloqueadas. Quando uma decisão exigir funcionalidades adicionais (por exemplo estorno ou histórico), atualizar PRD/arquitetura e dividir novas tarefas antes de executar; não usar uma tarefa de homologação para esconder implementação ampla. Preservar IDs publicados e registrar substituições futuras.

## Estados e dependências

- **pendente:** escopo suficiente para preparar/executar quando dependências forem satisfeitas; não significa iniciada.
- **bloqueada:** falta decisão, desenho técnico ou pré-requisito condicionado explicitado no detalhe.
- **em andamento / concluída:** apenas após execução real e evidências; F-001/T-001 foi concluída na execução posterior ao planejamento, conforme registro vinculado acima.

Referências de tarefa são completas: F-NNN/T-NNN. Dependências técnicas estão nas tabelas, decisões externas nos detalhes. O trabalho não possui estimativas de prazo; nenhuma foi solicitada e há incertezas relevantes de interface/identidade.

## Condição de MVP pronto

1. Núcleo financeiro e migração verificados; critérios AC-001 a AC-017 demonstrados conforme versão vigente do PRD.
2. Acesso compartilhado e gestão dos demais acessos efetivos no backend, com os quatro papéis e negativas verificadas (AC-018/019/021/022).
3. Interface web nova demonstra as jornadas e estados de AC-020, com representação monetária correta.
4. Política de exclusão, visibilidade, conflitos, moeda e operação resolvida ou explicitamente delimitada pelo responsável; nenhuma hipótese silenciosa.
5. Homologação, restauração sintética e metas acordadas verificadas; revisão técnica e aceite de produto registrados por responsáveis reais.
6. Entrega, recuperação e limitações documentadas. Publicação é ação posterior dependente de autorização específica.

Não incluir no MVP por este plano: saldo, transferências, relatórios, integrações bancárias, gestão de membros, multi-igreja ou painel administrativo genérico. Gestão dos acessos explicitamente confirmada está incluída; cadastro público e funções adicionais de conta dependem do contrato.

## Próxima tarefa elegível

F-004/T-002 pode preparar contratos independentes; F-004/T-001 foi concluída documentalmente. F-003/T-003 está concluída conforme seu handoff existente. Esta revisão não executou implementação.

## Revisão de escopo — 04/11/2026

O plano tem agora 27 tarefas: as 25 anteriores e F-004/T-008/T-009 para histórico e evolução de dados, sem migração multi-igreja. Contagens e estados nas evidências anteriores são históricos.

| Requisitos/critério vigente | Cobertura |
|---|---|
| REQ-015, AC-023/024 | F-004/T-005/T-007; F-005/T-004; F-006/T-003 |
| REQ-016, AC-025 | F-004/T-002/T-005/T-006/T-007; F-005/T-001; F-006/T-003 |
| REQ-018 a REQ-026, exceto REQ-022 retirado | Matriz detalhada de F-004/tasks.md, incluindo T-008/T-009; F-006/T-003 |
| REQ-027/028, AC-028/029 | F-004/T-002/T-004/T-007; F-005/T-005; F-006/T-003 |

REQ-017/022, AC-026/027 e F-004/AC-006 retirados do MVP; IDs preservados, sem reutilização. Histórico em docs/history/2026-11-04-decisoes-substituidas.md.
