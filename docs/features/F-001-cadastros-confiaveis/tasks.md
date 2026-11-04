# Tarefas — F-001: Cadastros confiáveis

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

## Sequência

| ID | Entrega | Dependências | Critérios | Estado |
|---|---|---|---|---|
| T-001 | Preparar ambiente e registrar baseline | — | AC-001, AC-002, AC-003, AC-004, AC-015 (pré-requisito) | concluída |
| T-002 | Rejeitar IDs fora do limite nos cadastros | F-001/T-001 | AC-003, AC-004 | concluída |
| T-003 | Verificar criação, busca e erros dos cadastros | F-001/T-002 | AC-001, AC-002, AC-003, AC-015 | concluída |

## Detalhamento

### F-001/T-001 — Preparar ambiente e registrar baseline

- **Estado:** concluída em 29/10/2026. Ambiente isolado preparado e baseline executado: 152 testes passaram; dependências verificadas com pip check.
- **Dependências:** —.
- **Critérios:** AC-001, AC-002, AC-003, AC-004, AC-015 (pré-requisito).
- **Escopo e arquivos:** Validar interpretador, criar/usar ambiente isolado, instalar requirements-dev.txt nas versões atuais; inspecionar fixtures e executar `python -m pytest`. Arquivos: README se precisar corrigir instrução e evidencias.md proposto; nenhum código de produção.
- **Verificação e conclusão:** Resultado real da suíte registrado, inclusive falhas, versões e comando exato; não precisa corrigir todas as falhas para concluir baseline. Se instalação falhar, registrar bloqueio de ambiente; não executar app.run.
- **Evidências após execução:** [evidencias.md](evidencias.md) registra ambiente, comandos, versões, resultados e limitações; [handoff de T-001](handoff-t001.md) delimita a revisão. Nenhum código de produção ou teste alterado.

### F-001/T-002 — Rejeitar IDs fora do limite nos cadastros

- **Estado:** concluída em 30/10/2026. Regressão reproduzida antes da correção; 78 testes dos cadastros e 164 da suíte completa aprovados após a correção.
- **Dependências:** F-001/T-001.
- **Critérios:** AC-003, AC-004.
- **Escopo e arquivos:** Ajustar schemas dos três módulos e testes correspondentes; usar core.validators somente se necessário à correção. Preservar comportamento válido.
- **Verificação e conclusão:** Teste reproduz falha anterior; limite máximo é aceito como filtro e máximo+1, inteiro muito longo, zero, negativo e texto inválido retornam 400 estruturado sem OverflowError.
- **Evidencias:** [evidencias-t002.md](evidencias-t002.md); [handoff](handoff-t002.md). Regressao reproduzida e suite completa aprovada.

### F-001/T-003 — Verificar criação, busca e erros dos cadastros

- **Estado:** concluída em 30/10/2026. Falha de exposição reproduzida e corrigida; 102 testes direcionados e 188 totais aprovados.
- **Dependências:** F-001/T-002.
- **Critérios:** AC-001, AC-002, AC-003, AC-015.
- **Escopo e arquivos:** Completar lacunas relevantes dos testes existentes; corrigir fallback de integridade de category.repository que inclui detalhe SQLite, conforme proposta arquitetural. Atualizar documentação afetada.
- **Verificação e conclusão:** Testes do plano passam para criação 201, duplicidade/validação 400, consulta 200/lista vazia e erro operacional genérico 500. Evidência por critério registrada; sem handler universal novo fora do contrato.
- **Evidências após execução:** [evidencias-t003.md](evidencias-t003.md) e [handoff-t003.md](handoff-t003.md). Inclui regressão, cobertura por critério e base/alvo de revisão.

## Próxima tarefa elegível

F-001 não possui tarefas pendentes. Pela ordem sugerida do MVP, a próxima é F-002/T-001 — Verificar criação e limites de dados; F-003/T-001 também tem seu pré-requisito satisfeito. Nenhuma delas foi iniciada nesta execução.

