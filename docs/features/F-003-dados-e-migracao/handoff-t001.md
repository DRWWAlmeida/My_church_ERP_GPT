# Handoff — F-003/T-001

- **Origem e destino:** desenvolvedor em investigação técnica → desenvolvedor de T-002 e revisor; nenhum outro executor acionado.
- **Estado:** pronto, contrato definido dentro da proposta arquitetural; implementação ainda pendente.
- **Pedido e escopo autorizado:** próxima tarefa elegível, investigar precedência/configuração e fechar contrato. Sem alterar produção ou executar migração real.
- **Artefatos:** [contrato-configuracao.md](contrato-configuracao.md), [evidencias.md](evidencias.md), [tasks.md](tasks.md), plano e mapa do MVP atualizados.
- **Base e alvo:** base `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo documental local desta tarefa. Alterações anteriores em aplicação/testes não pertencem a esta execução.
- **Resultado:** DATABASE como override explícito, DB_PATH como fallback compatível, resolução comum com/sem contexto; importação sem schema e preparação sob contexto antes do servidor. CFG-01 a CFG-12 detalham verificação de T-002.
- **Decisões confirmadas:** escolhas técnicas locais no escopo autorizado; não presumir aceitação dos ADRs ou produto. Sem divergência identificada da proposta arquitetural de unificação e preparação controlada.
- **Hipóteses e perguntas:** coordenação multiprocesso e servidor de produção não são resolvidos por este contrato; permanecem nas decisões operacionais.
- **Verificações:** sondagem com mocks confirmou precedência e ordem atual; 12 testes de schema/migração aprovados. Não executada suíte completa nesta etapa documental.
- **Riscos e pendências:** remover efeito de importação exige documentar preparação explícita para carregadores; não confundir uma chamada por main com garantia entre processos. T-002 implementa e verifica os cenários; T-003 ensaia recuperação.
- **Próxima ação recomendada:** F-003/T-002, ainda não iniciada. Revisar precedência/compatibilidade durante sua implementação; nova decisão ao arquiteto somente se houver divergência ou ampliação de escopo.
