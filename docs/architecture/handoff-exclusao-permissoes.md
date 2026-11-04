> Handoff histórico: decisões de escopo e acesso abaixo foram substituídas na revisão de 04/11/2026. Consulte [handoff vigente](../handoff-igreja-unica.md). Evidências anteriores não foram reexecutadas.

# Handoff — regras de exclusão e permissões

- **Origem e destino:** arquiteto → planejador técnico; sem executor acionado.
- **Estado:** parcial; decisões do solicitante registradas, identidade completa depende das perguntas restantes.
- **Pedido e escopo autorizado:** incorporar regras de permissões e exclusão, sem implementar aplicação.
- **Artefatos:** [PRD v0.3](../product/PRD.md), [atualização arquitetural](exclusao-e-permissoes.md), notas em overview.md, contracts.md e planejamento de F-004/mapa do MVP.
- **Resultado:** REQ-008/014 atualizados; REQ-015 e AC-023/024 acrescentados; contrato técnico de exclusão proposto com integridade transacional e sem cascata.
- **Decisões confirmadas:** mensagem do solicitante de 04/11/2026; ambos os perfis criam/editam permissões, lançamentos podem ser excluídos a qualquer momento, cadastros somente sem lançamentos vinculados.
- **Hipóteses e perguntas:** não equiparar criação de permissões a provisionamento de contas. Granularidade, escopo, revogação e histórico continuam indefinidos.
- **Verificações:** inspeção documental e de rastreabilidade; sem executar testes, aplicação ou migrações. Contratos propostos não constituem funcionalidades disponíveis.
- **Riscos e pendências:** planejamento anterior não contém tarefas próprias para exclusão dos cadastros; requisitos de autorização e operação continuam parciais.
- **Próxima ação recomendada:** decompor REQ-015 em tarefas de API, autorização e web; completar decisões restantes de F-004/T-001 para fechar identidade em T-002. Nenhuma autorização de deploy concedida.
