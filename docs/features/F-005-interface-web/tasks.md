# Tarefas — F-005: Interface web das jornadas do MVP

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Especificar jornadas e arquitetura da interface | F-004/T-002 | F-005/AC-001; AC-020 | bloqueada |
| T-002 | Entregar acesso e cadastros pela web | F-005/T-001, F-004/T-007 | AC-020 | bloqueada |
| T-003 | Entregar registro e busca de lançamentos | F-005/T-002 | AC-020 | bloqueada |
| T-004 | Entregar edição e remoção aprovada | F-005/T-003 | AC-020 | bloqueada |
| T-005 | Entregar gestão dos demais acessos pela web | F-005/T-004, F-004/T-004 | AC-020, AC-021, AC-022 | bloqueada |

## Detalhamento

### F-005/T-001 — Especificar jornadas e arquitetura da interface

- **Estado:** bloqueada.
- **Dependências:** F-004/T-002. O mapeamento preliminar de estados pode avançar sem essa dependência; o desenho pronto para implementação não pode ser concluído sem o contrato de identidade.
- **Critérios:** F-005/AC-001; AC-020.
- **Escopo e arquivos:** Mapear telas/estados mínimos e obter desenho técnico do arquiteto para web integrada ao projeto; registrar proposta em desenho-web.md, paths e comandos. Integrar contrato de identidade de F-004/T-002 quando disponível; pode produzir estados independentes antes dele.
- **Verificação e conclusão:** Desenho revisável das jornadas e decisão técnica registrada; partes que dependem de identidade ficam explícitas. Para concluir como pronto à implementação, contrato F-004/T-002 deve estar fechado; sem isso permanece parcial.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-005/T-002 — Entregar acesso e cadastros pela web

- **Estado:** bloqueada.
- **Dependências:** F-005/T-001, F-004/T-007.
- **Critérios:** AC-020.
- **Escopo e arquivos:** Implementar entrada/saída do sistema e criação/consulta dos três cadastros nos caminhos aprovados; validação, vazio e falhas. Comandos segundo desenho-web.md.
- **Verificação e conclusão:** Usuário autorizado percorre jornada; erros e negativa são visíveis; APIs continuam protegidas. Bloqueio: desenho e identidade.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-005/T-003 — Entregar registro e busca de lançamentos

- **Estado:** bloqueada.
- **Dependências:** F-005/T-002.
- **Critérios:** AC-020.
- **Escopo e arquivos:** Implementar seleção de relações, data/valor/descrição, confirmação, consulta individual, filtros e paginação. Testar limites monetários sem arredondamento silencioso no cliente.
- **Verificação e conclusão:** Cadastro→registro→busca demonstrado, valores conferem com API, vazio/erro tratados. Bloqueio: T-002.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-005/T-004 — Entregar edição e remoção aprovada

- **Estado:** bloqueada.
- **Dependências:** F-005/T-003.
- **Critérios:** AC-020.
- **Escopo e arquivos:** Implementar edição com estados de erro e ação de remoção conforme Q-003; comportamento de conflito conforme Q-005. Arquivos da interface e testes definidos em T-001.
- **Verificação e conclusão:** Jornada editada conferida na API, política de remoção e conflitos respeitada; não prometer proteção ausente. Bloqueio: T-003 e decisões Q-003/Q-005.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-005/T-005 — Entregar gestão dos demais acessos pela web

- **Estado:** bloqueada.
- **Dependências:** F-005/T-004, F-004/T-004.
- **Critérios:** AC-020, AC-021, AC-022.
- **Escopo e arquivos:** Implementar fluxo específico de definição/retirada de acessos para Administrador, usando operações da API; sem painel administrativo genérico.
- **Verificação e conclusão:** Administrador gere acessos; Presidente, Tesoureiro e Membro não gerem acessos e usuário restrito não se autopromove; concessões/retiradas observadas na jornada e API. Bloqueio: contratos e T-004.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

## Próxima tarefa elegível

F-005/T-001 aguarda F-004/T-002 para concluir o desenho. O levantamento preliminar das jornadas é independente, mas não desbloqueia implementação. A próxima tarefa global é F-001/T-001.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

T-001 desenha os quatro papéis sem seletor de igreja; T-004 cobre edição/exclusão de cadastros e lançamento; T-005 cobre gestão exclusiva do Administrador, negativas dos outros papéis e proteção do último Administrador (AC-028/029), conforme API F-004. Não apresentar permissões na interface como substituto da autorização no backend.
