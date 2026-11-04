# Tarefas — F-006: Aceite integrado e preparação operacional

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Fechar condições de operação e aceite | — | F-006/AC-001, F-006/AC-002 | bloqueada |
| T-002 | Preparar homologação e ensaiar operação | F-006/T-001, F-003/T-003, F-004/T-007 | AC-016, AC-017, AC-018, AC-019; F-006/AC-001 | bloqueada |
| T-003 | Executar aceite e revisão do candidato | F-006/T-002, F-005/T-005 | AC-001 a AC-022; F-006/AC-002 | bloqueada |
| T-004 | Preparar entrega e handoff operacional | F-006/T-003 | F-006/AC-002 | bloqueada |

## Detalhamento

### F-006/T-001 — Fechar condições de operação e aceite

- **Estado:** bloqueada.
- **Dependências:** —.
- **Critérios:** F-006/AC-001, F-006/AC-002.
- **Escopo e arquivos:** Obter decisões Q-005/Q-006/Q-007: carga, conflitos/reenvios, ambiente, moeda, responsáveis e metas de recuperação. Registrar operacao.md e encaminhar desenho de implantação ao arquiteto.
- **Verificação e conclusão:** Metas verificáveis ou limites explicitamente aceitos; decisões datadas; novas funções exigidas geram tarefas próprias. Bloqueio: respostas operacionais.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-006/T-002 — Preparar homologação e ensaiar operação

- **Estado:** bloqueada.
- **Dependências:** F-006/T-001, F-003/T-003, F-004/T-007.
- **Critérios:** AC-016, AC-017, AC-018, AC-019; F-006/AC-001.
- **Escopo e arquivos:** Preparar artefatos segundo arquitetura definida; ensaiar preparação única do banco, backup/restauração, carga/conflitos e acesso a logs/segredos em ambiente autorizado.
- **Verificação e conclusão:** Resultados satisfazem metas; banco sintético restaurado e conferido. Se houver contratação/publicação externa, preparar e obter autorização antes. Bloqueio: ambiente/metas e pré-requisitos.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-006/T-003 — Executar aceite e revisão do candidato

- **Estado:** bloqueada.
- **Dependências:** F-006/T-002, F-005/T-005.
- **Critérios:** AC-001 a AC-022; F-006/AC-002.
- **Escopo e arquivos:** Executar suíte, web e matriz; solicitar revisão com base/alvo identificado, resolver achados no escopo e verificar correções. Registrar evidências e obter aceite do responsável de produto.
- **Verificação e conclusão:** Todos os critérios aplicáveis demonstrados; revisão registrada sem alegar independência inexistente; aceite real, não assumido. Bloqueio: integração/homologação.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

### F-006/T-004 — Preparar entrega e handoff operacional

- **Estado:** bloqueada.
- **Dependências:** F-006/T-003.
- **Critérios:** F-006/AC-002.
- **Escopo e arquivos:** Consolidar versão, instruções, rollback, limites e responsáveis; preparar material revisável para eventual publicação posterior.
- **Verificação e conclusão:** Candidato e recuperação documentados, sem afirmar deploy realizado. Aprovação de publicação somente se ação for posteriormente solicitada e faltar autorização. Bloqueio: T-003.
- **Evidências após execução:** pendentes; registrar arquivos alterados, comandos/procedimentos, resultados e limitações em evidencias.md. A tarefa não está em andamento.

## Próxima tarefa elegível

F-006/T-001 está bloqueada pelas decisões descritas acima. Trabalho independente: F-001/T-001.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

F-006/T-003 executará também os critérios complementares acima, após F-004/T-007 e F-005/T-005; a homologação deve usar os quatro papéis em dados sintéticos da mesma igreja.
