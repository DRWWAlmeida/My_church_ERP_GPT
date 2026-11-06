# Plano — F-002: Ciclo financeiro verificado

## Referências e abordagem

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: `app/modules/transaction/`, `app/tests/test_lancamento.py`. Proposto: `evidencias.md` neste diretório. Atualizar contratos apenas para esclarecer resultados, sem alterar decisões de produto.

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Sem migração prevista. Mudança de contrato exige retorno ao analista/arquiteto. Q-003 permanece para exclusão compartilhada; Q-005 para conflitos/reenvios.

## Estratégia de verificação

`python -m pytest app/tests/test_lancamento.py`; ciclo com dados sintéticos, limites e falhas injetadas. Não replicar testes existentes que já demonstram os critérios.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-002/T-001 | AC-005, AC-006, AC-007, AC-008 | Critérios demonstrados; criação válida persiste e toda rejeição mantém estado anterior. Evidências identificam código/testes alterados. |
| F-002/T-002 | AC-009, AC-010, AC-011 | Lista e total corretos, páginas vazias 200, ID ausente 404 e consultas inválidas 400; registrar resultados. |
| F-002/T-003 | AC-012, AC-013, AC-014, AC-015 | Estado anterior preservado em falha; contrato atual de exclusão demonstrado sem aprovar uso compartilhado; suíte da funcionalidade passa. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.

