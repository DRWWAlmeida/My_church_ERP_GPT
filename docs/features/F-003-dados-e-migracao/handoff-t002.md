# Handoff — F-003/T-002

- **Origem e destino:** desenvolvedor → revisão técnica; nenhum revisor acionado.
- **Estado:** pronto para revisão da implementação; incidente no banco local permanece sem avaliação de dados ou recuperação.
- **Pedido e escopo autorizado:** próxima tarefa elegível, F-003/T-002; alinhar configuração e preparação do banco, testar e documentar.
- **Artefatos:** app/core/database.py, app/run.py, app/tests/test_database_config.py, README.md, docs/architecture/overview.md e documentação de F-003. Base `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo é o diff local desses arquivos, inclusive novos, sem commit. Mudanças de tarefas anteriores coexistem no workspace.
- **Resultado:** precedência DATABASE/DB_PATH respeitada; schema e API usam o mesmo destino; importação sem conexão/migração; main prepara no contexto da aplicação e falha antes de servir.
- **Decisões confirmadas:** contrato de T-001 aplicado sem alterar stack, factory, DDL ou regras de negócio.
- **Hipóteses e perguntas:** nenhuma nova decisão de produto necessária para T-002. Não é possível inferir preservação de dados no incidente inicial apenas por hash.
- **Verificações:** 22 testes específicos e 240 testes totais aprovados; diff sem erros de whitespace. Comandos e cobertura CFG-01 a CFG-12 em [evidências](evidencias-t002.md).
- **Riscos e pendências:** uma importação durante a primeira execução de teste acionou o schema antigo no banco local e seu hash mudou. Proteção adicionada aos testes e efeito removido do entrypoint; hash estável na suíte final. Nenhuma restauração tentada. Revisão independente pendente. WSGI exige preparação explícita antes dos processos.
- **Próxima ação recomendada:** F-003/T-003, ensaio sintético de migração e recuperação. Não equivale a autorização para recuperação do banco local ou deploy.

Este documento transfere contexto; não inicia outra tarefa ou agente.
