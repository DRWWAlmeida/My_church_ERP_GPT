# Especificação — F-001: Cadastros confiáveis

## Estado e referências

Referências: [PRD v0.2](../../product/PRD.md), [arquitetura](../../architecture/overview.md), [contratos](../../architecture/contracts.md) e [mapa do MVP](../README.md). Planejamento em 29/10/2026, base de código `02d08b4`. Nenhuma tarefa executada nesta etapa.

Requisitos: REQ-001, REQ-002, REQ-009. Critérios AC sem prefixo pertencem ao PRD; critérios F-001/AC são locais e não alteram os IDs do produto.

## Resultado e escopo

Demonstrar criação e consulta dos três cadastros com respostas consistentes, corrigindo o limite de IDs já identificado. O ambiente isolado é pré-requisito, não a entrega funcional.

## Regras e contratos

Preservar GET/POST, normalização, unicidade NOCASE atual, busca com curingas e consultas vazias. Não adicionar PUT/DELETE de cadastros ou paginação. Não padronizar parâmetros extras por preferência.

## Critérios de aceitação

| ID | Fonte e resultado |
|---|---|
| AC-001 | Para cada cadastro, enviar nome válido com espaços externos; receber HTTP 201 com ID e nome aparado; consultar e encontrar o registro persistido |
| AC-002 | Enviar corpo não objeto, nome ausente, não textual, em branco, com 2 ou 101 caracteres: receber 400 sem criar registro; limites de 3 e 100 são aceitos. Após criar `Oferta`, tentar `oferta`: receber 400 sem duplicar |
| AC-003 | Com cadastros sintéticos, consultar sem filtro, por ID, por trecho de nome e pelos dois juntos; receber 200 com a interseção correta em ordem de ID crescente. ID inexistente ou ausência de correspondência retorna lista vazia |
| AC-004 | Consultar cadastro com ID textual inválido, zero ou negativo: receber 400. Proposta de correção: ID acima de 9223372036854775807 também retorna 400, sem exceção interna; este último caso falha no código examinado |
| AC-015 | Leituras e gravações bem-sucedidas, exceto DELETE, retornam JSON com status, message e data; lista de lançamentos inclui pagination. Erro de validação ou integridade retorna 400; ausência individual, 404; falha tratada de banco, 500 com mensagem genérica sem caminho interno ou SQL |


## Cenários e pendências

`python -m pytest app/tests/test_categoria.py app/tests/test_conta_corrente.py app/tests/test_tipo_lancamento.py`, no interpretador validado. Usar fixtures isoladas e injeção de falhas, nunca o banco local.

Sem migração. O alias Python falhou e pytest não estava no interpretador direto durante a análise anterior. Não instalar globalmente nem atualizar dependências gerais. Não há autorização de commit/merge implícita.

Tarefas bloqueadas aguardam decisões identificadas em [tasks.md](tasks.md). A existência do código não equivale a aceite ou tarefa concluída.

