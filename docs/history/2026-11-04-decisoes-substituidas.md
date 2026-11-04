# Histórico — decisões anteriores ao MVP de igreja única

Arquivado em 04/11/2026. Conteúdo abaixo substituído; não é especificação vigente. Consulte o PRD v0.6 e ADR-004. Referências e estados são os da captura anterior à revisão documental.

## docs/product/PRD.md

~~~~text
> Aprovação de 04/11/2026: orientações de ciclo de acesso confirmadas. REQ-018 a REQ-026 e F-004/AC-002 a AC-010 registrados em docs/features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md, que prevalece sobre as pendências históricas abaixo. Um papel por igreja, contas/igrejas pelo Master, suspensão local pelo administrador, recuperação por e-mail, proteção dos últimos responsáveis, revogação na próxima requisição e histórico mínimo aprovados. T-001 parcial pela retenção ainda indefinida; mapeamento real bloqueia migração real, não desenho/ensaio sintético. T-002 pode avançar nas partes independentes; nenhuma implementação realizada neste registro.

> Catálogo RBAC confirmado em 04/11/2026: Presidente e Tesoureiro — Ver, Criar/Editar e Excluir; Membro — somente Ver. Configuração pelo administrador da igreja, dentro do vínculo autorizado pelo Master. Esta decisão resolve o catálogo inicial anteriormente pendente; não concede gestão administrativa aos papéis operacionais. Matriz e verificações: docs/features/F-004-acesso-compartilhado/matriz-acesso.md. T-001 continua parcial pelas demais decisões de ciclo de contas, composição e revogação.

> Decisão posterior de 04/11/2026: Presidente é papel configurável pelo administrador da igreja, sem concessão automática por nome. Permissões por tipo de cadastro: Ler, Criar/Editar (concessão conjunta) e Excluir; Categoria é o exemplo confirmado. Substitui o acesso geral e gestão de permissões automáticos de Presidente em REQ-014/AC-021/022. Ver matriz-acesso.md da F-004. T-001 permanece parcial; edição dos cadastros deve ser incorporada ao planejamento e contrato, sem afirmar implementação existente.

> Decisão de 04/11/2026: RBAC confirmado. Master tem acesso a todas as igrejas, define vínculos de usuários e administradores. Administrador da igreja decide permissões locais. Esta decisão substitui a atribuição anterior de vínculos ao Administrador (REQ-017/AC-027). Presidente é papel configurável pelo administrador da igreja, sem acesso geral ou gestão de permissões automáticos pelo nome do papel; esta decisão substitui a concessão anterior em REQ-014/AC-021/AC-022. O catálogo completo de papéis permanece pendente. Ver docs/features/F-004-acesso-compartilhado/matriz-acesso.md. T-001 permanece parcial; nenhuma implementação realizada.

# PRD — My Church ERP: núcleo financeiro

## Estado e fontes

- Versão: 0.5 — 04/11/2026. Preserva IDs e histórico das versões anteriores.
- Complemento de 04/11/2026: restrição somente por igreja, sem subdivisão por unidade ou conta bancária. Cada usuário pode acessar as igrejas definidas pelo Administrador, inclusive várias. Q-002 e Q-008 resolvidas; esta decisão prevalece sobre referências históricas a essas pendências. Administrador e Presidente continuam podendo gerir permissões de operações; a definição de igrejas foi atribuída ao Administrador nesta resposta.
- Decisão de 04/11/2026: Administrador e Presidente podem criar e editar permissões de usuários. Lançamentos podem ser excluídos a qualquer momento por quem tiver autorização; categorias, contas bancárias (contas correntes na API) e tipos de transação (tipos de lançamento na API) só podem ser excluídos quando nenhum lançamento os utilizar. Esta atualização prevalece sobre as pendências históricas de exclusão abaixo. Criar permissões não confirma, por si só, quem cria contas de usuários.
- Estado: rascunho para validação de produto. Documentar o comportamento atual não equivale a aprová-lo para operação compartilhada.
- Base examinada: branch `feature/api-transaction`, commit `02d08b4` e arquivos locais, sem alterações de código rastreadas.
- Pedido: utilizar o projeto atual para criar o PRD, sem implementar funcionalidades ou redefinir a stack.
- Decisão confirmada pelo solicitante em 28/10/2026: **uso compartilhado; perfis ainda indefinidos**.
- Complemento do solicitante, incorporado em 29/10/2026: **interface web nova; Administrador e Presidente têm acesso geral e definem os demais acessos**. A granularidade dos demais acessos, o escopo organizacional e a política de exclusão continuam pendentes.

Fontes usadas:

| Fonte | Evidência e limite |
|---|---|
| [README](../../README.md) | Contrato documentado das APIs e migração; a introdução e a árvore de módulos estão parcialmente desatualizadas |
| [Módulos](../../app/modules/) | Comportamento implementado de categorias, contas, tipos e lançamentos; não comprova necessidade de negócio aprovada |
| [Schema](../../app/scripts/schema.py) e [migração](../../app/scripts/transaction_migration.py) | Preservação de dados, consolidação de cadastros antigos e conversão para centavos |
| [Testes](../../app/tests/) | Cenários existentes de validação; suíte não executada nesta elaboração |
| [AGENTS.md](../../AGENTS.md) | Convenções de rastreabilidade e limites de atuação |
| Conversa com o solicitante | Escopo da elaboração e confirmação de uso compartilhado |

Neste documento, **existente** significa observado no código ou descrito no README; **proposto** significa recomendação ainda não aprovada; **pendente** significa decisão necessária. Prioridades são propostas: essencial para preservar o núcleo, essencial para uso compartilhado ou posterior.

## Objetivo e problema

Consolidar o registro e a consulta de movimentações financeiras da igreja, associando cada lançamento a uma categoria, uma conta e um tipo. O resultado pretendido é permitir registros consistentes, localização por critérios e correções controladas.

Esse objetivo foi inferido das funcionalidades existentes. Não foram fornecidas entrevistas, descrição do processo manual, volume de operações ou evidências de tempo perdido. O nome ERP não implica que gestão de membros, eventos, patrimônio ou outros domínios estejam incluídos neste MVP.

O núcleo atual é uma API. O MVP incluirá uma interface web nova. Administrador e Presidente terão acesso geral e definirão os demais acessos; falta detalhar a matriz de permissões e o escopo dos registros. Acesso geral não resolve a política de exclusão definitiva nem autoriza funcionalidades fora do MVP.

### Indicadores de sucesso

| Indicador | Avaliação proposta | Estado |
|---|---|---|
| Aderência funcional | Executar os critérios deste PRD e registrar aprovação/falha por critério | Proposto; aceite final depende de validação do escopo |
| Integridade dos registros | Comparar estado antes/depois de gravações rejeitadas e de migrações inválidas | Derivado das garantias atuais |
| Controle de acesso compartilhado | Verificar as combinações permitidas e negadas da futura matriz de permissões | Pendente de definição da matriz |
| Facilidade de registrar e localizar uma movimentação | Validar as jornadas com usuários representativos | Público, método e meta ainda indefinidos |

Não há metas aprovadas de adoção, desempenho, disponibilidade ou redução de esforço.

## Usuários e jornadas

O uso por vários usuários, os perfis Administrador e Presidente e sua autoridade para definir outros acessos foram confirmados. As atividades abaixo descrevem jornadas, não novos perfis aprovados; uma mesma pessoa poderá exercer mais de uma atividade.

