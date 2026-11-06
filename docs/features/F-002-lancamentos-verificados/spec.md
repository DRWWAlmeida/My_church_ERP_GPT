# Especificação — F-002: Ciclo financeiro verificado

## Estado e referências

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-012. Critérios AC sem prefixo pertencem ao PRD; critérios F-002/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Demonstrar cadastro de relações → lançamento → busca → edição → exclusão atual em banco sintético. Reaproveitar CRUD existente; corrigir somente desvios de critérios demonstrados.

## Regras e contratos

Preservar centavos positivos, relações, datas futuras, regras PUT/PATCH, filtros literais e paginação. DELETE definitivo é contrato herdado para regressão, não autorização de sua política no MVP compartilhado. Saldo, transferência e auditoria não são adicionados implicitamente.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
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


## Cenários e pendências

`python -m pytest app/tests/test_lancamento.py`; ciclo com dados sintéticos, limites e falhas injetadas. Não replicar testes existentes que já demonstram os critérios.

Sem migração prevista. Mudança de contrato exige retorno ao analista/arquiteto. Q-003 permanece para exclusão compartilhada; Q-005 para conflitos/reenvios.

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

