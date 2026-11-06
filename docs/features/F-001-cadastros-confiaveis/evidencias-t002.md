# Evidências — F-001/T-002

Data: 30/10/2026. Estado: concluída. Base: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, branch `feature/api-transaction`; alvo: diff local, sem novo commit. A alteração anterior no README e os documentos não rastreados foram preservados.

## Correção e critérios

Os schemas de `category`, `checking_account` e `transaction_type` agora rejeitam ID convertido acima de 9223372036854775807 antes da consulta. Mantidos os tratamentos de zero, negativos, formato inválido e conversão textual excessiva, sem refatorar core ou alterar filtros válidos.

AC-003: consultas existentes por ID/nome e filtros combinados continuam passando. AC-004: texto inválido, zero, negativo, fração, máximo+1 e números com 100/5000 dígitos retornam 400 estruturado; o máximo permitido retorna 200 com lista vazia na base sem esse ID.

Foram acrescentados quatro casos por módulo (12 ao todo): máximo aceito, máximo+1, 100 dígitos e 5000 dígitos. Nos testes de conta/tipo, reforçada a asserção `status == error`. Não foram desativados testes nem alterados critérios para obter sucesso.

## Verificações executadas

Ambiente da tarefa anterior: `.venv`, Python 3.14.3, pytest 9.0.3; sem instalação adicional.

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_categoria.py app/tests/test_conta_corrente.py app/tests/test_tipo_lancamento.py -q --tb=short
.\.venv\Scripts\python.exe -m pytest app/tests/test_categoria.py app/tests/test_conta_corrente.py app/tests/test_tipo_lancamento.py -q
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

| Momento | Resultado |
|---|---|
| Novos testes antes de corrigir schemas | 6 failed, 72 passed in 1.80s; OverflowError para máximo+1 e 100 dígitos nos três endpoints |
| Após correção, testes dos cadastros | 78 passed in 0.98s; saída 0 |
| Após correção, suíte completa | 164 passed in 2.56s; saída 0 |
| Inspeção de diff e whitespace | Sem erros de whitespace; Git apenas avisa conversão futura LF/CRLF conforme configuração local |

Os casos de 5000 dígitos já eram rejeitados pelo tratamento de ValueError na conversão Python; os testes agora preservam esse comportamento. Os testes de máximo aceito já passavam antes da correção.

Os testes usam fixtures isoladas existentes. O hash do banco local após a execução corresponde ao registrado em T-001: `3D02C0A098D0918B725C2507791B258AA6A373651326B98FEC87C2FB80C1977B`. Não houve migração do banco real, execução do servidor ou alteração de dependências.

## Escopo e limites

Código alterado: `app/modules/category/schema.py`, `app/modules/checking_account/schema.py`, `app/modules/transaction_type/schema.py`. Testes alterados: `test_categoria.py`, `test_conta_corrente.py`, `test_tipo_lancamento.py` em `app/tests/`.

README, contrato de API e quadro do planejamento atualizados. Este registro complementa, sem substituir, o baseline histórico de T-001. As menções ao defeito em documentos da análise inicial descrevem o estado daquela base; a correção local está registrada aqui e no contrato vigente.

T-003 não foi iniciada; a revisão de outros erros dos cadastros permanece pendente. Não houve revisão independente, commit, merge, push ou deploy. Lint/tipos/build não têm comandos configurados nesta base. A aprovação da suíte não é aceite do MVP.
