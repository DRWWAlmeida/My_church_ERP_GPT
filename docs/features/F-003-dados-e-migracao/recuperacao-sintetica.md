# Ensaio de recuperação — F-003/T-003

Escopo: AC-016, AC-017 e F-003/AC-002; somente dados sintéticos. Implementação reproduzível em `app/tests/test_transaction_migration.py`, teste `test_restore_synthetic_backup_after_committed_migration`.

## Procedimento reproduzido

1. Criar base legada isolada com valores 0.29, 1.005 e 125.90, duplicatas nos três cadastros e referências às duplicatas. Inserir e remover lançamento 50 para manter a sequência acima dos IDs presentes.
2. Salvar inventário ordenado de `sqlite_master` (tabelas, índices e SQL), linhas de todas as tabelas e `sqlite_sequence`. Identificar o código/schema correspondente ao backup: neste ensaio, fixture legada com coluna `valor`; código-base `02d08b416781d977693bcb97c4bab3ca89e4c9ab` mais diff local descrito no handoff.
3. Sem atendimento ou escritas concorrentes, copiar a base para arquivo e gerar outro arquivo de backup usando `sqlite3.Connection.backup`. Comparar o backup ao inventário. Fechar as conexões; o gerenciador de contexto SQLite sozinho não fecha conexões.
4. Configurar explicitamente `DATABASE` para o arquivo sintético e executar `create_schema()` no contexto Flask. Reabrir o arquivo em outra conexão e confirmar a conversão persistida para 29, 101 e 12590 centavos.
5. Com todas as conexões da aplicação fechadas, abrir o backup como origem e o arquivo convertido como destino; executar `backup.backup(destino)`. Fechar ambos e reabrir o destino.
6. Comparar integralmente schema, linhas e sequência ao inventário anterior. Exigir `PRAGMA integrity_check` igual a `ok` e `PRAGMA foreign_key_check` vazio. Inserir lançamento no schema legado e confirmar ID 51; desfazer essa escrita de sondagem.

Reprodução local, com diretório temporário exclusivo para evitar conflitos de permissão do diretório padrão:

```powershell
$testTemp = Join-Path $PWD ('.pytest_cache/t003-' + [guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe -m pytest app/tests/test_transaction_migration.py -q --basetemp $testTemp
```

## Falha antes do commit versus recuperação após commit

Antes do commit, `create_schema()` executa rollback: os testes com valores inválidos e cada uma das três referências inexistentes comparam o estado completo. Há uma linha válida antes da inválida e duplicatas nos três cadastros, para detectar atualização parcial.

Após o commit, rollback não desfaz a migração: o ensaio restaura uma cópia anterior. Uma operação real exigiria autorização própria, parada de todos os processos, backup validado e código compatível com o schema restaurado antes de reabrir atendimento. Não iniciar o código atual sobre a base restaurada esperando manter `valor`: a preparação voltará a convertê-la.

Não foi executada recuperação real, downgrade de aplicação, teste de concorrência, falha de energia ou ensaio de volume de produção. Não há garantia de RPO/RTO. Escritas posteriores ao backup podem ser perdidas. A comparação é lógica, não identidade byte a byte dos arquivos. Não copiar apenas o arquivo principal de um banco ativo; o ensaio usa a API de backup SQLite e conexões fechadas durante a restauração.
