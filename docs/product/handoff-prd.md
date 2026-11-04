> Handoff histórico: decisões de escopo e acesso abaixo foram substituídas na revisão de 04/11/2026. Consulte [handoff vigente](../handoff-igreja-unica.md). Evidências anteriores não foram reexecutadas.

# Handoff — Requisitos do núcleo financeiro

- **Origem e destino:** analista de requisitos → arquiteto de software; nenhum executor da próxima etapa designado ou acionado.
- **Estado:** parcial quanto à validação de produto; PRD v0.1 redigido, com uso compartilhado confirmado e decisões de acesso/operacionais pendentes.
- **Pedido e escopo autorizado:** criar PRD usando o projeto atual; sem implementar aplicação ou definir arquitetura detalhada.
- **Artefatos:** [PRD.md](PRD.md), versão 0.1 de 28/10/2026, baseado na branch `feature/api-transaction`, commit `02d08b4`.
- **Resultado:** núcleo financeiro documentado em REQ-001 a REQ-012 e AC-001 a AC-019, com jornadas, exclusões, fontes, riscos e evidências existentes. Não foram criadas tarefas de implementação.
- **Decisões confirmadas:** o solicitante pediu uso do projeto atual como base e confirmou uso compartilhado, com perfis ainda indefinidos. Nenhuma aprovação global dos requisitos foi inferida.
- **Hipóteses e perguntas:** H-001 e Q-001 a Q-007 no PRD; acesso, visibilidade de dados, exclusão, interface, concorrência, operação e moeda precisam de definição. Responsáveis de negócio/operacionais não designados.
- **Verificações:** confronto documental com README, rotas, schemas e testes; inspeção de referências e rastreabilidade do PRD. A suíte não foi executada nesta etapa. A análise anterior registrou ausência de pytest no interpretador disponível e reproduziu o limite inválido de IDs em bases isoladas.
- **Riscos e pendências:** ausência de autenticação/autorização; política de exclusão não validada para uso compartilhado; limite de IDs dos cadastros; divergências de configuração e documentação. O banco existente permaneceu intacto.
- **Próxima ação recomendada:** validar com o solicitante a matriz de acesso e o escopo de visibilidade (Q-001/Q-002), a política de remoção/histórico (Q-003) e o canal de uso (Q-004). Uma futura etapa de arquitetura pode mapear o núcleo existente e suas garantias; decisões finais de identidade, isolamento, concorrência e operação dependem das respostas. Nenhuma implementação, publicação ou migração foi autorizada por este handoff.

Este documento transfere contexto; não comprova aprovação de produto nem início da próxima etapa.
