# Contrato técnico — configuração e inicialização

Versão 0.1, 03/11/2026. Entrega de F-003/T-001, baseada em `02d08b416781d977693bcb97c4bab3ca89e4c9ab` e no estado local. Referências: [arquitetura](../../architecture/overview.md), [modelo de dados](../../architecture/data-model.md), [plano](plan.md), F-003/AC-001 e AC-016/017 do [PRD](../../product/PRD.md).

**Estado:** implementado por T-002 em 04/11/2026; [evidências e incidente da verificação inicial](evidencias-t002.md). Escolhas locais seguem a proposta arquitetural de resolução única, factory sem schema e preparação controlada. Não altera stack ou regra de negócio, nem declara ADRs aceitos ou revisão independente realizada.

## Diagnóstico observado antes da implementação

| Situação atual | Resultado |
|---|---|
| Configuração padrão | `app.config.DB_PATH` obtém DATABASE_PATH na importação ou caminho padrão app/db/igreja_erp.db |
| Contexto Flask com DATABASE | Conexão usa DATABASE; fixtures existentes dependem disso |
| Contexto com apenas DB_PATH sobrescrito | Conexão ignora essa alteração e usa a cópia importada por core.database |
| Sem contexto Flask | Usa a cópia de DB_PATH capturada ao importar core.database |
| Importar app.run | Executa create_schema antes da factory, mesmo sem iniciar servidor |
| Chamar create_app | Carrega configuração e blueprints, sem abrir conexão ou preparar schema |

Diagnóstico confirmado com connect/schema/factory substituídos por mocks; nenhum acesso real ao banco nessa sondagem. Testes existentes de migração rodaram separadamente em bases isoladas.

## Resolução de destino para T-002

`DATABASE` será a chave canônica de sobrescrita explícita por aplicação, preservando fixtures e chamadores atuais. `DB_PATH` permanece como configuração de base e fallback compatível; a variável externa continua sendo `DATABASE_PATH`. Não remover alias nesta entrega nem adicionar duas cópias padrão que possam divergir.

Ordem exata:

1. **Com contexto Flask:** se a chave `DATABASE` estiver presente, usar seu valor; caso contrário, usar `current_app.config['DB_PATH']`.
2. **Sem contexto Flask:** usar `app.config.DB_PATH` do módulo de configuração no momento da resolução, sem cópia congelada em `core.database`.
3. `app.config.DB_PATH` mantém a leitura de `DATABASE_PATH` na importação do módulo; variável ausente mantém o padrão atual. Alterações de variável de ambiente depois da importação não reconfiguram aplicações existentes. Configurar ambiente antes de carregar o processo; nos testes, usar sobrescrita explícita de configuração.

Não definir `DATABASE` com o valor padrão na factory: a presença dessa chave impediria a sobrescrita compatível de `DB_PATH`. Se ambas forem fornecidas, `DATABASE` vence, sem ambiguidade. A chave efetiva deve ser resolvida pela mesma função usada por schema e repositórios, sem caminhos alternativos na inicialização.

Aceitar caminhos string não vazios ou `os.PathLike`, incluindo Path. Não expandir variáveis, criar diretórios automaticamente ou converter um caminho inválido no padrão. Caminhos relativos continuam relativos ao diretório de trabalho, como hoje; execução documentada parte da raiz. Nenhuma opção de URI SQLite será ativada implicitamente.

Valor explícito None, string vazia, somente espaços ou tipo inadequado deve resultar em erro de configuração claro (ValueError), antes de conectar. Não usar fallback silencioso para outro banco. Arquivo inacessível ou diretório pai ausente deve conservar a falha SQLite; nunca iniciar servidor após falha de preparação. Tratamento HTTP universal de configuração inválida não entra no escopo de T-002: configuração é pré-condição operacional.

`:memory:` continua sendo aceito pelo SQLite, mas cada conexão terá sua própria base; não prometer persistência entre chamadas de repositório. Os testes de integração de configuração usarão arquivos temporários; fixtures de migração em memória mantêm sua conexão específica.

`get_connection()` continua abrindo uma conexão por chamada e habilitando `PRAGMA foreign_keys = ON`. Não adicionar pool, WAL, retry ou política nova de timeout. Repositórios/scripts continuam responsáveis por fechamento e transações.

## Inicialização e compatibilidade

