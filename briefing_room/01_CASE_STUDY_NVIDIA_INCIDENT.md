# Case Study: NVIDIA SSO Federation Incident (October 2025)

## A Execução da Confiança
Análise de um incidente de federação SSO e a arquitetura de mitigação com o Protocolo Veritas.

### 1. A Tese: Não Confie, Execute
Este documento estabelece uma tese central para a segurança de infraestrutura moderna: não confie em identidade—execute confiança em cada requisição. A confiança, quando assumida implicitamente através de cadeias de federação de identidade (SSO), torna-se um vetor de risco sistêmico.
Analisamos um evento real ocorrido em 11 de outubro de 2025, no qual uma tentativa de federação de identidade foi processada pelo nosso sistema, Infracore. O resultado foi uma decisão de DENY, executada de forma automática e determinística pela nossa política de Policy-as-Code (FL-SSO-1.7.2). Toda a transação foi concluída em menos de 5 segundos, com impacto zero.

### 2. A Ameaça: A Falácia da Confiança em Federação SSO
A federação de identidade via SSO é um pilar da colaboração empresarial, mas sua implementação padrão introduz uma confiança transitiva perigosa. Quando a Organização A confia no IdP B, que por sua vez confia no IdP C, os riscos são propagados.

**Classes de Risco Sistêmico:**
*   **Propagação de Privilégios:** Um usuário com privilégios elevados em um sistema parceiro pode obter acesso indevido a recursos internos.
*   **Tomada de Controle Organizacional:** Uma conta comprometida em um parceiro federado pode ser utilizada para escalar privilégios na organização alvo.
*   **Violação de Compliance:** O acesso a dados regulados (LGPD, BACEN) pode ser concedido a identidades não verificadas, quebrando a cadeia de custódia.

**Análise da Causa Raiz (RCA)**
O incidente expõe três pontos de falha arquitetural comuns:

1.  **Quebra de Proveniência de Dados:** Associação incorreta de um domínio a uma entidade terceira sem validação de propriedade.
2.  **Falta de Consentimento Recíproco:** A plataforma alvo não exigiu aprovação explícita do proprietário do domínio.
3.  **Comunicação Opaca:** A notificação foi um "aviso" pós-fato, não uma "solicitação de ação" que poderia ser rejeitada programaticamente.

### 3. A Solução: Infracore e o Protocolo Veritas
Infracore opera como uma camada-zero de execução de confiança, mitigando esses riscos através de Consentimento Explícito e Policy-as-Code.

#### Diagrama de Fluxo Comparativo
A diferença arquitetural é melhor ilustrada visualmente.

**Fluxo 1: O Incidente Real (Confiança Assumida)**
```mermaid
graph TD
    A[User@domain] -->|Login| B(Directory Provider);
    B -->|Redirects| C(Computing Platform);
    C -->|Presents IdP_A token| B;
    B -->|Redirects to Target System| D{Target System};
    D -->|Tries SSO with Platform_B token| C;
    C -->|System trusts Platform_B token. No consent check.| E[ACCESS GRANTED (BREACH)];
```

**Fluxo 2: O Fluxo Protegido pelo Infracore (Confiança Executada)**
```mermaid
graph TD
    A[User@domain] -->|Login| B(Directory Provider);
    B -->|Redirects| C(Computing Platform);
    C -->|Presents IdP_A token| B;
    B -->|Redirects to Infracore| F{FoundLab Infracore};
    F -->|Tries SSO with Platform_B token| C;
    F -->|Execute Policy FL-SSO-1.7.2| G{Veritas Protocol};
    G -->|FAIL: Consent missing. RULE: deny by default.| F;
    F --> H[ACCESS DENIED (HTTP 403)];
    G -->|Seal 'DENY' Decision| I[Immutable Audit Trail];
```

### 4. Protocolo Veritas: A Cadeia de Evidências Imutável
Uma decisão de segurança só é válida se sua evidência for irrefutável. O protocolo é composto por:

*   **DecisionID:** Um identificador único global para cada transação.
*   **Hash-Chain:** Cada log contém o hash do registro anterior, criando uma cadeia criptográfica.
*   **WORM Sink:** Logs são escritos em armazenamento Write-Once, Read-Many.
*   **Metadados de Política:** Cada registro inclui a versão da política executada.

### 5. Análise do Incidente de 11 de Outubro de 2025

**Linha do Tempo Detalhada (UTC)**
*   `13:20:42Z`: `FEDERATION_REQUEST_INITIATED` - Requisição de SSO recebida.
*   `13:20:52Z`: `ANOMALY_DETECTED` - IA detecta que o iniciador não pertence ao grafo de relações.
*   `13:20:58Z`: `CONSENT_REQUEST_SENT` - Solicitação de consentimento enviada aos proprietários.
*   `13:21:08Z`: `CONSENT_REJECTED` - Administrador rejeita a solicitação.
*   `13:21:09Z`: `BURN_POLICY_ENFORCED` - Rejeição aciona o "Burn Engine" que aplica a política de negação.
*   `13:22:00Z`: `AUDIT_EXPORT_READY` - Pacote de evidências selado e disponibilizado.

---
*This document is a recreation of the events for educational and demonstrative purposes.*
