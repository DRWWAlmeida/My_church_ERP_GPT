# PRD — My Church ERP: núcleo financeiro

## Estado e fontes

- Versão: 0.6 — 04/11/2026. MVP de igreja única; IDs anteriores preservados, inclusive os retirados.
- Estado: rascunho para validação de produto. Documentar o comportamento atual não equivale a aprová-lo para operação compartilhada.
- Base examinada: branch `feature/api-transaction`, commit `02d08b4` e arquivos locais, sem alterações de código rastreadas.
- Pedido: utilizar o projeto atual para criar o PRD, sem implementar funcionalidades ou redefinir a stack.

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

O núcleo atual é uma API. O MVP incluirá interface web nova para uma única igreja, com RBAC e exatamente quatro papéis: Administrador, Presidente, Tesoureiro e Membro. Administrador gere contas, nomeia Administradores e configura permissões. Presidente e Tesoureiro têm Ver, Criar/Editar e Excluir conforme configuração; Membro tem somente Ver. Não há papel Master nem gestão ou seleção de múltiplas igrejas.

### Indicadores de sucesso

| Indicador | Avaliação proposta | Estado |
|---|---|---|
| Aderência funcional | Executar os critérios deste PRD e registrar aprovação/falha por critério | Proposto; aceite final depende de validação do escopo |
| Integridade dos registros | Comparar estado antes/depois de gravações rejeitadas e de migrações inválidas | Derivado das garantias atuais |
| Controle de acesso compartilhado | Verificar as combinações permitidas e negadas da futura matriz de permissões | Pendente de definição da matriz |
| Facilidade de registrar e localizar uma movimentação | Validar as jornadas com usuários representativos | Público, método e meta ainda indefinidos |

Não há metas aprovadas de adoção, desempenho, disponibilidade ou redução de esforço.

## Usuários e jornadas

Uso compartilhado significa vários usuários da mesma igreja. Os quatro papéis estão confirmados; jornadas não criam papéis adicionais. Consulte a [matriz RBAC](../features/F-004-acesso-compartilhado/matriz-acesso.md).

| Necessidade de usuário | Jornada | Dependência |
|---|---|---|
| Organizar classificações financeiras | Consultar ou criar categorias, contas e tipos antes do registro | Permissões conforme matriz RBAC vigente |
| Registrar uma movimentação | Selecionar os três cadastros, informar data, valor e descrição; receber o registro criado ou erro acionável | Cadastros existentes e acesso autorizado |
| Consultar movimentações | Filtrar, navegar pelas páginas e consultar um lançamento específico | Definir quem pode consultar quais registros |
| Corrigir um registro | Localizar o lançamento, substituir todos os campos ou alterar parte deles | Política de edição e concorrência pendente |
| Remover um registro | Localizar e excluir o lançamento | Exclusão definitiva existe; autorização e histórico precisam ser implementados |
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

- Identificar usuários e restringir operações pela matriz RBAC; somente Administrador gere contas e permissões.
- Definir visibilidade dos registros, política de exclusão, rastreabilidade e edição concorrente.
- Construir interface web para as jornadas do núcleo e gestão de acessos confirmada.

Esses complementos não estão implementados. Uso compartilhado, interface web, igreja única e quatro papéis estão confirmados. A retenção do histórico de auditoria é eterna; o contrato técnico de identidade e histórico continua pendente.

### Fora deste recorte

