# Plano — F-005: Interface web das jornadas do MVP

## Referências e abordagem

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

[Especificação](spec.md) e [tarefas](tasks.md) delimitam a execução. Reutilizar módulos e testes existentes; evitar refatoração transversal e nova funcionalidade não confirmada.

## Componentes e arquivos previstos

Existentes: `docs/architecture/overview.md`, `contracts.md`, `security.md`, `README.md`. Propostos: `desenho-web.md`, `roteiro-jornadas.md`, `evidencias.md` neste diretório; diretórios de frontend/testes ainda a definir pelo arquiteto, sem escolha de framework neste plano.

Todos os caminhos propostos são previsão, não implementação. Caminhos curtos de testes/scripts referem-se aos diretórios app/tests e app/scripts descritos no texto.

## Ordem, dependências e riscos

Seguir dependências completas em tasks.md; dependência pendente impede início da tarefa sucessora mesmo quando seu estado é pendente. Bloqueada significa também haver decisão externa ou desenho ainda indefinido.

Q-004 resolvida: web nova. Tecnologia, organização de arquivos e mecanismo de autenticação ainda pendentes; não trocar stack por iniciativa do planejador. Nenhuma migração financeira esperada; compatibilidade de identidade em F-004.

## Estratégia de verificação

Demonstrar jornadas com dados sintéticos pelo navegador e testar chamadas diretas negativas na API. Comandos de build/lint/E2E não existem no repositório: serão descobertos/definidos após escolha técnica e registrados em T-001, sem apresentar comandos hipotéticos como executados.

| Tarefa | Critérios | Evidência exigida |
|---|---|---|
| F-005/T-001 | F-005/AC-001; AC-020 | Desenho revisável das jornadas e decisão técnica registrada; partes que dependem de identidade ficam explícitas. Para concluir como pronto à implementação, contrato F-004/T-002 deve estar fechado; sem isso permanece parcial. |
| F-005/T-002 | AC-020 | Usuário autorizado percorre jornada; erros e negativa são visíveis; APIs continuam protegidas. Bloqueio: desenho e identidade. |
| F-005/T-003 | AC-020 | Cadastro→registro→busca demonstrado, valores conferem com API, vazio/erro tratados. Bloqueio: T-002. |
| F-005/T-004 | AC-020 | Jornada editada conferida na API, política de remoção e conflitos respeitada; não prometer proteção ausente. Bloqueio: T-003 e decisões Q-003/Q-005. |
| F-005/T-005 | AC-020, AC-021, AC-022 | Administrador gere acessos; Presidente, Tesoureiro e Membro não gerem acessos e usuário restrito não se autopromove; concessões/retiradas observadas na jornada e API. Bloqueio: contratos e T-004. |

## Definição de pronto

Todos os critérios aplicáveis demonstrados por evidência real; correções delimitadas verificadas; documentação/contratos sincronizados; nenhuma decisão escondida. Para funcionalidades condicionadas, respostas e contratos devem estar fechados antes de declarar entrega concluída. Registrar comandos, resultados, versão e limitações em evidencias.md; não criar esse arquivo como comprovante vazio. Revisão e aceite de produto são atos separados da execução de testes.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

T-001 desenha os quatro papéis sem seletor de igreja; T-004 cobre edição/exclusão de cadastros e lançamento; T-005 cobre gestão exclusiva do Administrador, negativas dos outros papéis e proteção do último Administrador (AC-028/029), conforme API F-004. Não apresentar permissões na interface como substituto da autorização no backend.
