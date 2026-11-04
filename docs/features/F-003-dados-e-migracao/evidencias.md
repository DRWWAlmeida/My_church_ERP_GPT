# Evidências — F-003/T-001

> Registro histórico de T-001 preservado abaixo. Evidências de T-003 ao final.

Data: 03/11/2026. Estado: concluída como investigação e definição de contrato; nenhuma implementação de T-002. Base: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, branch `feature/api-transaction`, com alterações locais anteriores preservadas.

## Inspeção e sondagem

Inspecionados app/config.py, core/database.py, factory, app/run.py, usos de DATABASE/DB_PATH nos testes, README e arquitetura. A tarefa confirmou a divergência já documentada e definiu [contrato-configuracao.md](contrato-configuracao.md).

Sondagem executada pela `.venv` com script em stdin, usando unittest.mock.patch e runpy, sem persistir ferramenta adicional:

1. Substituir sqlite3.connect por mock e database.DB_PATH por `captured-default.db`.
2. Criar app e definir app.config['DB_PATH']='app-override.db'; em contexto, get_connection ainda solicita captured-default.db.
3. Definir DATABASE='explicit.db'; a conexão passa a solicitar explicit.db.
4. Sem contexto, substituir app.config.DB_PATH por module-updated.db; a conexão ainda usa captured-default.db.
5. Confirmar chamada de PRAGMA foreign_keys = ON.
6. Executar runpy.run_module('app.run', run_name='configuration_probe') com schema e factory substituídos por funções que apenas registram eventos. Ordem observada: schema, factory. Não foi iniciado servidor nem executada migração real.
7. Chamar factory com connect/schema monitorados; nenhuma dessas operações é chamada.

Todas as asserções passaram, saída 0. Os nomes acima são sentinelas de argumentos do mock; nenhum arquivo com esses nomes foi criado. Esses passos reproduzem o diagnóstico atual; CFG-01 a CFG-12 no contrato especificam o comportamento a implementar e verificar em T-002.

## Verificação existente de dados

```powershell
.\.venv\Scripts\python.exe -m pytest app/tests/test_schema.py app/tests/test_transaction_migration.py -q
```

Resultado: **12 passed in 0.12s**, saída 0. Ambiente: Python 3.14.3/pytest 9.0.3. Bases sintéticas isoladas; nenhuma migração do banco local.

Não foi repetida a suíte completa: esta tarefa só alterou documentos e fez sondagem com mocks. O último resultado completo de F-002/T-003 permanece histórico, não é uma execução desta etapa.

## Conclusão e limite

F-003/T-001 entrega precedência, compatibilidade, comportamento de falhas, fluxo de inicialização e 12 cenários verificáveis. F-003/AC-001 ainda depende da implementação real de T-002; os critérios de migração continuam sustentados pelos testes existentes, sem ensaio novo de recuperação pós-commit. Não foi marcado o restante de F-003 como concluído.

## F-003/T-003 — 04/11/2026

Estado: concluída. Base HEAD `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, diff local prévio preservado. Alterados os testes de migração, README, spec e quadro da tarefa; adicionados procedimento de recuperação e handoff. Não houve mudança em código de produção.

- **AC-016:** consolidação simultânea dos três cadastros no ID 1, redirecionamento das referências, preservação de IDs/datas/descrições, conversões 29/101/12590, próximo ID 51 após exclusão do 50 e comparação integral entre primeira e segunda execução.
- **AC-017:** sete valores inválidos (texto, negativo, zero, arredondado a zero, infinito, NaN e acima do limite) e referência inexistente em cada relacionamento. Comparação de todos os objetos de schema, linhas de todas as tabelas e sequências, com duplicatas e linha válida anterior; transação encerrada após rollback.
- **F-003/AC-002:** backup SQLite em arquivo, migração via alvo explicitamente configurado, confirmação do commit por nova conexão, restauração e comparação integral, integridade e próximo ID verificados. Ver [procedimento](recuperacao-sintetica.md).

Primeiro comando: `.\.venv\Scripts\python.exe -m pytest app/tests/test_schema.py app/tests/test_transaction_migration.py -q`: 14 passed, 1 error em setup do `tmp_path`, por falha de criação do diretório temporário padrão. Repetição fora do sandbox: 14 passed, 1 error por acesso negado ao diretório temporário. Nenhuma dessas tentativas concluiu o ensaio de restauração.

Verificação final:

```powershell
$testTemp = Join-Path $PWD ('.pytest_cache/t003-' + [guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe -m pytest -q --basetemp $testTemp
```

Resultado: **243 passed in 4.61s**, saída 0. `git diff --check`: saída 0. Autoinspeção do diff realizada; não equivale a revisão independente. Sem comandos de lint/tipos/build adicionais definidos para esta alteração de testes e documentação. Somente bases sintéticas; sem alegação de recuperação real, RPO/RTO ou aprovação de produto.