- Cálculo de saldo, transferências entre contas e interpretação contábil automática de entrada/saída, explicitamente ausentes no README.
- Funcionalidades além das operações Ver, Criar/Editar e Excluir da matriz. Edição e exclusão dos cadastros auxiliares integram o planejamento da F-004, ainda sem implementação.
- Relatórios consolidados, exportações, conciliação bancária, pagamentos, anexos e integrações externas.
- Gestão de membros, dízimos por pessoa, eventos, patrimônio e folha de pagamento.
- Múltiplas igrejas, Master, vínculos entre igrejas, seleção de igreja e migração para isolamento multi-igreja estão fora do MVP. Múltiplas moedas continuam sem confirmação.

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
| REQ-011 | Exigir identidade verificada e aplicar autorização a consultas e alterações no uso compartilhado | Essencial — uso compartilhado | Proposto a partir da decisão de uso; não implementado; quatro papéis confirmados, método técnico pendente | AC-018, AC-019 |
| REQ-012 | Preservar integridade e referências em falhas de gravação e atualização, sem aceitar relacionamentos inexistentes | Essencial — núcleo | Repositórios, schema e testes; existente | AC-006, AC-013, AC-017 |
| REQ-013 | Disponibilizar interface web nova para acesso e jornadas financeiras do MVP, com estados de erro, vazio e permissão negada | Essencial — uso compartilhado | Confirmado pelo solicitante; não implementado; tecnologia pendente | AC-020 |
| REQ-014 | Administrador tem acesso geral ao MVP e gere contas, papéis e permissões; Presidente e Tesoureiro operam conforme concessões e Membro somente consulta. Não há administração automática por Presidente | Essencial — uso compartilhado | Confirmado em 04/11/2026; matriz RBAC vigente | AC-021, AC-022 |
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
| AC-014 | REQ-008 | Excluir lançamento existente: receber 204 sem corpo; consulta ou nova exclusão do mesmo ID retorna 404. Exigir autorização e histórico no uso compartilhado; não há limite temporal para exclusão |
| AC-015 | REQ-009 | Leituras e gravações bem-sucedidas, exceto DELETE, retornam JSON com status, message e data; lista de lançamentos inclui pagination. Erro de validação ou integridade retorna 400; ausência individual, 404; falha tratada de banco, 500 com mensagem genérica sem caminho interno ou SQL |
| AC-016 | REQ-010 | Em base legada sintética válida, converter 0.29→29, 1.005→101 e 125.90→12590; preservar IDs dos lançamentos e continuidade da sequência mesmo após remoção de ID alto; segunda execução não altera o resultado. Cadastros duplicados são consolidados no menor ID e referências são redirecionadas |
| AC-017 | REQ-010, REQ-012 | Em base legada com valor inválido, não positivo, arredondado a zero, acima do limite ou referência inexistente, a migração falha com rollback; comparar schema, registros e cadastros antes/depois e confirmar que não houve atualização parcial |
| AC-018 | REQ-011 | Proposto: sem identidade verificada, tentativas de consulta, criação, edição e exclusão são negadas sem revelar dados financeiros nem alterar registros. Fluxo de autenticação e respostas exatas dependem de Q-001 |
| AC-019 | REQ-011 | Condicional à matriz aprovada: testar cada combinação de perfil, operação e escopo de dados, incluindo acesso direto por ID; permitidas funcionam e negadas não revelam nem alteram registros. Q-002 está resolvida: igreja única; contrato e implementação ainda precisam ser verificados |
| AC-020 | REQ-013 | Pela interface web, uma identidade autorizada acessa o sistema, cria/consulta cadastros, registra, localiza e edita lançamento; realiza a ação de remoção somente conforme política aprovada. Erros, resultados vazios e negativas são observáveis; dados e centavos coincidem com a API. Verificar também gestão de acessos para os perfis autorizados |
| AC-021 | REQ-014 | Administrador configura permissões; Presidente e Tesoureiro operam conforme matriz, sem gerir acessos; Membro somente consulta. Verificar aplicação na API e interface |
| AC-022 | REQ-014, REQ-011 | Usuário sem concessão não consegue executar a operação nem conceder privilégios a si mesmo por chamada direta ou payload forjado; ao retirar uma concessão, seu efeito segue a política de atualização/revogação acordada. Critério depende de fechar Q-001 |

### Critérios acrescentados em 04/11/2026

