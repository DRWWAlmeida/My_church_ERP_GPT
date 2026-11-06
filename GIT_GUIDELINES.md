# 📖 Manual de Boas Práticas de Versionamento (Git)

Este documento estabelece os padrões de desenvolvimento e controle de versão adotados no projeto. O objetivo é garantir um histórico de código limpo, rastreável e facilitar o trabalho em equipe.

---

## 📌 1. Padrão de Commits (Conventional Commits)

Todas as mensagens de commit devem seguir a especificação do [Conventional Commits](https://conventionalcommits.org).

### Estrutura
```text
<tipo>(<escopo opcional>): <descrição curta em letras minúsculas>
```

### Tipos de Commit principais
*   **`feat:`** Introduz uma nova funcionalidade no código (ex: `feat(category): adiciona rota put para atualização`).
*   **`fix:`** Corrige um bug ou problema (ex: `fix(auth): corrige expiração do token`).
*   **`docs:`** Alterações exclusivas na documentação (ex: `docs: atualiza instruções do readme`).
*   **`style:`** Mudanças de formatação que não alteram a lógica (espaços, lint, ponto e vírgula).
*   **`refactor:`** Alteração de código que não corrige bug nem adiciona funcionalidade, mas melhora a estrutura.
*   **`test:`** Adiciona ou modifica testes existentes.
*   **`chore:`** Atualizações de tarefas de build, pacotes ou ferramentas de desenvolvimento (ex: `chore: atualiza axios`).

### Regras de Ouro para Mensagens
1.  **Use o modo imperativo:** Escreva como uma ordem (ex: `adiciona`, `corrige`, `remove`). Nunca use no gerúndio (`adicionando`) ou passado (`adicionado`).
2.  **Seja direto:** O título deve ter no máximo 50 caracteres.
3.  **Sem ponto final:** Não termine o título com ponto `.`.
4.  **Commits Atômicos:** Faça commits pequenos e frequentes. Cada commit deve resolver apenas um assunto.

---

## 🌿 2. Fluxo de Trabalho e Branches

A ramificação principal do projeto deve ser protegida e mantida estável. **Nunca desenvolva ou faça commits diretamente na branch principal (`main`/`master`).**

### Nomenclatura de Branches
Utilize letras minúsculas e separe os termos por hífen. O prefixo deve indicar o tipo de tarefa seguido por uma barra `/`:

*   **Funcionalidades:** `feature/nome-da-tarefa` (ex: `feature/api-category-update`)
*   **Correções de bug:** `bugfix/nome-do-erro` (ex: `bugfix/login-desktop`)
*   **Correções urgentes em produção:** `hotfix/ajuste-urgente`
*   **Trabalho conduzido pelo Codex:** `codex/nome-da-tarefa`
*   **Histórico local arquivado:** `archive/nome-original` (preserva o commit e o upstream; não é base para novas tarefas)

`main` representa a linha estável; `develop` é a linha de integração.
`development` é um nome legado, arquivado localmente como `archive/development`.
Branches arquivadas não comprovam aprovação ou integração em `main`.

### Rotina Diária
1.  Antes de iniciar qualquer tarefa, atualize seu repositório local:
    ```bash
    git switch develop
    git pull --ff-only
    ```
2.  Crie sua branch a partir da versão mais recente de `develop`:
    ```bash
    git checkout -b feature/sua-tarefa
    ```
3.  Integre e teste em `develop` antes de promover para `main`, mediante a autorização aplicável.

Antes de trocar de branch, confira `git status` e preserve trabalho pendente.
Quando uma tarefa depender de alterações ainda não integradas, registre explicitamente
a branch e o commit usados como base. Não atualize `develop` ou `main` apenas para
organizar nomes de branches.

O inventário e as pendências da organização local estão em
[docs/handoff-organizacao-branches.md](docs/handoff-organizacao-branches.md).

---
