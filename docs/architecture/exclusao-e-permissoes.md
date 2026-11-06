# Atualização de arquitetura — exclusão e permissões

Data: 04/11/2026. Fonte: decisões explícitas do solicitante e [PRD v0.3](../product/PRD.md). Estado: regras confirmadas, desenho técnico proposto, sem implementação.

## Regras confirmadas

- REQ-014/028: somente Administrador gere contas, papéis e permissões. Catálogo, ciclo e retenção eterna do histórico de auditoria estão definidos na matriz F-004; contrato técnico permanece pendente.
- REQ-008: exclusão definitiva de lançamentos sem restrição temporal, preservando a exigência de autorização. Não significa permissão de exclusão para todos os usuários.
- REQ-015: categoria, conta bancária e tipo de transação só podem ser excluídos sem qualquer lançamento vinculado. Mesmo um vínculo fora da visibilidade do solicitante impede a exclusão, sem revelar dados desse lançamento.

## Contrato técnico proposto

Acrescentar DELETE `/category/<int:category_id>`, `/checking-account/<int:checking_account_id>` e `/transaction-type/<int:transaction_type_id>`. Validar ID positivo até 9223372036854775807 conforme convenção atual. Sucesso: 204 sem corpo; recurso ausente no escopo autorizado: 404; ID inválido tratado pelo schema: 400. Vínculo existente: 400 com envelope de IntegrityError e mensagem genérica de cadastro em uso, mantendo a política atual de integridade. Falha operacional: 500 genérico. Os códigos de autenticação/autorização serão fechados em F-004/T-002; não há exceção anônima proposta. Limitações atuais do conversor de rota permanecem descritas em contracts.md.

Autorizar ação e escopo antes da mutação. No repositório, usar uma única transação de escrita para verificar existência, verificar vínculos e excluir; manter foreign_keys habilitado e a proteção referencial do banco. Não usar cascata, não remover lançamentos nem anular referências. Na disputa com criação/edição de lançamento, ou o vínculo impede a exclusão, ou a remoção impede a referência posterior; nunca confirmar referência órfã. Falha deve reverter a operação e fechar a conexão.

Excluir lançamento não remove seus cadastros. Um cadastro fica elegível quando não restar lançamento que o utilize; não há exclusão automática. Nenhuma migração de dados é presumida: conferir DDL e restrições durante planejamento. Se alteração de schema for necessária, descrever compatibilidade e recuperação antes da implementação.

## Impactos e verificação prevista

F-004 deve incluir autorização de DELETE dos três cadastros na matriz e testes negativos. F-005 deve incluir ação de excluir cadastro, estado de cadastro em uso e atualização após sucesso. O planejador deve acrescentar tarefas rastreáveis para REQ-015/AC-023/AC-024, sem reabrir como incompletas as verificações já concluídas de F-001.

Testar os três cadastros sem vínculo, com um/múltiplos vínculos, após remoção do último vínculo, ID ausente/inválido, autorização negada, vínculo fora do escopo, rollback e concorrência. Testar REQ-008 sem restrição por data. Estas verificações estão previstas, não executadas.

Pendências: contrato técnico de identidade/histórico e Q-005/Q-006/Q-007 (operação/moeda). A retenção eterna do histórico está decidida; Q-002 está resolvida: igreja única. Esta atualização prevalece sobre menções históricas de política de exclusão inteiramente indefinida; não resolve essas outras perguntas.
