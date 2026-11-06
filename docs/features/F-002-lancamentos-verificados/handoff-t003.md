# Handoff — F-002/T-003

- **Origem e destino:** desenvolvedor → revisor; nenhum agente acionado.
- **Estado:** pronto para revisão; T-003 concluída e F-002 tecnicamente finalizada.
- **Pedido e escopo autorizado:** próxima tarefa elegível, edição/exclusão/rollback; não iniciar F-003.
- **Artefatos:** `app/tests/test_lancamento.py`, [evidências](evidencias-t003.md), [tarefas](tasks.md) e mapa do MVP atualizado.
- **Base e alvo:** base Git `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo local desta tarefa: dez casos novos e reforço de preservação após atualização inválida, mais documentação. O diff acumulado contém testes anteriores de criação/busca que não pertencem a esta execução.
- **Resultado:** AC-012/013/014/015 verificados no escopo; produção já atendia aos casos e não foi alterada.
- **Decisões confirmadas:** preservar semântica PUT/PATCH, exclusão definitiva atual e mapeamento de erros. Política de exclusão compartilhada continua pendente.
- **Hipóteses e perguntas:** nenhuma regra de produto escolhida; concorrência/recuperação operacional continuam para etapas próprias.
- **Verificações:** 104 testes direcionados e 218 totais aprovados; falhas após escrita real antes do commit, leitura por nova conexão e escrita posterior demonstradas. Autoinspeção não equivale a revisão independente.
- **Riscos e pendências:** não há evidência de resistência a falha de energia ou concorrência de produção; limitações registradas nas evidências.
- **Próxima ação recomendada:** revisar entrega e executar F-003/T-001 em nova solicitação. Sem publicação ou migração real.