| Necessidade de usuário | Jornada | Dependência |
|---|---|---|
| Organizar classificações financeiras | Consultar ou criar categorias, contas e tipos antes do registro | Permissão para gerir cadastros ainda indefinida |
| Registrar uma movimentação | Selecionar os três cadastros, informar data, valor e descrição; receber o registro criado ou erro acionável | Cadastros existentes e acesso autorizado |
| Consultar movimentações | Filtrar, navegar pelas páginas e consultar um lançamento específico | Definir quem pode consultar quais registros |
| Corrigir um registro | Localizar o lançamento, substituir todos os campos ou alterar parte deles | Política de edição e concorrência pendente |
| Remover um registro | Localizar e excluir o lançamento | Exclusão definitiva existe; sua aceitação para uso compartilhado está pendente |
| Atualizar uma instalação antiga | Preparar backup, interromper uso e converter dados preservando referências | Responsável operacional e procedimento de recuperação a definir |

Não há identidade, autenticação ou autorização implementadas. A ausência atual desses controles não é uma decisão de permitir acesso público.

## Escopo

### Núcleo existente a preservar

- Criação e consulta de categorias, contas correntes e tipos de lançamento.
- Criação, consulta, atualização completa/parcial e exclusão de lançamentos.
- Validação de valores em centavos, datas, descrição e relacionamentos.
- Busca combinada, ordenação e paginação dos lançamentos.
- Respostas de sucesso e erro da API e preservação de dados nas falhas tratadas.
- Compatibilidade de dados antigos por migração transacional.

### Complementos para o MVP compartilhado

- Identificar usuários e restringir operações conforme uma matriz a detalhar, com acesso geral e gestão dos demais acessos por Administrador e Presidente.
- Definir visibilidade dos registros, política de exclusão, rastreabilidade e edição concorrente.
- Construir interface web para as jornadas do núcleo e gestão de acessos confirmada.

Esses complementos não estão implementados. Uso compartilhado, interface web e autoridade dos dois perfis estão confirmados; mecanismo de identidade, outros perfis e regras detalhadas permanecem pendentes. O núcleo existente, por si só, não caracteriza o MVP compartilhado concluído.

### Fora deste recorte

- Cálculo de saldo, transferências entre contas e interpretação contábil automática de entrada/saída, explicitamente ausentes no README.
- Edição dos três cadastros auxiliares: não disponível nesta branch e fora do escopo. Exclusão passa a integrar o MVP por REQ-015, ainda sem implementação.
- Relatórios consolidados, exportações, conciliação bancária, pagamentos, anexos e integrações externas.
- Gestão de membros, dízimos por pessoa, eventos, patrimônio e folha de pagamento.
- Suporte a múltiplas moedas e isolamento entre várias igrejas não são assumidos; dependem de decisão de escopo.

Não há roadmap posterior aprovado. Os itens acima não constituem compromissos de entrega.

### Restrições e dependências

Preservar Python/Flask e SQLite como contexto existente, sem impor troca tecnológica neste PRD. A viabilidade operacional para o volume compartilhado será avaliada após definição de carga e concorrência. Não há prazo, orçamento, hospedagem, fornecedor de identidade ou integração obrigatória informados. Novas funcionalidades dependem de decisões de produto e de planejamento posterior.

## Requisitos e regras de negócio

| ID | Comportamento ou regra | Prioridade proposta | Fonte / estado | Critérios |
|---|---|---|---|---|
| REQ-001 | Criar categorias, contas correntes e tipos com nome textual, aparado, de 3 a 100 caracteres; impedir duplicidade por nome conforme comparação atual | Essencial — núcleo | Schemas, repositórios e testes dos cadastros; existente | AC-001, AC-002 |
| REQ-002 | Consultar cada cadastro, combinando ID positivo e trecho de nome; devolver lista vazia quando não houver resultado | Essencial — núcleo | README e módulos de cadastros; existente, com lacuna de limite de ID | AC-003, AC-004 |
| REQ-003 | Criar lançamento com tipo, categoria e conta existentes, data, valor e descrição obrigatórios | Essencial — núcleo | README e módulo transaction; existente | AC-005, AC-006 |
| REQ-004 | Representar valor em centavos inteiros positivos, até 9223372036854775807, inclusive para saídas; tipo é classificação, sem efeito automático sobre saldo | Essencial — núcleo | README e schema de transaction; existente | AC-007 |
| REQ-005 | Aceitar data de calendário válida em YYYY-MM-DD, inclusive futura, e descrição aparada de 3 a 255 caracteres | Essencial — núcleo | README e schema de transaction; existente | AC-008 |
| REQ-006 | Consultar lançamento por ID e listar com filtros combináveis, paginação e ordenação determinística | Essencial — núcleo | README e módulo transaction; existente | AC-009, AC-010, AC-011 |
| REQ-007 | Permitir substituição completa e alteração parcial, mantendo os demais campos e impedindo gravação parcial inválida | Essencial — núcleo | README, repository e testes de transaction; existente | AC-012, AC-013 |
| REQ-008 | Permitir exclusão definitiva de lançamento a qualquer momento, sem limite por data, respeitando autorização; informar inexistência nas consultas posteriores | Essencial — núcleo | Confirmado pelo solicitante em 04/11/2026; DELETE existente, autorização ainda pendente | AC-014 |
| REQ-009 | Retornar respostas de API consistentes nos fluxos documentados; não expor detalhes internos em falhas operacionais | Essencial — núcleo | README e tratamento de erros; existente nos fluxos tratados, lacuna conhecida em IDs dos cadastros | AC-015, AC-004 |
| REQ-010 | Converter valores legados para centavos, preservar lançamentos, referências e sequência de IDs, e desfazer toda a operação em caso inválido | Essencial — atualização de instalações antigas | README, scripts e testes de migração; existente | AC-016, AC-017 |
| REQ-011 | Exigir identidade verificada e aplicar autorização a consultas e alterações no uso compartilhado | Essencial — uso compartilhado | Proposto a partir da decisão de uso; não implementado; perfis e método pendentes | AC-018, AC-019 |
| REQ-012 | Preservar integridade e referências em falhas de gravação e atualização, sem aceitar relacionamentos inexistentes | Essencial — núcleo | Repositórios, schema e testes; existente | AC-006, AC-013, AC-017 |
| REQ-013 | Disponibilizar interface web nova para acesso e jornadas financeiras do MVP, com estados de erro, vazio e permissão negada | Essencial — uso compartilhado | Confirmado pelo solicitante; não implementado; tecnologia pendente | AC-020 |
| REQ-014 | Permitir a Administrador e Presidente acesso geral ao escopo do MVP, criação e edição de permissões de usuários | Essencial — uso compartilhado | Confirmado pelo solicitante, complementado em 04/11/2026; matriz detalhada e ciclo de usuários pendentes | AC-021, AC-022 |
| REQ-015 | Excluir categoria, conta bancária ou tipo de transação somente quando nenhum lançamento utilizar o cadastro; preservar os lançamentos e rejeitar exclusão de cadastro vinculado | Essencial — núcleo | Confirmado pelo solicitante em 04/11/2026; não implementado | AC-023, AC-024 |

### Regras complementares e limites do contrato atual

