# Evidências — F-003/T-002

Data: 04/11/2026. Estado técnico: concluído. Base: `02d08b416781d977693bcb97c4bab3ca89e4c9ab`, branch `feature/api-transaction`; alvo: alterações locais sem commit, incluindo arquivos novos. Alterações anteriores preservadas.

## Entrega e critérios

`app/core/database.py` resolve DATABASE explícito → DB_PATH da aplicação, ou DB_PATH do módulo sem contexto; valida destino antes da conexão. `app/run.py` exporta app sem acesso ao banco e prepara schema em main(), no contexto correto, antes do servidor. Factory, DDL e migração não foram modificados. README e arquitetura atualizados para preparação WSGI explícita.

F-003/AC-001 demonstrado em `app/tests/test_database_config.py`: CFG-01 ambiente/factory; CFG-02/03 schema e API no mesmo alvo, com sentinela intacta; CFG-04/07 resolução dinâmica e Path com foreign_keys=1; CFG-05 aplicações isoladas; CFG-06 destinos inválidos; CFG-08 importação; CFG-09 ordem/contexto; CFG-10/11 falhas impedem servidor. CFG-12 demonstrado pela suíte completa, incluindo schema/migração associados a AC-016/017. Recuperação pós-commit permanece em T-003.

## Verificações

Ambiente existente: Python 3.14.3 e pytest 9.0.3, sem novas dependências.

| Comando | Resultado |
|---|---|
| `.\.venv\Scripts\python.exe -m pytest app/tests/test_database_config.py -q --tb=no` antes da correção | 14 falhas e 8 erros; não constitui baseline seguro, ver incidente |
| Teste individual com `--tb=short` | Erro de criação do diretório temporário padrão no sandbox |
| `.\.venv\Scripts\python.exe -m pytest app/tests/test_database_config.py -q --tb=short --basetemp=.venv/pytest-t002-focused` | 22 aprovados em 0,27 s |
| `.\.venv\Scripts\python.exe -m pytest -q --basetemp=.venv/pytest-t002-full` | 240 aprovados em 4,76 s |
| `git diff --check` | Sem erros de whitespace; avisos de conversão LF/CRLF em arquivos anteriores |

Os diretórios de basetemp usados estavam ausentes antes dessas execuções. Para repetir, use um diretório descartável: pytest limpa o basetemp fornecido. Nenhum servidor real iniciado. Autoinspeção não representa revisão independente.

## Incidente da verificação anterior à correção

O teste inicial `test_schema_failure_prevents_server` importou o entrypoint antigo antes de substituir create_schema. Esse código executava a preparação no banco local. Isso contrariou o isolamento pretendido. O hash SHA256 previamente registrado era `3D02C0A098D0918B725C2507791B258AA6A373651326B98FEC87C2FB80C1977B`; após a execução inicial foi observado `B4280A85E644935E610A29A742BCE5868335D0C26E111A643A7093FE48ED790B`.

Não há comparação dos registros anterior/posterior que permita afirmar preservação ou quantificar mudanças. Não foi tentada restauração, migração adicional ou leitura dos dados pessoais. O usuário foi informado. Restaurar exigiria uma cópia anterior válida e autorização específica; não há recuperação real demonstrada.

Além de remover o efeito de importação em produção, foi adicionada proteção autouse no novo módulo de testes: conexões ao caminho do banco local são rejeitadas antes de SQLite. Os testes finais usam bancos sintéticos. Após a suíte completa, o hash continuou `B4280A85E644935E610A29A742BCE5868335D0C26E111A643A7093FE48ED790B`. Isso comprova ausência de mudança adicional nessa etapa, não desfaz o incidente inicial.

## Próxima ação

F-003/T-003: ensaiar migração e recuperação exclusivamente com dados sintéticos. Revisão técnica e avaliação do incidente local permanecem pendentes; nenhuma aprovação de produto, implantação ou recuperação foi declarada.
