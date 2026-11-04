> Handoff histórico: decisões de escopo e acesso abaixo foram substituídas na revisão de 04/11/2026. Consulte [handoff vigente](../handoff-igreja-unica.md). Evidências anteriores não foram reexecutadas.

# Handoff — Planejamento até o MVP

- **Origem e destino:** planejador técnico → desenvolvedor para F-001/T-001; analista/solicitante e arquiteto para decisões condicionantes. Nenhum executor foi acionado.
- **Estado:** pronto para iniciar verificação do núcleo; parcial para o caminho final do MVP, por depender de permissões detalhadas, escopo de dados, exclusão, desenho web/identidade e operação.
- **Pedido e escopo autorizado:** analisar projeto e definir tarefas até o MVP; produzir planejamento sem implementar.
- **Artefatos:** [mapa do MVP](README.md), seis conjuntos spec/plan/tasks, [PRD v0.2](../product/PRD.md) com decisões recentes incorporadas e notas de contexto na arquitetura. Base de código `02d08b4`.
- **Resultado:** 25 tarefas com dependências, critérios, arquivos previstos e verificações; cobertura de REQ-001 a REQ-014 e AC-001 a AC-022. Nenhuma tarefa concluída por inferência da existência do código.
- **Decisões confirmadas:** web nova; Administrador e Presidente com acesso geral e definição dos demais acessos; uso compartilhado. Não são escolhas de mecanismo de identidade ou tecnologia frontend.
- **Hipóteses e perguntas:** Q-001 parcialmente resolvida; Q-002/Q-003/Q-005/Q-006/Q-007 pendentes. Q-004 resolvida quanto ao canal; desenho técnico pendente. Não assumir acesso entre organizações ou exclusão irrestrita.
- **Verificações:** inspeção de PRD, arquitetura, templates, manifests, configuração, fixtures e inventário de testes; checagem documental de links, cobertura, IDs e dependências. Suíte não executada nesta etapa; a limitação anterior de ambiente é entrada para F-001/T-001.
- **Riscos e pendências:** ambiente sem pytest validado, limite de IDs dos cadastros, configuração divergente, acesso ainda ausente, interface ainda ausente, operação sem metas. Alterações de exclusão ou conflito exigem critérios e tarefas antes de implementação.
- **Próxima ação recomendada:** executar [F-001/T-001](F-001-cadastros-confiaveis/tasks.md) usando [spec](F-001-cadastros-confiaveis/spec.md) e [plan](F-001-cadastros-confiaveis/plan.md). Dependências documentais satisfeitas; ambiente será investigado. Registrar baseline real e então seguir correções delimitadas. Trabalho de acesso/interface permanece condicionado aos contratos; não há deploy autorizado.

Este handoff transfere contexto, não inicia implementação nem comprova aprovação de produto ou revisão independente.