- Cadastros usam os campos de entrada `categoria`, `conta_corrente` e `tipo_lancamento`; retornam `id` e `nome`. A comparação atual usa `NOCASE` do SQLite; equivalência Unicode ampla e tratamento de acentos não estão definidos. Não prometer que todas as variações de maiúsculas Unicode serão equivalentes.
- Campos obrigatórios de lançamento: `tipo_lancamento_id`, `categoria_id`, `conta_corrente_id`, `data`, `valor_centavos`, `descricao`. IDs no corpo devem ser inteiros positivos dentro do limite suportado; booleanos, strings e frações são rejeitados.
- Lançamentos rejeitam campos desconhecidos no corpo e parâmetros desconhecidos ou repetidos na consulta. Não estender essa garantia aos cadastros: neles, campos extras e parâmetros repetidos não têm a mesma validação.
- Filtros de lançamentos: os três IDs relacionados, `data_inicio`, `data_fim` inclusivos e trecho literal de `descricao`. Início posterior ao fim é inválido. Descrição de busca deve ter de 1 a 255 caracteres após aparar.
- Ordenação dos lançamentos: data decrescente e, no empate, ID decrescente. Página inicial 1; tamanho padrão 20 e máximo 100. Limites numéricos e deslocamento fora do suportado devem ser rejeitados.
- Busca por nome dos cadastros é parcial; o comportamento atual permite curingas de busca. Torná-la literal exigiria decisão de contrato. Resultados dos cadastros são ordenados por ID crescente e não paginados.
- Migrações de cadastros legados consolidam nomes equivalentes pela comparação atual, preservam o menor ID e redirecionam lançamentos antes de remover duplicatas. A preservação de referências deve considerar essa transformação, não exigir retenção dos IDs duplicados removidos.
- Não há restrição de duplicidade de lançamentos nem garantia de idempotência de criação: repetir uma criação válida pode gerar outro registro. Necessidade de prevenção de duplicidade em reenvios permanece aberta.

## Critérios de aceitação

São critérios para verificação posterior; sua presença não declara aprovação ou execução. Critérios propostos ou condicionais estão identificados.

| ID | Requisito | Contexto, ação e resultado observável |
|---|---|---|
| AC-001 | REQ-001 | Para cada cadastro, enviar nome válido com espaços externos; receber HTTP 201 com ID e nome aparado; consultar e encontrar o registro persistido |
| AC-002 | REQ-001 | Enviar corpo não objeto, nome ausente, não textual, em branco, com 2 ou 101 caracteres: receber 400 sem criar registro; limites de 3 e 100 são aceitos. Após criar `Oferta`, tentar `oferta`: receber 400 sem duplicar |
| AC-003 | REQ-002 | Com cadastros sintéticos, consultar sem filtro, por ID, por trecho de nome e pelos dois juntos; receber 200 com a interseção correta em ordem de ID crescente. ID inexistente ou ausência de correspondência retorna lista vazia |
| AC-004 | REQ-002, REQ-009 | Consultar cadastro com ID textual inválido, zero ou negativo: receber 400. Proposta de correção: ID acima de 9223372036854775807 também retorna 400, sem exceção interna; este último caso falha no código examinado |
| AC-005 | REQ-003 | Com os três cadastros existentes, criar lançamento válido; receber 201 com ID, data, valor, descrição e cada relação como objeto com ID e nome; a consulta individual retorna o registro |
| AC-006 | REQ-003, REQ-012 | Omitir cada campo obrigatório, enviar corpo não objeto/JSON inválido, campo desconhecido ou relação inexistente: receber 400 e manter a quantidade de lançamentos anterior |
| AC-007 | REQ-004 | Aceitar 1, 12590 e 9223372036854775807 centavos; rejeitar zero, negativo, fração, string, booleano, nulo e valor acima do limite com 400. Tipo denominado `Saída` mantém valor positivo, sem gerar saldo ou transferência |
| AC-008 | REQ-005 | Aceitar data futura válida e descrição de 3 ou 255 caracteres após aparar. Rejeitar data impossível ou formato diferente, descrição em branco, não textual, com 2 ou 256 caracteres; não persistir as tentativas inválidas |
| AC-009 | REQ-006 | Consultar ID existente e receber 200; consultar ID positivo válido inexistente e receber 404. A resposta contém as três relações identificadas |
| AC-010 | REQ-006 | Com lançamentos em datas diferentes e empatadas, combinar filtros e verificar interseção, limites inclusivos e ordem data/ID decrescente. Busca por `%` na descrição procura caractere literal. Sem correspondência ou em página além do fim, receber 200 com lista vazia |
| AC-011 | REQ-006 | Sem parâmetros de página, retornar page=1 e per_page=20; retornar total e total_pages coerentes. Rejeitar page=0, per_page=101, parâmetros repetidos/desconhecidos, filtros inválidos, intervalo invertido e deslocamento acima do limite com 400 |
| AC-012 | REQ-007 | PUT válido substitui todos os campos e retorna 200; PUT incompleto retorna 400. PATCH válido altera apenas os campos enviados; PATCH vazio ou com campo desconhecido retorna 400. Atualização com corpo válido para ID inexistente retorna 404 |
| AC-013 | REQ-007, REQ-012 | Ao alterar simultaneamente descrição e uma relação para ID inexistente, receber 400 e verificar que nenhum campo foi alterado; em falha de persistência, confirmar ausência de gravação parcial |
| AC-014 | REQ-008 | Excluir lançamento existente: receber 204 sem corpo; consulta ou nova exclusão do mesmo ID retorna 404. Critério descreve contrato atual; política de remoção no produto compartilhado depende de Q-003 |
| AC-015 | REQ-009 | Leituras e gravações bem-sucedidas, exceto DELETE, retornam JSON com status, message e data; lista de lançamentos inclui pagination. Erro de validação ou integridade retorna 400; ausência individual, 404; falha tratada de banco, 500 com mensagem genérica sem caminho interno ou SQL |
| AC-016 | REQ-010 | Em base legada sintética válida, converter 0.29→29, 1.005→101 e 125.90→12590; preservar IDs dos lançamentos e continuidade da sequência mesmo após remoção de ID alto; segunda execução não altera o resultado. Cadastros duplicados são consolidados no menor ID e referências são redirecionadas |
| AC-017 | REQ-010, REQ-012 | Em base legada com valor inválido, não positivo, arredondado a zero, acima do limite ou referência inexistente, a migração falha com rollback; comparar schema, registros e cadastros antes/depois e confirmar que não houve atualização parcial |
| AC-018 | REQ-011 | Proposto: sem identidade verificada, tentativas de consulta, criação, edição e exclusão são negadas sem revelar dados financeiros nem alterar registros. Fluxo de autenticação e respostas exatas dependem de Q-001 |
| AC-019 | REQ-011 | Condicional à matriz aprovada: testar cada combinação de perfil, operação e escopo de dados, incluindo acesso direto por ID; permitidas funcionam e negadas não revelam nem alteram registros. Não é possível declarar aceite antes de responder Q-001/Q-002 |
| AC-020 | REQ-013 | Pela interface web, uma identidade autorizada acessa o sistema, cria/consulta cadastros, registra, localiza e edita lançamento; realiza a ação de remoção somente conforme política aprovada. Erros, resultados vazios e negativas são observáveis; dados e centavos coincidem com a API. Verificar também gestão de acessos para os perfis autorizados |
| AC-021 | REQ-014 | Testar separadamente Administrador e Presidente: cada um realiza as operações aprovadas do MVP e define acessos de outro usuário conforme mecanismo e granularidade acordados; a alteração é efetivamente aplicada pela API e interface |
| AC-022 | REQ-014, REQ-011 | Usuário sem concessão não consegue executar a operação nem conceder privilégios a si mesmo por chamada direta ou payload forjado; ao retirar uma concessão, seu efeito segue a política de atualização/revogação acordada. Critério depende de fechar Q-001 |

### Critérios acrescentados em 04/11/2026

