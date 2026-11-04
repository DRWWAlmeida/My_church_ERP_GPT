# Especificação — F-006: Aceite integrado e preparação operacional

## Estado e referências

Referências: [PRD vigente](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-001 a REQ-014; Q-005, Q-006, Q-007. Critérios AC sem prefixo pertencem ao PRD; critérios F-006/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Demonstrar MVP integrado em homologação com recuperação ensaiada, metas/limites conhecidos e aceite rastreável. Preparar entrega revisável; implantação real não está autorizada por este planejamento.

## Regras e contratos

Não inventar carga, disponibilidade, moeda, hospedagem ou política de conflito. A retenção eterna do histórico de auditoria está decidida; retenção e acesso de logs operacionais continuam separados. Distinguir aceite técnico, decisão de produto e publicação. Infraestrutura é suporte à jornada, não substitui aceite funcional.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
| AC-001 | Para cada cadastro, enviar nome válido com espaços externos; receber HTTP 201 com ID e nome aparado; consultar e encontrar o registro persistido |
| AC-002 | Enviar corpo não objeto, nome ausente, não textual, em branco, com 2 ou 101 caracteres: receber 400 sem criar registro; limites de 3 e 100 são aceitos. Após criar `Oferta`, tentar `oferta`: receber 400 sem duplicar |
| AC-003 | Com cadastros sintéticos, consultar sem filtro, por ID, por trecho de nome e pelos dois juntos; receber 200 com a interseção correta em ordem de ID crescente. ID inexistente ou ausência de correspondência retorna lista vazia |
| AC-004 | Consultar cadastro com ID textual inválido, zero ou negativo: receber 400. Proposta de correção: ID acima de 9223372036854775807 também retorna 400, sem exceção interna; este último caso falha no código examinado |
| AC-005 | Com os três cadastros existentes, criar lançamento válido; receber 201 com ID, data, valor, descrição e cada relação como objeto com ID e nome; a consulta individual retorna o registro |
| AC-006 | Omitir cada campo obrigatório, enviar corpo não objeto/JSON inválido, campo desconhecido ou relação inexistente: receber 400 e manter a quantidade de lançamentos anterior |
| AC-007 | Aceitar 1, 12590 e 9223372036854775807 centavos; rejeitar zero, negativo, fração, string, booleano, nulo e valor acima do limite com 400. Tipo denominado `Saída` mantém valor positivo, sem gerar saldo ou transferência |
| AC-008 | Aceitar data futura válida e descrição de 3 ou 255 caracteres após aparar. Rejeitar data impossível ou formato diferente, descrição em branco, não textual, com 2 ou 256 caracteres; não persistir as tentativas inválidas |
| AC-009 | Consultar ID existente e receber 200; consultar ID positivo válido inexistente e receber 404. A resposta contém as três relações identificadas |
| AC-010 | Com lançamentos em datas diferentes e empatadas, combinar filtros e verificar interseção, limites inclusivos e ordem data/ID decrescente. Busca por `%` na descrição procura caractere literal. Sem correspondência ou em página além do fim, receber 200 com lista vazia |
| AC-011 | Sem parâmetros de página, retornar page=1 e per_page=20; retornar total e total_pages coerentes. Rejeitar page=0, per_page=101, parâmetros repetidos/desconhecidos, filtros inválidos, intervalo invertido e deslocamento acima do limite com 400 |
| AC-012 | PUT válido substitui todos os campos e retorna 200; PUT incompleto retorna 400. PATCH válido altera apenas os campos enviados; PATCH vazio ou com campo desconhecido retorna 400. Atualização com corpo válido para ID inexistente retorna 404 |
| AC-013 | Ao alterar simultaneamente descrição e uma relação para ID inexistente, receber 400 e verificar que nenhum campo foi alterado; em falha de persistência, confirmar ausência de gravação parcial |
| AC-014 | Excluir lançamento existente: receber 204 sem corpo; consulta ou nova exclusão do mesmo ID retorna 404. Critério descreve contrato atual; política de remoção no produto compartilhado depende de Q-003 |
| AC-015 | Leituras e gravações bem-sucedidas, exceto DELETE, retornam JSON com status, message e data; lista de lançamentos inclui pagination. Erro de validação ou integridade retorna 400; ausência individual, 404; falha tratada de banco, 500 com mensagem genérica sem caminho interno ou SQL |
| AC-016 | Em base legada sintética válida, converter 0.29→29, 1.005→101 e 125.90→12590; preservar IDs dos lançamentos e continuidade da sequência mesmo após remoção de ID alto; segunda execução não altera o resultado. Cadastros duplicados são consolidados no menor ID e referências são redirecionadas |
| AC-017 | Em base legada com valor inválido, não positivo, arredondado a zero, acima do limite ou referência inexistente, a migração falha com rollback; comparar schema, registros e cadastros antes/depois e confirmar que não houve atualização parcial |
| AC-018 | Proposto: sem identidade verificada, tentativas de consulta, criação, edição e exclusão são negadas sem revelar dados financeiros nem alterar registros. Fluxo de autenticação e respostas exatas dependem de Q-001 |
| AC-019 | Condicional à matriz aprovada: testar cada combinação de perfil, operação e escopo de dados, incluindo acesso direto por ID; permitidas funcionam e negadas não revelam nem alteram registros. Q-002 está resolvida: igreja única; contrato e implementação ainda precisam ser verificados |
| AC-020 | Pela interface web, uma identidade autorizada acessa o sistema, cria/consulta cadastros, registra, localiza e edita lançamento; realiza a ação de remoção somente conforme política aprovada. Erros, resultados vazios e negativas são observáveis; dados e centavos coincidem com a API. Verificar também gestão de acessos para os perfis autorizados |
| AC-021 | Administrador configura permissões; Presidente e Tesoureiro operam conforme matriz, sem gerir acessos; Membro somente consulta. Verificar aplicação na API e interface |
| AC-022 | Usuário sem concessão não consegue executar a operação nem conceder privilégios a si mesmo por chamada direta ou payload forjado; ao retirar uma concessão, seu efeito segue a política de atualização/revogação acordada. Critério depende de fechar Q-001 |
| F-006/AC-001 | Critério técnico/local proposto: Metas acordadas de capacidade/recuperação e política de conflitos/reenvios têm evidência em homologação com configuração e versão identificadas. |
| F-006/AC-002 | Critério técnico/local proposto: Matriz de aceite reúne evidências de critérios, revisão técnica, responsável de produto, versão e procedimento de recuperação; publicação é decisão separada. |

## Cenários e pendências

`python -m pytest` no commit candidato; executar verificações da web que forem definidas, jornadas e matriz de acesso em ambiente isolado. Ensaiar carga/conflitos e backup/restauração conforme metas acordadas. Registrar revisor, base/alvo e aceite do responsável de produto.

Q-005/Q-006/Q-007 pendentes. Se produto exigir novo mecanismo de conflito, idempotência, auditoria ou multimoeda, revisar requisitos e decompor tarefas antes de implementação. Não ocultar expansão de escopo em tarefa de homologação.

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

## Escopo vigente e aceite complementar — 04/11/2026

Uma única igreja, sem seletor/contexto multi-igreja, com Administrador, Presidente, Tesoureiro e Membro. Somente Administrador gere contas, papéis e permissões. Incluir AC-023/024/025/028/029 do PRD e critérios F-004/AC-002 a AC-010 vigentes (AC-006 retirado) na integração. AC-026/027 não se aplicam ao MVP. Matriz, ciclo de acesso e retenção eterna do histórico de auditoria estão na F-004; contrato técnico permanece pendente.

F-006/T-003 executará também os critérios complementares acima, após F-004/T-007 e F-005/T-005; a homologação deve usar os quatro papéis em dados sintéticos da mesma igreja.
