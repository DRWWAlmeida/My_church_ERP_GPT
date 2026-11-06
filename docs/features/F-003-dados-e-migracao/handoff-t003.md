# Handoff — F-003/T-003

- **Origem e destino:** desenvolvedor → revisão independente, sem executor designado.
- **Estado:** pronto para revisão; critérios demonstrados pela suíte.
- **Pedido e escopo autorizado:** implementar F-003/T-003, completar cobertura de migração/rollback e ensaiar recuperação sintética após commit.
- **Artefatos e alvo:** diff local de `app/tests/test_transaction_migration.py`, adição ao README, atualização de `tasks.md`, `spec.md`, `evidencias.md` e novos `recuperacao-sintetica.md` e `handoff-t003.md` em F-003. Base HEAD `02d08b416781d977693bcb97c4bab3ca89e4c9ab`. Já havia alterações locais de outras tarefas; foram preservadas e não integram esta entrega.
- **Resultado:** AC-016 cobre consolidação conjunta no menor ID, referências, arredondamento, sequência e idempotência integral; AC-017 compara schema, todas as linhas e sequências após falhas; F-003/AC-002 demonstra restauração de backup em arquivo após conversão confirmada por nova conexão.
- **Decisões confirmadas:** escopo da tarefa e contrato de configuração existente; nenhuma alteração em código de produção necessária.
- **Hipóteses e perguntas:** ensaio sem concorrência, com dados sintéticos; estratégia operacional real continua fora do escopo.
- **Verificações:** suíte completa com diretório temporário exclusivo: 243 passed in 4.61s; `git diff --check` sem erros. Comandos e incidente de permissão em `evidencias.md`.
- **Riscos e pendências:** revisão independente e aceite de produto não realizados; sem recuperação real ou RPO/RTO. Nenhum deploy, push ou migração real executado.
- **Próxima ação recomendada:** revisar o diff delimitado e a rastreabilidade dos critérios. Este handoff não inicia outra etapa.