- **AC-014 (atualizado):** usuário autorizado exclui lançamento existente independentemente de sua data; recebe 204 sem corpo; consulta ou nova exclusão retorna 404. Não há prazo de exclusão.
- **AC-021 (complementado):** testar Administrador e Presidente separadamente criando e editando permissões de outro usuário; a API aplica as concessões definidas.
- **AC-023 — REQ-015:** para cada um dos três cadastros, usuário autorizado exclui registro sem vínculos; o registro deixa de aparecer nas consultas. A exclusão de um lançamento não exclui automaticamente seus cadastros; após remover o último vínculo, a exclusão do cadastro torna-se permitida.
- **AC-024 — REQ-015/012:** para cada cadastro com um ou mais lançamentos vinculados, rejeitar exclusão sem alterar cadastro ou lançamentos. Verificar disputa entre criação/edição de lançamento e exclusão do cadastro, impedindo referências órfãs e remoção em cascata.

### Isolamento confirmado em 04/11/2026

- **REQ-016:** isolar categorias, contas, tipos e lançamentos por igreja. Dentro da igreja autorizada, não subdividir visibilidade por unidade ou conta; permissões por operação continuam aplicáveis. Acesso geral de Administrador/Presidente não implica acesso automático entre igrejas.
- **AC-025 — REQ-016/011:** com duas igrejas sintéticas, verificar que identidade autorizada apenas na primeira não consulta, altera ou exclui recursos da segunda por listas, ID ou parâmetros forjados; totais e relações também ficam isolados. Na primeira, não filtrar visibilidade por conta ou unidade.
- **AC-026 — REQ-016/012:** rejeitar lançamento com categoria, conta ou tipo de outra igreja, sem gravação parcial; verificar isolamento também na exclusão de cadastros e na gestão de permissões.
- **REQ-017:** permitir que o Administrador defina as igrejas acessíveis a cada usuário, com múltiplos vínculos possíveis. O usuário só acessa igrejas concedidas e não pode ampliar seu próprio escopo. Este requisito não concede automaticamente ao Presidente a gestão dos vínculos entre usuário e igreja.
- **AC-027 — REQ-017/016:** Administrador concede igrejas A e B a usuário sintético; usuário acessa ambas conforme permissões de operação, mas não C, nem por ID ou contexto forjado. Tentativa de alterar os próprios vínculos sem autoridade é rejeitada. Usuário sem vínculos não recebe acesso a dados financeiros. A retirada de vínculo deve impedir novos acessos conforme política técnica de revogação a fechar em F-004/T-002.

## Requisitos não funcionais

| Referência | Condição / meta | Forma de avaliação | Estado |
|---|---|---|---|
| REQ-004 — exatidão monetária | Valores armazenados e retornados em centavos inteiros, conforme limites definidos | AC-007 e AC-016 | Existente; não implica suporte multimoeda |
| REQ-012 — integridade | Nenhuma gravação parcial nos cenários de falha definidos | AC-006, AC-013 e AC-017 | Garantia a verificar pela suíte |
| REQ-009 — erros | Não expor caminhos internos ou SQL nas falhas operacionais tratadas | Injetar falhas em ambiente isolado; AC-015 | Há testes existentes; limite de ID conhecido deve ser corrigido |
| REQ-011 — acesso | Permissões aplicadas também a acesso direto às APIs e aos IDs | AC-018 e AC-019 | Proposto; regras e implementação pendentes |
| Desempenho e capacidade | Quantidade de usuários simultâneos, volume e latência aceitável não definidos | Definir carga representativa e medir após Q-005 | Meta pendente, sem número inventado |
| Disponibilidade e recuperação | Janela aceitável de interrupção e perda de dados não definidas | Definir rotina de backup e ensaio de restauração após Q-006 | README exige backup/parada para migração, mas não define serviço operacional |
| Rastreabilidade e retenção | Necessidade de histórico, autoria e prazo de retenção ainda não definidos | Definir evidência de alterações e exclusões após Q-003 | Pendência relevante para uso compartilhado |
| Usabilidade | Canal e tarefas representativas não definidos | Avaliar jornadas após Q-004 | API existente; interface de usuário não localizada |

## Verificação e rastreabilidade existente

| Requisitos | Evidência disponível | Limite |
|---|---|---|
| REQ-001, REQ-002 | `app/tests/test_categoria.py`, `test_conta_corrente.py`, `test_tipo_lancamento.py` | Não cobre todos os limites propostos; IDs muito grandes causam OverflowError |
| REQ-003 a REQ-009, REQ-012 | `app/tests/test_lancamento.py` | Existência dos testes não garante cobertura de todos os critérios nem sucesso de execução |
| REQ-010, REQ-012 | `app/tests/test_schema.py`, `test_transaction_migration.py` | Testes usam dados isolados; banco local não foi migrado nem inspecionado |
| REQ-011 | Nenhuma implementação/teste localizado | Depende de decisões de acesso |

Na análise anterior desta sessão, `python -m pytest -q` não executou porque o alias de Python estava inacessível; o Python 3.14 encontrado diretamente não tinha pytest. Foi reproduzido, com bancos em memória, o OverflowError nas três consultas de cadastros para ID acima do limite. Este PRD não declara testes aprovados nem revisão independente concluída.

O [plano até o MVP](../features/README.md) vincula requisitos e critérios às entregas F-001 a F-006. IDs anteriores foram preservados; tarefas futuras não representam funcionalidades implementadas.

## Riscos, hipóteses e perguntas abertas

O solicitante é a interlocução atual; responsáveis de negócio e operação não foram designados. Perguntas não respondidas não autorizam escolhas implícitas.

| ID | Pergunta ou hipótese | Impacto e trabalho dependente | Estado |
|---|---|---|---|
| Q-001 | Quais são os demais acessos, sua granularidade, quem provisiona usuários e como concessões/revogações entram em vigor? | Matriz de autorização, autenticação e REQ-011/014 | Parcial: Administrador e Presidente têm acesso geral e definem os demais acessos; detalhes pendentes |
| Q-002 | Todos os usuários compartilham os mesmos registros ou há restrições por igreja, unidade ou conta? | Visibilidade, propriedade dos dados e isolamento | Resolvida em 04/11/2026: restrição somente por igreja, sem subdivisão por unidade ou conta |
| Q-008 | Um usuário pode acessar uma ou várias igrejas? Quem cria e altera esses vínculos? | Identidade, seleção de contexto e gestão de acessos | Resolvida em 04/11/2026: usuário acessa as igrejas definidas pelo Administrador, com múltiplos vínculos possíveis. Não concede acesso global automático nem atribui ao Presidente gestão desses vínculos |
| Q-003 | É preciso motivo, autoria ou histórico de alterações/exclusões? | Rastreabilidade e retenção | Parcialmente resolvida em 04/11/2026: exclusão definitiva de lançamentos a qualquer momento e exclusão de cadastros somente sem vínculos confirmadas. Histórico e retenção não foram definidos; estorno não foi solicitado |
| Q-004 | O uso será por cliente de API já existente ou exige interface web? | Entrega utilizável e REQ-013 | Resolvida: interface web nova. Tecnologia e contratos de identidade dependem de desenho técnico |
| Q-005 | Quantos usuários simultâneos e registros são esperados? Como tratar edições concorrentes e reenvios de criação? | Capacidade, conflitos e prevenção de duplicidade | Pendente; não prometer proteção contra sobrescrita concorrente |
| Q-006 | Onde será operado, quem fará backup e qual perda/interrupção é aceitável? | Hospedagem, recuperação e disponibilidade | Pendente |
| Q-007 | BRL será a única moeda? Tipos continuarão livres ou terão significado fixo de entrada/saída? | Evolução de valores, saldo e relatórios; sem mudança do contrato atual até decisão | BRL aparece em exemplo do README; exclusividade não confirmada |
| H-001 | Pessoas responsáveis pelas finanças são o público principal | Validar jornadas e vocabulário antes de fechar o MVP | Hipótese derivada do domínio |

