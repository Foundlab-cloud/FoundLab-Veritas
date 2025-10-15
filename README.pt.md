# FoundLab IEM VERITAS: Uma Demonstração Viva de Federação SSO Auditável

[![Validate Infracore Simulation](https://github.com/your-username/your-repo/actions/workflows/simulation_check.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/simulation_check.yml)

**[Policy-as-Code] &nbsp;&nbsp; [Arquitetura Zero-Trust] &nbsp;&nbsp; [Trilha de Auditoria Imutável] &nbsp;&nbsp; [Pronto para SOC2]**

---

## A Premissa: Não Confie, *Execute*.

Em 11 de Outubro de 2025, uma tentativa não autorizada de tomada de controle da conta administrativa da FoundLab na plataforma NVIDIA NGC foi detectada e neutralizada. Este repositório não apenas analisa o incidente; ele o recria, permitindo que você **execute a prova** de como uma infraestrutura de confiança moderna bloqueia deterministicamente tais ameaças.

Esta é uma demonstração ao vivo da tese central da FoundLab: em um mundo de cadeias de suprimentos complexas e identidade federada, a confiança não deve ser assumida. Ela deve ser executada programaticamente e provada criptograficamente.

## A Simulação: Recrie o Incidente

Criamos uma simulação autocontida que replica a tentativa de federação SSO não autorizada. Você pode executá-la em sua máquina local em menos de 60 segundos.

### 1. Execute a Prova

Navegue até o diretório da simulação e execute o script:

```bash
cd infracore_simulation
pip install -r ../requirements.txt
python main.py
```

### 2. Resultado Esperado

O script o guiará através do incidente, desde a ingestão até a negação final orientada por políticas. A saída do terminal será clara e inequívoca:

```plaintext
--- Infracore Simulation: Unauthorized SSO Federation ---
Timestamp: 2025-10-15T18:00:00.123456+00:00

[STEP 1/5] INGESTION: Unauthorized SSO federation request received.
   > Initiator: Accenture
   > Consent Granted: False

[STEP 2/5] POLICY EXECUTION: Evaluating 'sso_federation_policy.rego'...
   > Policy evaluation result: ALLOW = False

[STEP 3/5] DECISION: Policy evaluation complete.
   > Result: ACCESS DENIED
   > Reason(s): REL_001_NO_VERIFIED_RELATIONSHIP, POL_403_HARD_DENY_IF_NO_CONTRACT

[STEP 4/5] VERITAS SEAL: Generating cryptographic proof of the decision...
   > DecisionID: dec-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   > Final Chain Hash: <sha256_hash>

[STEP 5/5] PROOF GENERATION: Writing immutable audit trail to disk...
   > Success! Audit trail written to:
     /path/to/FoundLab-Veritas/infracore_simulation/veritas_audit_trail.jsonl

--- Simulation Complete ---
```

O arquivo `veritas_audit_trail.jsonl` gerado é a **prova matemática** da decisão, um registro de ledger imutável que é admissível para qualquer auditoria.

## A Arquitetura: Como Funciona

A simulação é alimentada pelos mesmos princípios que impulsionam nossa plataforma de produção.

### Fluxo Comparativo: Vulnerável vs. Protegido

Este diagrama ilustra a diferença crítica entre um fluxo de SSO padrão e vulnerável e um protegido pelo Protocolo Veritas.

| Fluxo SSO Vulnerável (Confiança Assumida) | Fluxo Protegido (Confiança Executada pelo Veritas) |
| :--- | :--- |
| ```mermaid
graph TD
    subgraph "Plataforma NVIDIA (Estado Atual)"
        A[Usuário @ Accenture] -->|1. Tenta Login| B(IdP);
        B -->|2. Redireciona com Token| C(NVIDIA NGC);
        C -->|3. Confia no Token Implicitamente| D[<font color=red>FALHA</font><br>Acesso Concedido];
    end
``` | ```mermaid
graph TD
    subgraph "Fluxo Proposto com Veritas"
        A[Usuário @ Accenture] -->|1. Tenta Login| B(IdP);
        B -->|2. Redireciona para o Veritas| E{Protocolo Veritas};
        E -->|3. Executa Política| F[<font color=green>NEGADO</font><br>Sem Consentimento];
        E -->|4. Sela Decisão| G(Ledger Imutável);
    end
``` |

## A Sala de Guerra: Análise Aprofundada

Para uma compreensão abrangente do incidente e de nossa arquitetura, compilamos um dossiê completo.

*   **[00_EXECUTIVE_SUMMARY.md](./briefing_room/00_EXECUTIVE_SUMMARY.md)**: Um resumo de uma página para liderança (PT/EN).
*   **[01_CASE_STUDY_NVIDIA_INCIDENT.md](./briefing_room/01_CASE_STUDY_NVIDIA_INCIDENT.md)**: Uma análise detalhada do incidente de federação.
*   **[02_TECHNICAL_WHITEPAPER.md](./briefing_room/02_TECHNICAL_WHITEPAPER.md)**: O whitepaper técnico completo da Plataforma Umbrella.
*   **[03_VERITAS_PROTOCOL.md](./briefing_room/03_VERITAS_PROTOCOL.md)**: Um aprofundamento técnico em nossa tecnologia de trilha de auditoria criptográfica.

## Próximos Passos: Um Novo Padrão para Segurança

A mesma arquitetura que protege contra esta falha de SSO pode proteger seus fluxos de trabalho operacionais e de conformidade mais críticos. Ela fornece uma camada de confiança programável e auditável que é essencial para empresas modernas.

**A FoundLab está preparada para ajudar a NVIDIA a ser pioneira neste novo padrão de segurança.**

*   **Contate-nos para uma demonstração técnica aprofundada:** [contact@foundlab.cloud](mailto:contact@foundlab.cloud)
*   **Explore uma parceria estratégica para integrar o Veritas ao ecossistema NVIDIA.**

---

*Aviso: Este repositório contém uma demonstração funcional para fins educacionais e de auditoria. A solução comercial está disponível como um serviço gerenciado e escalável.*
