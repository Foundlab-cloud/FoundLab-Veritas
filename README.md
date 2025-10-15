# FoundLab Veritas

[![Validate Infracore Simulation](https://github.com/your-username/your-repo/actions/workflows/simulation_check.yml/badge.svg)](https://github.com/your-username/your-repo/actions/workflows/simulation_check.yml)
[![License](https://img.shields.io/badge/License-Proprietary-lightgrey)](LICENSE)
[![Infrastructure](https://img.shields.io/badge/Infrastructure-Terraform-blue)](terraform/)

> **A Ética Programável: Onde a verdade auditável é o primeiro passo para a confiança imutável.**

---

## 1. Visão Geral

**FoundLab Veritas** é o motor de auditoria criptográfica do ecossistema **Umbrella**. Ele implementa o **Veritas Protocol**, um sistema projetado para criar provas matemáticas de integridade para cada decisão de negócio, gerando uma trilha de auditoria imutável, segura e verificável.

Este repositório contém:

- O **código-fonte** para a geração e publicação de eventos de auditoria.
- A **infraestrutura como código (IaC)** para provisionar os recursos necessários no Google Cloud Platform (GCP).
- Uma **interface de linha de comando (CLI)** para interagir com o protocolo.

## 2. Arquitetura e Fluxo

O Veritas opera sobre uma arquitetura serverless no GCP, garantindo escalabilidade, segurança e baixo custo operacional.

O fluxo de um evento de auditoria é o seguinte:

1. **Geração do Evento:** Uma aplicação (neste caso, a CLI) utiliza o módulo `foundlab.core.veritas` para criar um evento criptograficamente encadeado.
2. **Publicação:** O evento é publicado de forma assíncrona num tópico do **Google Pub/Sub**.
3. **Processamento:** Uma **Cloud Function** é acionada pela mensagem no tópico.
4. **Armazenamento:** A Cloud Function armazena o evento na tabela `audit.Veritas_Audit_Trail` no **Google BigQuery**, completando a trilha de auditoria.

## 3. Como Começar

Toda a configuração do ambiente, desde a autenticação local até o deploy da infraestrutura, está detalhada no nosso guia completo.

➡️ **Para começar, siga as instruções em: [`BLUEPRINT_SETUP.md`](BLUEPRINT_SETUP.md)**

O blueprint cobre:

- Configuração do ambiente local e autenticação com o GCP.
- Limpeza de segredos do histórico do Git (passo de segurança obrigatório).
- Configuração do Google Secret Manager para chaves privadas.
- Inicialização do Terraform com backend remoto.
- Deploy da infraestrutura e da aplicação.

## 4. Uso da CLI

Após seguir o `BLUEPRINT_SETUP.md`, você pode usar a CLI para gerar e publicar eventos de auditoria.

**Exemplo: Assinar um documento e gerar um evento `DOCUMENT_SIGNED`**

```bash
# Certifique-se de que a variável de ambiente GCP_PROJECT_ID está definida
# Exemplo para PowerShell:
# $env:GCP_PROJECT_ID="seu-projeto-id"

# Execute o comando de assinatura
python foundlab/cli/main.py sign alice README.md
```

Este comando irá:

1. Assinar o arquivo `README.md` com a chave privada de `alice` (carregada do Secret Manager).
2. Gerar um evento Veritas Protocol completo.
3. Publicar o evento no Google Pub/Sub.
4. Imprimir o evento no console para sua verificação.

### Assinando um Arquivo

Para assinar um arquivo, você precisa do nome de um signatário cuja chave privada esteja armazenada no Secret Manager.

```bash
# Exemplo: Assinar o arquivo README.md com a chave de 'alice'
python foundlab/cli/main.py sign alice README.md
```

Isso criará um arquivo de assinatura chamado `README.md.sig`.

### Verificando uma Assinatura

Para verificar uma assinatura, você precisa do arquivo original, do arquivo de assinatura e do nome do signatário.

```bash
# Exemplo: Verificar a assinatura do README.md
python foundlab/cli/main.py verify alice README.md README.md.sig
```

## 5. Infraestrutura como Código (Terraform)

Toda a infraestrutura do Veritas é gerenciada pelo Terraform e está localizada no diretório `/terraform`.

- **`main.tf`**: Define todos os recursos (BigQuery, Pub/Sub, Service Accounts, etc.).
- **`variables.tf`**: Declara as variáveis de configuração (ID do projeto, região).
- **`terraform.tfvars`**: **(Arquivo local, não versionado)** Onde você define os valores para as variáveis.

Para aplicar a infraestrutura, navegue até o diretório `terraform` e execute `terraform apply`.

## 6. Fluxos de Autenticação: Estado Atual vs. Proposto

| Fluxo Vulnerável de SSO (Confiança Assumida) | Fluxo Protegido (Confiança Executada pelo Veritas) |
| :--- | :--- |
| ```mermaid
graph TD
    subgraph "NVIDIA Platform (Estado Atual)"
        A[Usuário @ Accenture] -->|1. Tenta Fazer Login| B(IdP);
        B -->|2. Redireciona com Token| C(NVIDIA NGC);
        C -->|3. Confia no Token Implicitamente| D[<font color=red>VIOLAÇÃO</font><br>Acesso Permitido];
    end
``` | ```mermaid
graph TD
    subgraph "Fluxo Proposto com Veritas"
        A[Usuário @ Accenture] -->|1. Tenta Fazer Login| B(IdP);
        B -->|2. Redireciona para Veritas| E{Protocolo Veritas};
        E -->|3. Executa Política| F[<font color=green>NEGAR</font><br>Sem Consentimento];
        E -->|4. Lacra Decisão| G(Livro Imutável);
    end
``` |

---
© FoundLab. Todos os direitos reservados.