Riscos concretos: uso compartilhado ainda sem controles de acesso; política de exclusão sem validação de negócio; suite não executada; entrada numérica de ID sem limite nos cadastros; configuração do banco com chaves `DB_PATH` e `DATABASE` distintas. A documentação inicial do README diverge dos módulos atuais, e README/GIT_GUIDELINES divergem sobre a branch de origem. Esses pontos devem ser tratados no planejamento apropriado, sem converter ajustes técnicos em novas funcionalidades de produto.

## Decisões e alterações

| Data | Decisão ou alteração | Fonte | Impacto |
|---|---|---|---|
| 28/10/2026 | Criar o primeiro PRD a partir do projeto atual | Pedido do solicitante | Consolida REQ-001 a REQ-012 e AC-001 a AC-019; sem alterações de código |
| 28/10/2026 | O primeiro uso será compartilhado; perfis ainda indefinidos | Resposta explícita do solicitante | REQ-011 proposto e Q-001 a Q-006; não define permissões automaticamente |
| 28/10/2026 | Separar contrato atual de propostas e pendências | Organização desta versão pelo analista | Não atribui aprovação de produto a comportamentos herdados |
| 29/10/2026 | Incorporar resposta do solicitante: interface web nova; Administrador e Presidente com acesso geral e definição dos demais acessos | Resposta explícita durante planejamento, incorporada nesta data | REQ-013/014, AC-020 a AC-022, Q-004 resolvida e Q-001 parcialmente resolvida; versão 0.2, sem escolha de frontend ou permissões adicionais |

Documentos posteriores devem preservar os IDs e resolver as perguntas antes de assumir permissões, isolamento, exclusão ou metas operacionais. Não há aprovação final de produto registrada. O [handoff](handoff-prd.md) descreve o que pode avançar e as dependências restantes.

~~~~

## docs/features/F-004-acesso-compartilhado/matriz-acesso.md

~~~~text
# Matriz RBAC — F-004

Data: 04/11/2026. Fonte: decisão explícita do solicitante. Estado: parcial.

| Autoridade | Escopo e responsabilidade confirmados |
|---|---|
| Master | Acesso a todas as igrejas; define vínculos de usuários e administrador de cada igreja. |
| Administrador da igreja | Define permissões dos usuários naquela igreja. A autoridade local não concede acesso administrativo a outras igrejas. |
| Presidente | Papel configurável pelo administrador da igreja; exerce somente as permissões concedidas no contexto daquela igreja. |
| Usuário | Acessa igrejas concedidas pelo Master, com permissões locais conforme papéis. |

RBAC associa permissões a papéis e papéis a usuários no escopo aplicável. Os papéis são configurados pelo administrador da igreja. Ver e Ler representam a mesma permissão; Criar/Editar é uma única concessão. Um único papel operacional por usuário em cada igreja; pode variar entre igrejas. Não presumir concessões individuais adicionais.

## Papéis operacionais confirmados

Fonte: lista explícita do solicitante em 04/11/2026, posterior às decisões acima. Esta matriz resolve a pendência de catálogo inicial de papéis.

| Papel | Ver | Criar/Editar | Excluir |
|---|---|---|---|
| Presidente | Sim | Sim | Sim |
| Tesoureiro | Sim | Sim | Sim |
| Membro | Sim | Não | Não |

As concessões valem dentro da igreja autorizada e não conferem gestão de vínculos, nomeação de administradores ou autoridade Master. A configuração continua sob responsabilidade do administrador da igreja. A exclusão de cadastro permanece condicionada à ausência de lançamentos vinculados. O contrato deve mapear as concessões aos recursos e rotas do MVP, incluindo a edição de cadastros ainda pendente de implementação.

A decisão atual substitui a gestão de vínculos anteriormente atribuída ao Administrador em REQ-017/AC-027. Múltiplas igrejas por usuário continuam permitidas. A decisão posterior do solicitante torna Presidente um papel configurável pelo administrador: o nome do papel não concede acesso geral nem gestão de permissões automaticamente. Esta regra substitui as concessões automáticas anteriores de REQ-014/AC-021/AC-022 para Presidente.

## Verificação esperada

- Master acessa duas igrejas, define seus administradores e concede/retira vínculos.
- Administrador altera permissões na igreja que administra; tentativa sem autoridade em outra igreja é negada.
- Usuário só executa ações concedidas por papel dentro de igreja autorizada; chamadas diretas e papéis forjados não ampliam acesso.
- Administração local não permite conceder Master nem criar vínculos globais.
- Presidente com permissão de leitura consegue consultar; uma ação sem concessão é negada, mesmo que o papel se chame Presidente. Permissões concedidas em uma igreja não se propagam a outra.
- Na matriz confirmada, Presidente e Tesoureiro conseguem ver, criar/editar e excluir recursos autorizados, respeitando regras de integridade. Membro consegue ver; criação, edição e exclusão são negadas sem efeito, inclusive por chamada direta.

## Pendências

Ciclo de contas, composição, criação de igrejas, Master, revogação e histórico mínimo aprovados em decisoes-ciclo-acesso.md. Restam retenção do histórico, mapeamento real do legado e contrato técnico.

## Handoff

- **Origem e destino:** orquestrador/analista → arquitetura e planejamento; sem executor delegado.
- **Estado:** parcial, T-001 ainda não concluída.
- **Pedido e escopo autorizado:** registrar RBAC e hierarquia global/local.
- **Artefatos:** este documento e notas no PRD, spec, plan, tasks e arquitetura afetada.
- **Resultado:** autoridade e catálogo inicial de Presidente, Tesoureiro e Membro registrados; contrato técnico permanece pendente.
- **Decisões confirmadas:** declaração do solicitante de 04/11/2026.
- **Hipóteses e perguntas:** pendências acima; catálogo operacional não presumido.
- **Verificações:** inspeção documental; testes não executados; código não alterado.
- **Riscos e pendências:** completar composição de papéis e ciclo de contas antes de concluir contrato.
- **Próxima ação recomendada:** resolver as pendências restantes de T-001; depois concluir T-002.

~~~~

## docs/features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md

~~~~text
# Decisões confirmadas — ciclo de acesso F-004

Data: 04/11/2026. Fonte: aprovação explícita «pode seguir essa orientação», referente às propostas apresentadas nesta conversa. Este documento prevalece sobre pendências históricas equivalentes. Registro de requisitos; não comprova implementação.

## Regras e verificações

