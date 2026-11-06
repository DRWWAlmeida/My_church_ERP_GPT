# Handoff — Organização local de branches

- **Origem e destino:** orquestrador → manutenção do repositório; sem executor adicional designado.
- **Estado:** pronto no escopo local; publicação remota autorizada, limpeza de nomes remotos pendente.
- **Pedido e escopo autorizado:** organizar as branches, preservando commits e trabalho pendente.
- **Data:** 05/11/2026, America/Sao_Paulo.
- **Artefatos:** referências Git locais e `GIT_GUIDELINES.md`.
- **Resultado:** trabalho local de acesso e interface associado à nova branch ativa `codex/mvp-acesso-interface`, criada em `62191868e884df7864dced06bbb3f42c32a89900`, a partir de `feature/api-transaction`. As alterações pendentes continuam sem commit; criar a branch não constitui backup desses arquivos.

| Branch local | Papel / destino |
|---|---|
| `main` | Linha estável, preservada em `b750c3e` |
| `develop` | Integração, preservada em `d3e8c68` |
| `feature/api-transaction` | Base preservada em `6219186` |
| `codex/mvp-acesso-interface` | Trabalho atual, sem upstream |
| `feature/api-category-update` | Preservada; commit exclusivo `fb395c4` exige avaliação |
| `development` | Renomeada para `archive/development` |
| `bugfix/category-api-hardening` | Renomeada para `archive/bugfix/category-api-hardening` |
| `feature/api-category-get` | Renomeada para `archive/feature/api-category-get` |
| `feature/api-checking-account` | Renomeada para `archive/feature/api-checking-account` |
| `feature/api-transaction-type` | Renomeada para `archive/feature/api-transaction-type` |

- **Decisões confirmadas:** o README define `develop` como base e integração antes de `main`; o manual foi alinhado a essa convenção.
- **Hipóteses:** arquivar nomes locais ancestrais do trabalho atual é organização reversível, não aprovação das funcionalidades. Upstreams originais foram preservados.
- **Verificações:** `git merge-base --is-ancestor` confirmou as cinco branches arquivadas como ancestrais de HEAD; comparação de `git status --porcelain=v1 --untracked-files=all` antes/depois e de `git rev-parse HEAD` confirmou preservação durante a operação; `git branch -vv` confirmou nomes e upstreams. Inspeção documental feita após a atualização do manual. Sem mudanças de lógica ou execução de testes da aplicação.
- **Limitações:** `graphify-out/graph.json` ausente; usadas fontes Git e documentos atuais. Referências `origin/*` são o estado conhecido localmente, sem fetch ou verificação remota nesta tarefa.
- **Riscos e pendências:** alterações de aplicação preexistentes permanecem sem commit. `feature/api-category-update` tem histórico exclusivo; não foi mesclada nem descartada. Nenhum push, exclusão remota, merge, rebase ou avanço de `main`/`develop` foi realizado.
- **Próxima ação recomendada:** revisar e versionar o trabalho atual em commits coerentes antes de propor sua integração em `develop`. Avaliar separadamente o commit exclusivo de categorias. Para desfazer um arquivamento local, usar `git branch -m archive/<nome-original> <nome-original>` enquanto o nome original estiver livre.

## Continuação — publicação no GitHub

- O usuário autorizou git push e organização no GitHub.
- A consulta remota confirmou seis branches: `main`, `develop`, `feature/api-transaction`, `bugfix/category-api-hardening`, `feature/api-checking-account` e `feature/api-transaction-type`. Não foram encontrados PRs abertos.
- A branch padrão encontrada foi `bugfix/category-api-hardening`. A primeira tentativa atômica foi recusada pelo GitHub porque incluía remover esse nome; nenhuma referência foi alterada nessa tentativa.
- A revisão automática de aprovação rejeitou a mudança de branch padrão para `main` em conjunto com a remoção dos nomes antigos, exigindo autorização explícita. Essas operações não foram executadas.
- Escopo do push preparado: nova branch de trabalho, cinco branches `archive/...`, branch de categorias com commit exclusivo e commit contendo apenas o manual Git e este registro. As alterações preexistentes da aplicação permanecem locais e sem commit.
- Pendência: autorizar explicitamente `main` como padrão e a remoção dos três nomes antigos após confirmar que seus commits estão preservados nas branches `archive/...`. Até lá, os nomes antigos e os arquivos históricos coexistirão no remoto.
