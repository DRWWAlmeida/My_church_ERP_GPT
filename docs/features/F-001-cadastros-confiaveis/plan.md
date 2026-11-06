# Plano — F-001: Cadastros confiáveis

## Referências e abordagem

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: `app/modules/category/`, `checking_account/`, `transaction_type/`, `app/core/validators.py`, testes dos três cadastros, `README.md`. Propostos: `.venv/` local ignorado pelo Git e `evidencias.md` neste diretório.

Atualização de execução de T-003: acrescentado `app/tests/test_cadastros_contract.py` para verificar garantias comuns aos três cadastros sem duplicar o mesmo teste em três arquivos. Resultados em [evidencias-t003.md](evidencias-t003.md).

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Sem migração. O alias Python falhou e pytest não estava no interpretador direto durante a análise anterior. Não instalar globalmente nem atualizar dependências gerais. Não há autorização de commit/merge implícita.

## Estratégia de verificação

`python -m pytest app/tests/test_categoria.py app/tests/test_conta_corrente.py app/tests/test_tipo_lancamento.py`, no interpretador validado. Usar fixtures isoladas e injeção de falhas, nunca o banco local.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-001/T-001 | AC-001, AC-002, AC-003, AC-004, AC-015 (pré-requisito) | Resultado real da suíte registrado, inclusive falhas, versões e comando exato; não precisa corrigir todas as falhas para concluir baseline. Se instalação falhar, registrar bloqueio de ambiente; não executar app.run. |
| F-001/T-002 | AC-003, AC-004 | Teste reproduz falha anterior; limite máximo é aceito como filtro e máximo+1, inteiro muito longo, zero, negativo e texto inválido retornam 400 estruturado sem OverflowError. |
| F-001/T-003 | AC-001, AC-002, AC-003, AC-015 | Testes do plano passam para criação 201, duplicidade/validação 400, consulta 200/lista vazia e erro operacional genérico 500. Evidência por critério registrada; sem handler universal novo fora do contrato. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.