| ID | Regra confirmada | Verificação de aceite |
|---|---|---|
| REQ-018 | Um papel operacional por usuário em cada igreja; papéis diferentes entre igrejas são permitidos. | F-004/AC-002: impedir dois papéis operacionais simultâneos no mesmo vínculo; permitir Tesoureiro em A e Membro em B sem propagação de permissões. |
| REQ-019 | Master cadastra/convida contas e define igrejas; administrador atribui papel local. Sem cadastro público. Sem papel local não há acesso financeiro, ressalvadas autoridades Master/administrador já confirmadas. | F-004/AC-003: usuário sem papel operacional e sem autoridade administrativa não acessa dados; administrador não cria vínculo global. |
| REQ-020 | Master desativa conta globalmente ou retira vínculos; administrador suspende somente acesso à sua igreja. Preservar registros e autoria. | F-004/AC-004: suspensão em A não bloqueia B; desativação global bloqueia ambas. |
| REQ-021 | Recuperação por e-mail, com link temporário de uso único; usuário define senha. Administração pode iniciar envio, sem escolher/visualizar senha e dentro de seu escopo. | F-004/AC-005: link expirado ou reutilizado falha; recuperação não reativa conta nem concede papel/vínculo. |
| REQ-022 | Somente Master cria igrejas e indica administrador; igreja precisa de administrador ativo para operar. | F-004/AC-006: usuário local não cria igreja; igreja sem administrador não entra em operação. |
| REQ-023 | Primeiro Master provisionado na instalação por procedimento restrito, sem senha padrão. Master existente concede novos Masters com confirmação de identidade e registro. Contas pessoais; segundo Master permitido. | F-004/AC-007: impedir retirada/desativação do último Master ativo; impedir perda do último administrador ativo sem substituição, inclusive em alterações concorrentes. |
| REQ-024 | Revogação vale na próxima requisição, sem novo login. Escrita em andamento revalida autoridade antes de confirmar. Operação já confirmada permanece registrada. | F-004/AC-008: sessão aberta perde acesso após revogação; escrita que perde autorização antes de confirmar é revertida. |
| REQ-025 | Histórico mínimo registra autor, data, igreja quando aplicável, ação e registro afetado, cobrindo alterações financeiras, exclusões e gestão de acesso. Interface comum não edita histórico. Exclusão mantém identificador e motivo, sem cópia completa do conteúdo excluído. | F-004/AC-009: mutação confirmada tem evento correspondente; falha não produz evento de sucesso; exclusão remove conteúdo operacional sem copiá-lo integralmente para histórico; segredos não são registrados. |
| REQ-026 | Legado exige inventário e associação explícita a igrejas. Migração ensaiada em cópia, preservando IDs/referências, conferindo quantidades/valores e restauração. | F-004/AC-010: mapeamento ambíguo/incompleto bloqueia migração definitiva; ensaio sintético valida integridade e recuperação. |

IDs REQ complementam o PRD; critérios F-004/AC são locais, preservando IDs existentes do produto. Para eventos globais, como concessão de Master, igreja é não aplicável; isso não deve descartar o evento.

## Pendências reais

- Prazo de retenção e descarte do histórico ainda não escolhido. Não presumir retenção eterna nem criar rotina automática de descarte antes dessa definição.
- Associação dos registros reais às igrejas depende de inventário e confirmação dos responsáveis. Pode-se desenhar e testar a migração com dados sintéticos sem essa entrada.
- Contrato técnico T-002: endpoints, autenticação, expiração dos links/sessões, entrega de e-mail, persistência, atomicidade da revogação/histórico, migração e recuperação. Decisões técnicas serão propostas em arquitetura.

## Impacto no planejamento

T-001: matriz, composição, autoridade e ciclo de contas confirmados; fechamento permanece parcial pela retenção. O mapeamento real bloqueia a execução sobre legado, não o desenho técnico. T-002 pode avançar no contrato independente dessa entrada, explicitando a retenção pendente. T-003 cobre identidade/recuperação; T-004 cobre gestão global/local e proteção dos últimos responsáveis; T-005/T-006 incorporam histórico e isolamento; T-007 demonstra os critérios acima. Decompor migração e auditoria em tarefas explícitas antes da implementação.

## Handoff

- **Origem e destino:** orquestrador/analista → arquitetura e planejamento; sem executor delegado.
- **Estado:** parcial; regras aprovadas, retenção e contrato pendentes.
- **Pedido e escopo autorizado:** seguir orientações de produto aprovadas; nenhuma operação externa ou migração real autorizada por este registro.
- **Artefatos:** este documento, matriz-acesso.md e referências no PRD/spec/plan/tasks e diagnóstico.
- **Resultado:** REQ-018 a REQ-026 e F-004/AC-002 a AC-010 rastreiam as decisões às verificações e tarefas.
- **Decisões confirmadas:** aprovação do solicitante nesta conversa em 04/11/2026.
- **Hipóteses e perguntas:** retenção e mapeamento real permanecem sem valores presumidos.
- **Verificações:** inspeção documental, estado do Git e conferência de alterações; testes de comportamento não executados.
- **Riscos e pendências:** T-002 ainda não fechado; nenhuma implementação comprovada.
- **Próxima ação recomendada:** fechar contrato técnico e decompor auditoria/migração; obter retenção e mapeamento antes das operações dependentes.

~~~~

## docs/architecture/isolamento-igrejas.md

~~~~text
> Decisão de 04/11/2026: RBAC confirmado. Master tem acesso a todas as igrejas, define vínculos de usuários e administradores. Administrador da igreja decide permissões locais. Esta decisão substitui a atribuição anterior de vínculos ao Administrador (REQ-017/AC-027). Presidente é papel configurável pelo administrador da igreja, sem acesso geral ou gestão de permissões automáticos pelo nome do papel; esta decisão substitui a concessão anterior em REQ-014/AC-021/AC-022. O catálogo completo de papéis permanece pendente. Ver docs/features/F-004-acesso-compartilhado/matriz-acesso.md. T-001 permanece parcial; nenhuma implementação realizada.

# Isolamento por igreja

Data: 04/11/2026. Fontes: respostas do solicitante «Restrição somente por igrejas» e «O usuário poderá acessar as igrejas definidas pelo administrador», [PRD v0.5](../product/PRD.md), REQ-016/017 e AC-025/026/027. Fronteira e múltiplos vínculos definidos pelo Administrador confirmados; desenho abaixo proposto, sem implementação.

## Acesso e contratos

Igreja é a fronteira de propriedade de categorias, contas, tipos e lançamentos. Não subdividir visibilidade por unidade ou conta. Permissões por operação continuam aplicáveis. Administrador e Presidente gerem permissões dentro de seu escopo autorizado; não recebem acesso automático a outras igrejas.

O servidor deriva o escopo de identidade e vínculos persistidos. Igreja enviada pelo cliente, caso haja seleção de contexto, é solicitação a validar, não prova de autorização. Listas, contagens, consulta por ID, alterações e exclusões usam o mesmo escopo confiável, passado explicitamente aos repositórios. Relações do lançamento são verificadas na transação e devem pertencer à mesma igreja.

Proposta: recurso fora do escopo retorna 404 sem revelar existência; referência inexistente ou de outra igreja retorna o mesmo erro genérico 400. Respostas de identidade ausente e ação negada serão fechadas em F-004/T-002. Nenhum controle está implementado nesta etapa.

## Dados e evolução propostos

Acrescentar igreja e igreja_id obrigatório em todos os cadastros financeiros e lançamentos. Preservar IDs, restringir unicidade de nomes à igreja e avaliar chaves compostas para garantir no banco a mesma igreja entre lançamento e referências. Fechar DDL e índices no contrato de identidade.

Modelar relação muitos-para-muitos usuario_igreja com par (usuario_id, igreja_id) único e referências obrigatórias. Administrador define esses vínculos; gestão de permissões de operações por Presidente não lhe concede implicitamente gestão dos vínculos. O escopo de igrejas que cada Administrador pode conceder e o provisionamento inicial devem ser explicitados no contrato, sem inferir autoridade global.