- **AC-014 (atualizado):** usuário autorizado exclui lançamento existente independentemente de sua data; recebe 204 sem corpo; consulta ou nova exclusão retorna 404. Não há prazo de exclusão.
- **AC-021 (complementado):** testar Administrador criando e editando permissões; Presidente, Tesoureiro e Membro não podem gerir permissões, inclusive por API direta.
- **AC-023 — REQ-015:** para cada um dos três cadastros, usuário autorizado exclui registro sem vínculos; o registro deixa de aparecer nas consultas. A exclusão de um lançamento não exclui automaticamente seus cadastros; após remover o último vínculo, a exclusão do cadastro torna-se permitida.
- **AC-024 — REQ-015/012:** para cada cadastro com um ou mais lançamentos vinculados, rejeitar exclusão sem alterar cadastro ou lançamentos. Verificar disputa entre criação/edição de lançamento e exclusão do cadastro, impedindo referências órfãs e remoção em cascata.

### Igreja única e rastreabilidade da revisão de 04/11/2026

- **REQ-016 (substituído):** o MVP atende uma única igreja, com dados financeiros compartilhados conforme RBAC, sem subdivisão por unidade ou conta.
- **AC-025 — REQ-016/011 (revisado):** usuários autorizados consultam os mesmos dados da igreja, sem seleção de igreja; permissões de ação continuam sendo verificadas na API.
- **AC-026 (retirado do MVP):** cenário de referências cruzadas entre igrejas não se aplica. Integridade das referências continua coberta por AC-006/013/024.
- **REQ-017 e AC-027 (retirados do MVP):** gestão de vínculos entre usuário e igrejas deixa de fazer parte do escopo. IDs não serão reutilizados.
- **REQ-018 a REQ-026:** regras vigentes e critérios locais em [ciclo de acesso](../features/F-004-acesso-compartilhado/decisoes-ciclo-acesso.md); requisitos retirados estão identificados.
- **REQ-027:** catálogo fechado de Administrador, Presidente, Tesoureiro e Membro; não aceitar Master ou papéis inventados. **AC-028:** testar os quatro papéis e rejeitar atribuição de papel fora do catálogo, sem mudança de privilégios.
- **REQ-028:** Administrador cria/convida e desativa contas, atribui papéis e nomeia outros Administradores; preservar ao menos um Administrador ativo. **AC-029:** Administrador executa essas ações; os outros três papéis são impedidos, inclusive por API direta; retirada/desativação do último Administrador falha, inclusive sob concorrência.
- A retirada de múltiplas igrejas e os quatro papéis foram solicitados explicitamente; a transferência das funções do Master ao Administrador foi confirmada pelo solicitante nesta revisão.
- Histórico anterior: [decisões substituídas](../history/2026-11-04-decisoes-substituidas.md).
## Requisitos não funcionais

