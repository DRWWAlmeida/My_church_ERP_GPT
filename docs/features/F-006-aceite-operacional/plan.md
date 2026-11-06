# Plano — F-006: Aceite integrado e preparação operacional

## Referências e abordagem

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: PRD, arquitetura, README, configuração/entrypoint e testes. Propostos: `operacao.md`, `evidencias.md` neste diretório, arquivos de servidor/homologação e teste de carga a definir após desenho técnico; nenhuma ferramenta escolhida por suposição.

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Q-005/Q-006/Q-007 pendentes. Se produto exigir novo mecanismo de conflito, idempotência, auditoria ou multimoeda, revisar requisitos e decompor tarefas antes de implementação. Não ocultar expansão de escopo em tarefa de homologação.

## Estratégia de verificação

`python -m pytest` no commit candidato; executar verificações da web que forem definidas, jornadas e matriz de acesso em ambiente isolado. Ensaiar carga/conflitos e backup/restauração conforme metas acordadas. Registrar revisor, base/alvo e aceite do responsável de produto.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-006/T-001 | F-006/AC-001, F-006/AC-002 | Metas verificáveis ou limites explicitamente aceitos; decisões datadas; novas funções exigidas geram tarefas próprias. Bloqueio: respostas operacionais. |
| F-006/T-002 | AC-016, AC-017, AC-018, AC-019; F-006/AC-001 | Resultados satisfazem metas; banco sintético restaurado e conferido. Se houver contratação/publicação externa, preparar e obter autorização antes. Bloqueio: ambiente/metas e pré-requisitos. |
| F-006/T-003 | AC-001 a AC-022; F-006/AC-002 | Todos os critérios aplicáveis demonstrados; revisão registrada sem alegar independência inexistente; aceite real, não assumido. Bloqueio: integração/homologação. |
| F-006/T-004 | F-006/AC-002 | Candidato e recuperação documentados, sem afirmar deploy realizado. Aprovação de publicação somente se ação for posteriormente solicitada e faltar autorização. Bloqueio: T-003. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

F-006/T-003 executará também os critérios complementares acima, após F-004/T-007 e F-005/T-005; a homologação deve usar os quatro papéis em dados sintéticos da mesma igreja.
