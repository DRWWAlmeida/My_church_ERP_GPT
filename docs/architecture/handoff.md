> Handoff histórico: decisões de escopo e acesso abaixo foram substituídas na revisão de 04/11/2026. Consulte [handoff vigente](../handoff-igreja-unica.md). Evidências anteriores não foram reexecutadas.

# Handoff — Arquitetura do núcleo financeiro

- **Origem e destino:** arquiteto de software → planejador técnico; nenhum executor da próxima etapa acionado.
- **Estado:** pronto como documentação da arquitetura atual; parcial para desenho final do uso compartilhado por depender de Q-001 a Q-007 do PRD.
- **Pedido e escopo autorizado:** ler o PRD e documentar a arquitetura; sem implementar aplicação, mudar dependências ou executar migrações.
- **Artefatos:** [overview.md](overview.md), [data-model.md](data-model.md), [contracts.md](contracts.md), [security.md](security.md), [ADR-001](decisions/ADR-001-monolito-modular.md), [ADR-002](decisions/ADR-002-centavos-e-transacoes.md), [ADR-003](decisions/ADR-003-acesso-compartilhado.md). Base `02d08b4`, PRD v0.1; documentos de 28/10/2026.
- **Resultado:** REQ-001 a REQ-010 e REQ-012 mapeados ao núcleo existente, sem alegar todos os critérios satisfeitos. REQ-011 mapeado a pontos de integração propostos; sem controle de acesso atual. Dados, contratos, atomicidade, migração e recuperação descritos.
- **Decisões confirmadas:** preservar contexto atual para documentação e uso compartilhado com perfis indefinidos, conforme PRD. ADRs são propostas de continuidade/evolução, não aceitações novas.
- **Hipóteses e perguntas:** retornar Q-001/Q-002/Q-003/Q-004 ao analista/solicitante para perfis, escopo, exclusão e interface. Q-005/Q-006/Q-007 afetam capacidade, recuperação e moeda. Não inventar perfis ou organização proprietária dos dados.
- **Verificações:** inspeção de factory, configuração, módulos, erros, scripts, manifestos e testes existentes; consulta oficial de transações/tipos SQLite e implantação Flask. Links e rastreabilidade documental conferidos. Não foi executada suíte, aplicação ou migração; versão SQLite de implantação e desempenho não verificados.
- **Riscos e pendências:** ausência de identidade, limite inválido de IDs nos cadastros, chaves de configuração divergentes, tratamento de erro não universal, migração na importação do entrypoint, concorrência sem controle de versão, POST sem idempotência, DELETE sem histórico e rotina de recuperação ainda não validada.
- **Próxima ação recomendada:** em etapa posterior, planejar correções delimitadas de validação/configuração e testes de contrato com REQ/AC rastreáveis. Pode avançar o planejamento do núcleo preservado e dos pontos de integração de acesso. Fechamento de permissões, isolamento, schema de identidade e contratos de conflito exige decisões do produto. Não há tarefas ou estimativas de implementação criadas nesta etapa.

Este handoff não inicia planejamento, aprova produto ou autoriza publicação, alteração em produção ou migração.
