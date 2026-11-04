# Contratos internos e HTTP

Base: [PRD](../product/PRD.md), REQ-001 a REQ-009 e REQ-012, e [módulos](../../app/modules/). Estado: contrato observado; propostas identificadas explicitamente. URLs não têm prefixo de versão. Não há contrato de login ou gerenciamento de usuários implementado.

## Cadastros

| Caminho | Métodos | Campo no POST | Dados retornados |
|---|---|---|---|
| `/category` | GET, POST | `categoria` | Objeto `{id, nome}` no POST; lista desses objetos no GET |
| `/checking-account` | GET, POST | `conta_corrente` | Mesmo formato |
| `/transaction-type` | GET, POST | `tipo_lancamento` | Mesmo formato |

POST recebe objeto JSON, exige campo textual aparado de 3 a 100 caracteres e retorna 201; inválido/duplicado retorna 400. Campos extras são ignorados. JSON ausente ou inválido é tratado como payload inválido.

GET retorna 200; aceita `id` convertido para inteiro positivo e `nome` aparado de 1 a 100 caracteres. Os filtros combinam-se por AND; nome usa LIKE parcial, com curingas `%` e `_` interpretados. Ordenação por ID crescente, sem paginação. Sem resultados: `data: []`. Parâmetros desconhecidos são ignorados e repetidos são lidos por `request.args.get`, sem rejeição explícita.

Atualização de 30/10/2026 (F-001/T-002): IDs acima de 9223372036854775807 são rejeitados pelos três schemas com HTTP 400 e JSON de erro, antes da consulta SQLite. O limite máximo continua aceito como filtro; sem correspondência, retorna lista vazia com 200. Valores que excedem o limite de conversão textual do Python também retornam 400 pela validação existente. Não há GET individual por segmento de URL, PUT, PATCH ou DELETE desses cadastros.

## Lançamentos

| Método/caminho | Entrada | Sucesso | Ausência |
|---|---|---|---|
| POST `/transaction` | Todos os campos abaixo | 201, objeto completo | Relação inexistente: 400 |
| GET `/transaction` | Filtros e paginação | 200, lista e pagination | Lista vazia: 200 |
| GET `/transaction/<int:transaction_id>` | ID positivo suportado | 200, objeto completo | 404 |
| PUT `/transaction/<int:transaction_id>` | Todos os campos | 200, objeto completo | Com corpo válido: 404 |
| PATCH `/transaction/<int:transaction_id>` | Um ou mais campos conhecidos | 200, objeto completo | Com corpo válido: 404 |
| DELETE `/transaction/<int:transaction_id>` | ID positivo suportado | 204, sem corpo | 404 |

Payload sintético de POST/PUT:

```json
{
  "tipo_lancamento_id": 1,
  "categoria_id": 1,
  "conta_corrente_id": 1,
  "data": "2026-10-06",
  "valor_centavos": 12590,
  "descricao": "Oferta de exemplo"
}
```

Os três IDs e o valor devem ser inteiros de 1 a 9223372036854775807; booleanos, strings, frações e nulos são inválidos. As relações devem existir. A data precisa ser válida em `YYYY-MM-DD`; pode ser futura. A descrição aparada deve ter 3 a 255 caracteres. Corpo não objeto, vazio, campos desconhecidos ou falta de obrigatórios no POST/PUT retornam 400. PATCH vazio é inválido; não altera campos omitidos. Nenhum campo de identidade/propriedade é aceito atualmente.

| Query de GET coleção | Regra |
|---|---|
| `tipo_lancamento_id`, `categoria_id`, `conta_corrente_id` | Inteiro positivo textual, de 1 a 19 dígitos, dentro do limite; ID válido inexistente resulta em lista vazia |
| `data_inicio`, `data_fim` | Datas válidas, limites inclusivos, início não posterior ao fim |
| `descricao` | Trecho literal aparado de 1 a 255 caracteres; `%`, `_` e barra invertida escapados na busca |
| `page` | Inteiro positivo, padrão 1; limite do inteiro e do deslocamento verificados |
| `per_page` | Inteiro positivo, padrão 20, máximo 100 |

Queries desconhecidas/repetidas são rejeitadas com 400. Resultados são ordenados por data decrescente, depois ID decrescente. `total_pages = (total + per_page - 1) // per_page`; total zero resulta em zero páginas. Página além do fim retorna lista vazia. Deslocamento `(page - 1) * per_page` acima do limite retorna 400.

Resposta sintética de lançamento:

