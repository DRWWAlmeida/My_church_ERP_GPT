# Evidências — F-002/T-002

Data: 03/11/2026. Estado: concluída. Base Git: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; alvo: diff local desta tarefa em `app/tests/test_lancamento.py` e documentos de acompanhamento. Alterações anteriores foram preservadas; não houve commit.

## Resultado

Acrescentados 14 casos de teste e reforçada a asserção JSON dos parâmetros inválidos existentes. Não foi encontrado desvio nos cenários verificados; nenhuma correção de produção ou mudança de contrato foi necessária.

| Critério | Evidência |
|---|---|
| AC-009 | Consultas válidas com relações já cobertas pelos testes de ciclo/criação; novo caso confirma 404 JSON para ID válido inexistente no limite superior |
| AC-010 | Registros que diferem em apenas um filtro garantem que nenhuma condição seja omitida: tipo, categoria, conta, data inicial/final e descrição. Datas nos dois limites são incluídas. Busca literal encontra `%`, `_` e barra invertida e exclui textos semelhantes; testes anteriores preservam ordem por data/ID |
| AC-011 | Base com 21 registros demonstra padrão 20, segunda página parcial, terceira vazia e per_page=100; base vazia retorna total_pages=0. Maior deslocamento par suportado é aceito, próximo é rejeitado com 400. Repetição de todos os filtros é verificada, além dos casos existentes de parâmetro desconhecido, intervalo invertido e entrada inválida |

A lista e a contagem são conferidas juntas no cenário combinado. Registros excluídos da busca permanecem na base, distinguindo filtragem correta de ausência de dados. As respostas 400 verificam `status: error`.

## Execução

Ambiente existente: Python 3.14.3, pytest 9.0.3, `.venv`; sem novas dependências.

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_lancamento.py -q
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

- Direcionados: **94 passed in 2.55s**, saída 0.
- Suíte completa: **208 passed in 4.02s**, saída 0.
- Não houve falha nova reproduzida: a tarefa fechou lacunas de verificação do comportamento existente.
- Testes usam as fixtures isoladas; não houve execução de servidor ou migração do banco local.

## Limites

T-003 (edição, exclusão e rollback) não foi executada. A cobertura aqui não demonstra capacidade sob carga nem estabilidade entre páginas obtidas durante gravações concorrentes; essas garantias não pertencem ao contrato atual. Não houve revisão independente, publicação ou alteração de produção nesta tarefa.