- `create_app()` mantém assinatura sem argumentos e continua sem acesso ao banco. Não é necessário ampliar sua API para resolver esta tarefa.
- `app.run` pode continuar exportando `app = create_app()` para compatibilidade de importação, mas importar esse módulo não deve abrir banco, executar schema ou iniciar servidor.
- A execução `python -m app.run` deve invocar uma função de entrada, proposta `main()`: entrar no contexto da mesma aplicação exportada, executar `create_schema()` uma vez nessa invocação, sair do contexto e só então iniciar `app.run(debug=app.config['DEBUG'])`.
- Falha em create_schema propaga e impede a chamada ao servidor. Não capturar a falha para continuar com schema incompleto. O bloco de execução deve ficar sob `if __name__ == '__main__'`.
- A preparação usa o contexto da aplicação servida, inclusive sobrescritas DATABASE/DB_PATH. Não criar segunda aplicação para migrar ou preparar fora do contexto antes de criar a aplicação.
- “Uma vez” significa por invocação da função de entrada, não bloqueio global entre processos. Reloader de debug pode executar novamente; a migração existente deve permanecer idempotente. Não apresentar o entrypoint de desenvolvimento como coordenação de implantação multiprocesso.

Importar `app.run:app` deixará de migrar automaticamente: essa é uma mudança intencional de efeito colateral. O comando local mantém preparação automática antes de servir. Para carregadores que apenas importam a aplicação, documentar preparação separada e explícita, sob contexto, antes dos processos de atendimento. Não implementar novo servidor, provedor, CLI de deploy ou mecanismo distribuído nesta tarefa.

## Cenários de verificação de T-002

Os IDs abaixo são locais a este contrato e detalham F-003/AC-001, sem substituir critérios do PRD.

| ID | Preparação e ação | Resultado obrigatório |
|---|---|---|
| CFG-01 | Criar aplicação com ambiente controlado e sem override explícito | DB_PATH corresponde a DATABASE_PATH; sem variável, corresponde ao padrão, sem conexão durante factory |
| CFG-02 | Aplicação com DB_PATH=A, sem DATABASE; preparar schema e criar/consultar cadastro pela API | Apenas A usado; B, banco sentinela, permanece intacto |
| CFG-03 | DB_PATH=A e DATABASE=B; preparar e usar API | Apenas B recebe schema/dados; A permanece intacto |
| CFG-04 | Sem contexto, sobrescrever app.config.DB_PATH para A após importar core.database | get_connection usa A; nenhuma cópia antiga do destino é usada |
| CFG-05 | Duas aplicações com destinos diferentes, alternar contextos | Conexões/consultas não misturam registros ou configuração |
| CFG-06 | DATABASE presente mas None/vazio/branco/tipo inválido; repetir em DB_PATH quando não há DATABASE | ValueError antes de connect; nenhum fallback ou arquivo inesperado |
| CFG-07 | Destino válido como Path; consultar PRAGMA foreign_keys em conexão real temporária | Caminho aceito e foreign_keys=1 |
| CFG-08 | Importar app.run com schema/conexão/servidor monitorados | Nenhum deles chamado; factory pode ser criada |
| CFG-09 | Executar função main com servidor substituído e banco temporário configurado | Schema uma vez por invocação, no contexto correto, antes de run; dados da preparação são acessíveis pela API |
| CFG-10 | Schema lança exceção durante main | Servidor não é chamado; exceção permanece observável |
| CFG-11 | Diretório pai de destino configurado inexistente, em área temporária | Preparação falha e servidor não inicia; padrão não é usado nem diretório criado silenciosamente |
| CFG-12 | Rodar testes existentes de schema, migração e suíte completa após implementação | AC-016/017 preservados; fixtures com DATABASE continuam isoladas |

Para CFG-01, isolar variáveis antes da importação em processo de teste ou carregar configuração de forma controlada; não depender do ambiente pessoal da máquina. Para CFG-02/03, criar sentinela sintética e comparar hash/schema/conteúdo antes e depois. Nunca usar o banco real como alvo da preparação.

Arquivos previstos para T-002: `app/config.py` se necessário, `app/core/database.py`, `app/run.py`, novo `app/tests/test_database_config.py` e README. Evitar mudanças na factory, fixtures ou migração se o contrato puder ser satisfeito preservando-os.

## Migração, recuperação e revisão

Este contrato não altera DDL nem conversão monetária. T-002 deve manter transação e rollback existentes. A mudança do resolvedor não autoriza migrar ou mover arquivo; verificar o destino efetivo antes de qualquer operação real futura.

Reverter o código de configuração não desfaz migração de centavos já confirmada; recuperação de dados segue o modelo arquitetural e será ensaiada em F-003/T-003. Nenhuma recuperação real ocorre nesta entrega.

Revisão técnica da implementação deve verificar precedência, compatibilidade das fixtures, ausência de efeitos de importação e interrupção em falha. Não há divergência identificada que exija bloquear T-002 por nova decisão arquitetural: as opções estão dentro da proposta de unificação e preparação controlada. Se surgirem exigências de outra assinatura pública, servidor, configuração por usuário ou mudança de armazenamento, devolver a decisão ao arquiteto antes de ampliar o escopo.
