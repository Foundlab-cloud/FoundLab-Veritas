# FoundLab Veritas

[![FoundLab](https://img.shields.io/badge/FoundLab-Veritas-blueviolet)](https://foundlab.com.br)
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
python foundlab/cli/main.py sign alex README.md
```

Este comando irá:

1. Assinar o arquivo `README.md` com a chave privada de `alex` (carregada do Secret Manager).
2. Gerar um evento Veritas Protocol completo.
3. Publicar o evento no Google Pub/Sub.
4. Imprimir o evento no console para sua verificação.

## 5. Infraestrutura como Código (Terraform)

Toda a infraestrutura do Veritas é gerenciada pelo Terraform e está localizada no diretório `/terraform`.

- **`main.tf`**: Define todos os recursos (BigQuery, Pub/Sub, Service Accounts, etc.).
- **`variables.tf`**: Declara as variáveis de configuração (ID do projeto, região).
- **`terraform.tfvars`**: **(Arquivo local, não versionado)** Onde você define os valores para as variáveis.

Para aplicar a infraestrutura, navegue até o diretório `terraform` e execute `terraform apply`.

---
© FoundLab. Todos os direitos reservados.