Proposta de interface: listar apenas igrejas concedidas e permitir selecionar a igreja ativa. Seleção não agrega dados entre igrejas nem altera vínculos; agregação não foi solicitada. Usuário sem vínculos não acessa dados financeiros. A API valida igreja ativa e permissão da operação em cada requisição. Proposta de revogação: consultar vínculo vigente por requisição e negar novas requisições após sua retirada, sem depender de encerramento de sessão; comportamento de operações já em andamento deve constar do contrato transacional.

Dados legados não possuem igreja: obter associação explícita antes de migração, sem atribuição arbitrária. Preparar backup e ensaio sintético, interromper escritas durante transformação e validar IDs, contagens, nomes e relações antes de confirmar. Recuperação deve restaurar banco e aplicação compatível; não presumir downgrade seguro após novas escritas. Nenhuma migração real autorizada.

A exclusão de cadastros continua condicionada à ausência de lançamentos vinculados, sem cascata, conforme [exclusao-e-permissoes.md](exclusao-e-permissoes.md).

## Handoff

- **Origem e destino:** arquiteto → planejador e solicitante; nenhum executor acionado.
- **Estado:** parcial; fronteira, cardinalidade e responsável pelos vínculos confirmados; contrato de identidade ainda incompleto.
- **Pedido e escopo autorizado:** registrar isolamento somente por igrejas, sem implementar código.
- **Artefatos:** este documento, PRD v0.5 e notas nos documentos de arquitetura e planejamento.
- **Resultado:** Q-002 e Q-008 resolvidas; REQ-016/017 e AC-025/026/027 registrados.
- **Decisões confirmadas:** respostas do solicitante de 04/11/2026; sem restrição por unidade ou conta; múltiplas igrejas por usuário definidas pelo Administrador.
- **Hipóteses e perguntas:** granularidade de permissões, ciclo de identidade, provisionamento inicial e autoridade de concessão do Administrador continuam a detalhar. Não presumir atribuição de vínculos ao Presidente.
- **Verificações:** inspeção documental; testes de isolamento, migração e acesso ainda não executados.
- **Riscos e pendências:** banco legado sem propriedade; tarefas de migração/isolamento ainda devem ser decompostas. Validar duas igrejas, IDs conhecidos, parâmetros forjados, contagens, vínculos cruzados, permissões e exclusões.
- **Próxima ação recomendada:** completar F-004/T-001 com granularidade e ciclo de usuários; T-002 fecha schema/contratos/migração; T-004/T-005/T-006/T-007 incorporam AC-025/026/027. F-005 deve planejar seleção entre igrejas autorizadas e gestão dos vínculos pelo Administrador.

~~~~

## docs/architecture/pendencias-F-004.md

~~~~text
> Aprovação de 04/11/2026: orientações de ciclo de acesso confirmadas. REQ-018 a REQ-026 e F-004/AC-002 a AC-010 registrados em docs/features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md, que prevalece sobre as pendências históricas abaixo. Um papel por igreja, contas/igrejas pelo Master, suspensão local pelo administrador, recuperação por e-mail, proteção dos últimos responsáveis, revogação na próxima requisição e histórico mínimo aprovados. T-001 parcial pela retenção ainda indefinida; mapeamento real bloqueia migração real, não desenho/ensaio sintético. T-002 pode avançar nas partes independentes; nenhuma implementação realizada neste registro.

> Catálogo RBAC confirmado em 04/11/2026: Presidente e Tesoureiro — Ver, Criar/Editar e Excluir; Membro — somente Ver. Configuração pelo administrador da igreja, dentro do vínculo autorizado pelo Master. Esta decisão resolve o catálogo inicial anteriormente pendente; não concede gestão administrativa aos papéis operacionais. Matriz e verificações: docs/features/F-004-acesso-compartilhado/matriz-acesso.md. T-001 continua parcial pelas demais decisões de ciclo de contas, composição e revogação.

> Decisão posterior de 04/11/2026: Presidente é papel configurável pelo administrador da igreja, sem concessão automática por nome. Permissões por tipo de cadastro: Ler, Criar/Editar (concessão conjunta) e Excluir; Categoria é o exemplo confirmado. Substitui o acesso geral e gestão de permissões automáticos de Presidente em REQ-014/AC-021/022. Ver matriz-acesso.md da F-004. T-001 permanece parcial; edição dos cadastros deve ser incorporada ao planejamento e contrato, sem afirmar implementação existente.

> Decisão de 04/11/2026: RBAC confirmado. Master tem acesso a todas as igrejas, define vínculos de usuários e administradores. Administrador da igreja decide permissões locais. Esta decisão substitui a atribuição anterior de vínculos ao Administrador (REQ-017/AC-027). Presidente é papel configurável pelo administrador da igreja, sem acesso geral ou gestão de permissões automáticos pelo nome do papel; esta decisão substitui a concessão anterior em REQ-014/AC-021/AC-022. O catálogo completo de papéis permanece pendente. Ver docs/features/F-004-acesso-compartilhado/matriz-acesso.md. T-001 permanece parcial; nenhuma implementação realizada.

# Verificação de prontidão — F-004

Data: 04/11/2026. Estado: diagnóstico concluído; implementação bloqueada por decisões de produto e contrato técnico incompleto. Referências: [PRD](../product/PRD.md), [tarefas](../features/F-004-acesso-compartilhado/tasks.md), [isolamento](isolamento-igrejas.md) e [exclusões](exclusao-e-permissoes.md).

## Base examinada

