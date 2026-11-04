# Handoff — F-002/T-001

- **Origem e destino:** desenvolvedor → revisor; nenhum outro executor acionado.
- **Estado:** pronto para revisão; tarefa concluída, F-002 ainda parcial.
- **Pedido e escopo autorizado:** próxima tarefa elegível, verificar criação e limites de lançamentos; sem avançar para T-002.
- **Artefatos:** `app/tests/test_lancamento.py`, [evidencias.md](evidencias.md), [tasks.md](tasks.md) e mapa do MVP atualizado.
- **Base e alvo:** base Git `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo local desta tarefa: alterações de testes de lançamentos e documentos indicados. Alterações anteriores de F-001 não fazem parte desta execução.
- **Resultado:** AC-005/006/007/008 demonstrados por testes existentes/ampliados; seis novos casos e asserções de preservação de registros. Produção não precisou de correção.
- **Decisões confirmadas:** manter limites e regras do PRD, incluindo datas futuras e valor positivo para Saída.
- **Hipóteses e perguntas:** nenhuma nova decisão de negócio; pendências do MVP preservadas.
- **Verificações:** 80 testes direcionados e 194 totais passaram; inspeção do diff e documentação. Não houve falha nova reproduzida nem revisão independente.
- **Riscos e pendências:** T-002/T-003 não executadas; não extrapolar cobertura de criação para aceite de busca, edição ou concorrência.
- **Próxima ação recomendada:** revisar a entrega e executar F-002/T-002 na próxima solicitação. Não houve publicação ou alteração do banco real.