| Referência | Condição / meta | Forma de avaliação | Estado |
|---|---|---|---|
| REQ-004 — exatidão monetária | Valores armazenados e retornados em centavos inteiros, conforme limites definidos | AC-007 e AC-016 | Existente; não implica suporte multimoeda |
| REQ-012 — integridade | Nenhuma gravação parcial nos cenários de falha definidos | AC-006, AC-013 e AC-017 | Garantia a verificar pela suíte |
| REQ-009 — erros | Não expor caminhos internos ou SQL nas falhas operacionais tratadas | Injetar falhas em ambiente isolado; AC-015 | Há testes existentes; limite de ID conhecido deve ser corrigido |
| REQ-011 — acesso | Permissões aplicadas também a acesso direto às APIs e aos IDs | AC-018 e AC-019 | Proposto; regras e implementação pendentes |
| Desempenho e capacidade | Quantidade de usuários simultâneos, volume e latência aceitável não definidos | Definir carga representativa e medir após Q-005 | Meta pendente, sem número inventado |
| Disponibilidade e recuperação | Janela aceitável de interrupção e perda de dados não definidas | Definir rotina de backup e ensaio de restauração após Q-006 | README exige backup/parada para migração, mas não define serviço operacional |
| Rastreabilidade e retenção | Histórico mínimo, autoria e retenção eterna confirmados | Verificar que eventos de auditoria não são eliminados nem descartados automaticamente | Requisito confirmado; implementação pendente |
| Usabilidade | Interface web confirmada; validação com usuários pendente | Avaliar jornadas após Q-004 | API existente; interface de usuário não localizada |

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
| Q-001 | Identidade, permissões e ciclo de acesso | F-004/T-001/T-002 | Quatro papéis e autoridade do Administrador confirmados; contrato técnico pendente |
| Q-002 | Escopo dos registros | REQ-016 | Resolvida: única igreja, sem subdivisão por unidade ou conta; RBAC controla operações |
| Q-008 | Múltiplos vínculos entre usuário e igrejas | REQ-017 retirado | Não aplicável ao MVP de igreja única |
| Q-003 | Exclusão, autoria, histórico e retenção | REQ-008/015/025 | Resolvida em 04/11/2026: histórico de auditoria com retenção eterna, sem descarte automático |
| Q-004 | O uso será por cliente de API já existente ou exige interface web? | Entrega utilizável e REQ-013 | Resolvida: interface web nova. Tecnologia e contratos de identidade dependem de desenho técnico |
| Q-005 | Quantos usuários simultâneos e registros são esperados? Como tratar edições concorrentes e reenvios de criação? | Capacidade, conflitos e prevenção de duplicidade | Pendente; não prometer proteção contra sobrescrita concorrente |
| Q-006 | Onde será operado, quem fará backup e qual perda/interrupção é aceitável? | Hospedagem, recuperação e disponibilidade | Pendente |
| Q-007 | BRL será a única moeda? Tipos continuarão livres ou terão significado fixo de entrada/saída? | Evolução de valores, saldo e relatórios; sem mudança do contrato atual até decisão | BRL aparece em exemplo do README; exclusividade não confirmada |
| H-001 | Pessoas responsáveis pelas finanças são o público principal | Validar jornadas e vocabulário antes de fechar o MVP | Hipótese derivada do domínio |

Riscos concretos: uso compartilhado ainda sem controles de acesso; política de exclusão sem validação de negócio; suite não executada; entrada numérica de ID sem limite nos cadastros; configuração do banco com chaves `DB_PATH` e `DATABASE` distintas. A documentação inicial do README diverge dos módulos atuais, e README/GIT_GUIDELINES divergem sobre a branch de origem. Esses pontos devem ser tratados no planejamento apropriado, sem converter ajustes técnicos em novas funcionalidades de produto.

## Decisões e alterações históricas (substituições indicadas na revisão vigente)

| Data | Decisão ou alteração | Fonte | Impacto |
|---|---|---|---|
| 28/10/2026 | Criar o primeiro PRD a partir do projeto atual | Pedido do solicitante | Consolida REQ-001 a REQ-012 e AC-001 a AC-019; sem alterações de código |
| 28/10/2026 | O primeiro uso será compartilhado; perfis ainda indefinidos | Resposta explícita do solicitante | REQ-011 proposto e Q-001 a Q-006; não define permissões automaticamente |
| 28/10/2026 | Separar contrato atual de propostas e pendências | Organização desta versão pelo analista | Não atribui aprovação de produto a comportamentos herdados |
| 29/10/2026 | Incorporar resposta do solicitante: interface web nova; Administrador e Presidente com acesso geral e definição dos demais acessos | Resposta explícita durante planejamento, incorporada nesta data | REQ-013/014, AC-020 a AC-022, Q-004 resolvida e Q-001 parcialmente resolvida; versão 0.2, sem escolha de frontend ou permissões adicionais |

Documentos posteriores devem preservar os IDs e resolver as perguntas antes de assumir permissões, isolamento, exclusão ou metas operacionais. Não há aprovação final de produto registrada. O [handoff](handoff-prd.md) descreve o que pode avançar e as dependências restantes.

### Revisão vigente — 04/11/2026

Igreja única e RBAC com quatro papéis substituem as decisões anteriores de múltiplas igrejas. Administrador assume as funções de gestão de contas anteriormente atribuídas ao Master, conforme confirmação explícita. Histórico mínimo com retenção eterna, recuperação por e-mail e revogação permanecem; não há alteração de código nesta revisão.