```json
{
  "status": "success",
  "message": "Lançamento consultado com sucesso!",
  "data": {
    "id": 1,
    "data": "2026-10-06",
    "valor_centavos": 12590,
    "descricao": "Oferta de exemplo",
    "tipo_lancamento": {"id": 1, "nome": "Entrada"},
    "categoria": {"id": 1, "nome": "Oferta"},
    "conta_corrente": {"id": 1, "nome": "Caixa"}
  }
}
```

Coleção usa `data` como lista e acrescenta `pagination: {page, per_page, total, total_pages}`. Respostas dos cadastros usam o mesmo envelope de sucesso, com objetos menores. A mensagem varia por operação; clientes devem usar o status HTTP e os campos estruturados, sem depender de comparação de frases.

## Erros e limitações

| Erro próprio | HTTP | Corpo |
|---|---|---|
| `ValidationError` | 400 | `status: "error"`, `message`, opcional `data: {campo: valor}` |
| `IntegrityError` | 400 | Mesmo formato; inclui unicidade e relações inválidas |
| `NotFoundError` | 404 | `status: "error"`, `message` |
| `OperationalError` | 500 | `status: "error"`, mensagem operacional genérica |

`app/errors.py` registra handlers dos erros próprios; não há handler universal para 404/405 do roteador ou exceções inesperadas. Por isso, URL não reconhecida e falha fora dos erros próprios não têm garantia de JSON. IDs incompatíveis com o conversor de rota podem nem chegar ao service. No PUT/PATCH a validação do corpo ocorre antes da busca do recurso; corpo inválido pode retornar 400 mesmo para ID inexistente.

Atualização de 30/10/2026 (F-001/T-003): o fallback de integridade de `category.repository.create` retorna mensagem genérica, sem incluir o texto da exceção SQLite. O detalhe continua no log do servidor; respostas específicas de duplicidade e campo obrigatório foram preservadas. Testes dos três cadastros verificam erros de integridade e falhas operacionais sem detalhes internos no corpo HTTP. Padronização de erros de roteamento é evolução de contrato, não comportamento já disponível.

## Interfaces internas

| Fronteira atual | Contrato |
|---|---|
| Rotas → services dos cadastros | POST passa payload bruto; GET passa ID/nome já validados pela rota |
| Services de cadastros → schemas | `validate_create_*_payload(payload)` retorna dicionário normalizado ou ValidationError |
| Services de cadastros → repository | `create(nome)` retorna dict; consultas recebem listas de condições SQL internas e parâmetros; retornam Rows convertidas em dict no service |
| Rotas → services de transaction | `create_transaction(payload)`, `get_transaction(id)`, `get_transactions(args)`, `update_transaction(id,payload,partial=False)`, `delete_transaction(id)` |
| Services de transaction → schema | Validar ID, payload ou query; `validate_query` espera objeto com `getlist`, como `request.args`, não dict simples |
| Services de transaction → repository | Valores validados; create/get/update retornam dict, list_transactions retorna `(lista, pagination)`, delete retorna None; erros próprios propagam |
| Repository → database | `get_connection()` devolve nova conexão com foreign_keys ligado; repository é responsável por transação e fechamento |

Services atuais não recebem identidade ou escopo. A proposta de evolução é receber contexto autenticado e aplicar políticas antes do acesso aos dados, sem confiar em parâmetros de autorização do cliente; detalhes em [security.md](security.md).

## Compatibilidade

Preservar URLs, tipos e semântica atuais ao corrigir validações locais. Mudanças em autenticação, escopo de dados, exclusão, conflito, formato numérico ou paginação dos cadastros exigem explicitar impacto aos consumidores e testes de contrato. Autenticação futura negará chamadas hoje anônimas; preparar migração dos clientes, sem manter uma exceção anônima implícita.

Os valores são números JSON; um futuro cliente deve preservar sua representação inteira no intervalo contratado. Não reduzir limites nem trocar números por strings silenciosamente por causa da escolha do frontend; avaliar essa compatibilidade ao responder Q-004.

## Revisão de escopo — 04/11/2026

O MVP atende uma única igreja, com os papéis Administrador, Presidente, Tesoureiro e Membro. [ADR-004](decisions/ADR-004-igreja-unica-rbac.md) e [escopo organizacional](isolamento-igrejas.md) definem a revisão. Preservar schema financeiro e unicidade global; não adicionar igreja_id, usuario_igreja ou contexto/seletor de igreja. Contratos de identidade e histórico permanecem propostos, sem implementação. Administração de contas e permissões é exclusiva do Administrador.
