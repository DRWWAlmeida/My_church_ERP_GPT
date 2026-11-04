# Plano — F-004: Identidade, permissões e gestão de acessos

## Referências e abordagem

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: `docs/product/PRD.md`, `docs/architecture/security.md`, `contracts.md`, `decisions/ADR-003-acesso-compartilhado.md`; `app/api/__init__.py`, `app/modules/*/{routes,services,repository}.py`, `app/errors.py`, `app/scripts/schema.py`, `app/tests/conftest.py`. Propostos condicionais: `app/modules/identity/`, `app/tests/test_access.py`, `app/tests/test_permissions.py`; nomes finais dependem do desenho de identidade. `matriz-acesso.md`, `contrato-identidade.md` e `evidencias.md` propostos neste diretório.

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Q-002/Q-008 resolvidas: igreja única, sem vínculos entre igrejas. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão definidos; contrato técnico permanece pendente. T-002 pode avançar nas partes independentes. Migração/recuperação de identidade e histórico deve constar do contrato antes de código; não há associação multi-igreja a realizar.

## Estratégia de verificação

Após desenho aprovado, `python -m pytest`, com identidades sintéticas dos quatro papéis em uma única igreja. Exercitar chamadas diretas por ID, contagens, referências inválidas, concessão/revogação e tentativa de elevação de privilégio; preservar regressões do núcleo.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-004/T-001 | F-004/AC-001; AC-018, AC-019, AC-021, AC-022 | Matriz, políticas e retenção eterna do histórico confirmadas. Tarefa documental pode ser concluída; contrato técnico e implementação seguem em T-002/T-008. |
| F-004/T-002 | F-004/AC-001; AC-018, AC-019, AC-021, AC-022 | Contrato de API e migração/recuperação de dados suficiente para implementar; caminhos propostos confirmados e tarefas repartidas se necessário. Bloqueio: matriz e decisão arquitetural. |
| F-004/T-003 | AC-018 | Chamadas financeiras sem identidade válida são negadas sem dados/efeito; login e fim de acesso seguem contrato. Bloqueio: contrato técnico. Entrega intermediária não deve ser publicada como MVP. |
| F-004/T-004 | AC-021, AC-022 | Administrador define acessos; usuário sem concessão não concede a si próprio nem falsifica papel. Efeito de retirada demonstrado conforme prazo/política acordados. Bloqueio: contrato. |
| F-004/T-005 | AC-019, AC-021, AC-022 | Matriz dos cadastros demonstrada e concessões efetivas; nenhum filtro do cliente amplia escopo. Bloqueio: identidade e regras. |
| F-004/T-006 | AC-019, AC-021, AC-022 | Negativas não alteram dados nem revelam contagem/nomes; cada um dos quatro papéis exerce somente suas operações autorizadas. Q-003 pode exigir replanejamento de exclusão. Bloqueio: matriz e política. |
| F-004/T-007 | AC-018, AC-019, AC-021, AC-022 | Evidência por célula e por critério; sem bypass global de autorização nos testes. Bloqueio: implementação anterior. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.

## Cobertura revisada

As extensões T-008/T-009 e os critérios adicionais por tarefa estão em [tasks.md](tasks.md). T-007 depende também de histórico e ensaio de recuperação. Não implementar Master, igreja_id, vínculos ou seletor de igreja. T-005 inclui contratos e implementação de edição/exclusão dos cadastros. Sem execução de testes nesta revisão documental.
