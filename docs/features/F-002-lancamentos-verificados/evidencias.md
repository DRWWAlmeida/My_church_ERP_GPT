# Evidências — F-002/T-001

Data: 30/10/2026. Estado: concluída. Base Git: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`; branch `feature/api-transaction`; alvo: diff local de `app/tests/test_lancamento.py` e documentação desta tarefa. Alterações anteriores de F-001 preservadas, sem novo commit.

## Resultado e cobertura

O comportamento existente passou nas verificações ampliadas; não foi necessário alterar produção. Foram acrescentados seis casos parametrizados/individuais e reforçadas as asserções de rejeição dos testes existentes, sem duplicar os cenários já cobertos.

| Critério | Evidência |
|---|---|
| AC-005 | Teste de ciclo existente verifica criação, relações com ID/nome e consulta; novos testes conferem persistência dos valores de fronteira por leitura individual |
| AC-006 | Campos obrigatórios, JSON inválido/não objeto e relações inexistentes continuam rejeitados; novas asserções confirmam quantidade inalterada. Campo desconhecido no POST tem caso específico com registro prévio preservado |
| AC-007 | Criação aceita 1, 12590 e 9223372036854775807 centavos e a leitura mantém o inteiro exato. Tipos inválidos, zero, negativo, fração e estouro são rejeitados. Tipo Saída mantém valor positivo, um único lançamento e a conta inalterada |
| AC-008 | Descrições com 3/255 caracteres após aparar são aceitas; datas futura e de ano bissexto válidas persistem. Data 2025-02-29 é rejeitada. Casos inválidos existentes de formato, descrição e tipos mantêm o registro anterior intacto |

Para valores inválidos nos campos, os testes agora criam primeiro um registro válido e conferem que lista e total continuam exatamente iguais após a rejeição. Isso verifica preservação de dados além da simples resposta 400.

## Verificações

Ambiente existente: `.venv`, Python 3.14.3, pytest 9.0.3. Sem instalar dependências adicionais.

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_lancamento.py -q
.\.venv\Scripts\python.exe -m pytest
git diff --check
```

| Verificação | Resultado |
|---|---|
| Testes de lançamentos | **80 passed in 1.83s**, saída 0 |
| Suíte completa | **194 passed in 3.16s**, saída 0 |
| Diff/whitespace | Sem erro; avisos de conversão futura LF/CRLF conforme configuração do Git |

Não foi reproduzido defeito novo, nem afirmado que houve falha antes da alteração. Trata-se de fechamento de lacunas de verificação previstas em T-001. As fixtures existentes mantêm bancos isolados; não houve execução do servidor ou migração do banco real.

## Limites

Busca/paginação e edição/exclusão/rollback permanecem nas tarefas T-002/T-003, mesmo com testes anteriores desses fluxos passando. Esta execução não aceita essas tarefas antecipadamente. Não houve revisão independente, alteração de contrato, commit, push ou deploy. O resultado não representa aceite do MVP.