HEAD `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, mais o estado local com alterações preexistentes. Inspeção documental e de `app/__init__.py`, `app/api/__init__.py`, `app/scripts/schema.py`, `app/modules/category/routes.py`, `app/modules/transaction/services.py` e `app/tests/conftest.py`. Nenhum banco real foi aberto. Este diagnóstico não é revisão independente nem execução de testes.

F-001/T-003, F-002/T-003 e F-003/T-003 estão concluídas nos respectivos quadros; os resultados históricos não foram reexecutados nesta inspeção. O diretório F-004 contém apenas spec, plan e tasks: matriz-acesso.md e contrato-identidade.md ainda não existem. A aplicação registra somente módulos financeiros e erros; o schema não contém identidade ou igreja, e os serviços examinados não recebem contexto de acesso.

## Decisões já confirmadas

- Interface web nova; Administrador e Presidente têm acesso geral dentro do escopo autorizado e podem criar/editar permissões (REQ-013/014).
- Isolamento somente por igreja, incluindo categorias, contas, tipos e lançamentos; sem subdivisão por unidade ou conta (REQ-016, Q-002 resolvida).
- Um usuário pode acessar várias igrejas, com vínculos definidos pelo Administrador. Presidente não recebeu implicitamente autoridade para gerir esses vínculos (REQ-017, Q-008 resolvida).
- Lançamentos podem ser excluídos definitivamente sem prazo. Cadastros só podem ser excluídos sem lançamentos vinculados (REQ-008/015). Isso não concede exclusão a qualquer usuário.

Esses pontos não precisam de nova confirmação. Acesso geral não concede acesso automático a todas as igrejas.

## Decisões de produto ainda necessárias — T-001

| Pendência | Decisão necessária | Impacto |
|---|---|---|
| Granularidade | Permissões individuais ou agrupadas? Variam por igreja? Quais ações de cada módulo podem ser concedidas? | Matriz de AC-019/021/022 e persistência das concessões |
| Autoridade administrativa | Quem nomeia/remove Administradores e Presidentes? Papel é global ou por igreja? Que igrejas um Administrador pode conceder? | Evitar elevação de privilégio e concessão fora do escopo; AC-027 |
| Ciclo de contas | Quem cria/desativa contas e inicia recuperação? Há convite, cadastro público ou provisionamento administrativo? Como se estabelece o primeiro responsável? | Primeiro acesso, recuperação e rotas de gestão |
| Gestão de igrejas | Quem cria igrejas e atribui seu primeiro Administrador? | Provisionamento sem pressupor autoridade global |
| Efeito da retirada | Retirada de vínculo/permissão e desativação devem impedir a próxima requisição? Qual comportamento esperado para operações já iniciadas? | Critérios observáveis de revogação e concorrência |
| Histórico | Autoria, motivo e histórico de alterações/exclusões fazem parte desta entrega? Se sim, quais eventos e retenção? | Q-003 permanece parcialmente aberta; afeta schema e fronteiras transacionais |
| Dados existentes | Qual associação explícita vincula os registros legados às igrejas? | Migração real; não atribuir uma igreja arbitrária |

As perguntas pertencem ao analista/solicitante; sugestões anteriores não são respostas confirmadas. A associação dos dados reais não impede desenhar e testar uma migração com mapeamento sintético explícito, mas impede executá-la sobre o legado sem esse mapeamento.

## Definições técnicas ainda necessárias — T-002

São trabalho de arquitetura, não perguntas de implementação a transferir automaticamente ao usuário. O método de sessão/token, em particular, pode ser proposto pelo arquiteto após conhecer o fluxo de conta; o usuário não precisa escolher JWT ou cookie.

| Área | Entrega necessária |
|---|---|
| Identidade | Decidir mecanismo adequado ao cliente web, identificador de login, expiração, encerramento, recuperação e invalidação; definir proteção contra abuso e, conforme mecanismo, CSRF e armazenamento de credenciais/segredos. Registrar alternativas e decisão em ADR. |
| API | Fechar endpoints, payloads, respostas e validações para identidade, contexto de igreja, contas, permissões e vínculos. Definir 401/403 e regra uniforme de 404 fora do escopo; referências inválidas/externas sem revelar existência. |
| Contexto interno | Definir contexto confiável recebido pelos serviços, checagem de ação e escopo obrigatório nos repositórios; nunca aceitar papel ou vínculo do payload como prova de autoridade. |
| Persistência | Fechar DDL de usuários, igrejas, vínculos, concessões e mecanismo de identidade escolhido; igreja_id obrigatório nos dados financeiros, unicidade de nomes por igreja e integridade das relações dentro da mesma igreja. |
| Transações | Especificar consistência entre autorização e escrita, revogação concorrente, alterações de privilégios e proteção contra perda do último acesso administrativo, conforme regra de produto. |
| Migração | Definir versão, mapeamento explícito, ordem de conversão, preservação de IDs/referências/sequências, validação, rollback e restauração pós-commit; adaptar o preparo repetido do schema. |
| Testes/compatibilidade | Migrar fixtures para identidades sintéticas, sem bypass global, e documentar quebra de compatibilidade com clientes anônimos e schema antigo. Preparar evidências por critério e célula da matriz. |

Não há seleção de biblioteca, algoritmo ou parâmetros de segurança nesta inspeção. Detalhes dependentes de versão deverão ser conferidos na documentação oficial ao fechar o contrato.

## Lacunas concretas do planejamento

1. Spec e plan ainda dizem que Q-002 está pendente; os detalhes de T-001 também repetem perguntas de escopo e exclusão já resolvidas. As notas recentes prevalecem, mas os textos precisam ser consolidados, inclusive ADR-003.
2. T-005 menciona GET/POST, mas precisa incluir os DELETE dos três cadastros previstos na atualização arquitetural e AC-023/024 do PRD. Não há autorização para acrescentar edição de cadastros apenas porque uma matriz genérica contenha a ação editar.
3. AC-025/026/027 precisam constar na rastreabilidade das tarefas, com entregas explícitas para migração, contexto ativo, múltiplos vínculos e isolamento. As notas atuais não substituem essa decomposição.
4. `schema.py` consolida nomes e cria unicidade global. Apenas adicionar igreja_id seria insuficiente: a preparação repetida poderia juntar cadastros homônimos de igrejas diferentes. Conversão, índices e consolidação precisam evoluir juntos, com teste de reinicialização.
5. A frase final de tasks.md recomenda F-001/T-001, que já está concluída. A próxima ação é resolver T-001 da F-004, não reiniciar funcionalidades anteriores.
6. AC-021 inclui efeito na interface. A F-004 deve evidenciar a API e registrar a parcela visual dependente da F-005, sem declarar aceite integral do critério antes dessa integração.

## Condições para liberar as tarefas

| Tarefa | Pendência para iniciar/concluir |
|---|---|
| T-001 | Respostas de produto registradas com fonte e matriz coerente com REQ-014/016/017. Continua bloqueada. |
| T-002 | Matriz fechada; produzir contrato implementável, ADR e estratégia de migração. Desenho preliminar pode avançar sem apresentar hipóteses como aprovadas. |
| T-003 | T-002 concluída. F-003/T-003 já está concluída no quadro. Implementar identidade e negativas anônimas conforme contrato. |
| T-004 | T-003 e contrato de autoridade; incluir ciclo de concessões e vínculos de igrejas, sem atribuir sua gestão ao Presidente por inferência. |
| T-005 | T-004 e schema com isolamento; F-001/T-003 já concluída. Cobrir consultas, criação e DELETE dos cadastros. |
| T-006 | T-005; F-002/T-003 já concluída. Aplicar ação e igreja a lista/contagem/ID/escrita e validar relações na transação. |
| T-007 | Implementação anterior e suíte autenticada: duas igrejas ou mais, usuário multivínculo, usuário sem vínculos, cada perfil geral, concessões negativas, IDs/contextos forjados, referências cruzadas, revogação e regressão financeira. |

O planejador deve decompor migração/isolamento antes das tarefas que dependem do novo schema, preservando IDs existentes das tarefas ou registrando a extensão explicitamente. Não liberar uma versão intermediária como MVP protegido enquanto algum caminho financeiro ignorar a política.

## Handoff

- **Origem e destino:** arquiteto → analista/solicitante para decisões de comportamento; depois arquiteto e planejador. Nenhum outro executor acionado.
- **Estado:** pronto como diagnóstico; F-004 continua bloqueada para implementação conforme sequência atual.
- **Pedido e escopo autorizado:** verificar pendências da F-004; sem implementação, dependências ou migração.
- **Artefatos:** este documento, novo no diff local contra a base identificada acima. Arquivos preexistentes preservados.
- **Resultado:** separação de decisões confirmadas, perguntas de produto, lacunas técnicas e condições por T-001 a T-007; rastreabilidade para REQ-011/014/015/016/017 e critérios associados.
- **Decisões confirmadas:** as registradas no PRD e nos complementos de arquitetura, discriminadas acima. Nenhuma decisão de negócio nova presumida.
- **Hipóteses e perguntas:** matriz, ciclo de contas, autoridade, retirada de acesso, histórico e associação do legado ainda precisam das definições indicadas.
- **Verificações:** leitura dos documentos/código citados, `git status --short`, `git rev-parse HEAD` e inventário da F-004. Inspeção documental; não foram executados testes nem acessados dados reais.
- **Riscos e pendências:** contrato ausente, consolidação global incompatível com isolamento, tarefas desatualizadas e dependência da interface para aceite integral de AC-021.
- **Próxima ação recomendada:** responder as decisões de produto de T-001; fechar T-002 e consolidar o planejamento com migração/isolamento antes de implementar T-003 a T-007. Não é necessária nova autorização para decisões já confirmadas.

~~~~
