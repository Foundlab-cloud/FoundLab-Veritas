# Blueprint de Setup e Boas Práticas - FoundLab Veritas

Este documento descreve os passos essenciais para configurar o ambiente de desenvolvimento e produção do projeto Veritas, seguindo as melhores práticas de segurança e infraestrutura como código.

## 1. Configuração do Ambiente Local (Pré-requisito)

**Objetivo:** Autenticar sua máquina local para interagir com os serviços do Google Cloud (GCP).

**Passos:**

1. **Instale o `gcloud` CLI:** Siga as instruções oficiais para [instalar o Google Cloud SDK](https://cloud.google.com/sdk/docs/install).

2. **Autentique-se:** Execute o seguinte comando e siga as instruções no seu navegador para fazer login com a sua conta Google Cloud:

   ```bash
   gcloud auth application-default login
   ```

3. **Defina a Variável de Ambiente:** O código precisa saber qual projeto GCP usar. Defina a seguinte variável de ambiente no seu terminal:

   ```bash
   # Para PowerShell (Windows)
   $env:GCP_PROJECT_ID="seu-gcp-project-id-aqui"

   # Para Bash (Linux/macOS)
   export GCP_PROJECT_ID="seu-gcp-project-id-aqui"
   ```

   **Importante:** Substitua `"seu-gcp-project-id-aqui"` pelo ID real do seu projeto.

## 2. Limpeza de Segredos do Repositório (Ação Única e Obrigatória)

**Objetivo:** Remover permanentemente as chaves privadas (`.pem`) do histórico do Git para mitigar riscos de segurança.

**Ferramenta:** [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/)

**Passos:**

1. **Instale o BFG Repo-Cleaner.**
2. Navegue até a raiz do seu repositório clonado.
3. Execute o seguinte comando para remover todos os arquivos `*_priv.pem`:

   ```bash
   bfg --delete-files "*_priv.pem"
   ```

4. Finalize o processo de limpeza do Git:

   ```bash
   git reflog expire --expire=now --all && git gc --prune=now --aggressive
   ```

5. Faça um `push --force` para o seu repositório remoto para atualizar o histórico.

## 3. Configuração do Google Secret Manager

**Objetivo:** Armazenar as chaves privadas dos signatários de forma segura.

**Passos:**

1. Para cada signatário (ex: `alex`, `patrick`, `raissa`), crie um segredo no Google Secret Manager.
2. O nome do segredo deve seguir o padrão: `veritas_signer_<NOME>_priv`.
   - Exemplo: `veritas_signer_alex_priv`
3. O valor do segredo deve ser o conteúdo exato do arquivo `.pem` da chave privada correspondente.

## 4. Configuração do Terraform com Backend Remoto

**Objetivo:** Gerenciar a infraestrutura como código de forma segura e colaborativa.

**Passos:**

1. **Crie o Bucket para o Estado do Terraform:**
   Execute o seguinte comando no `gcloud` para criar o bucket que armazenará o arquivo de estado:

   ```bash
   gsutil mb gs://foundlab-veritas-tfstate
   ```

   *(Se o bucket já existir, você pode pular esta etapa.)*

2. **Configure suas Variáveis de Ambiente:**
   - Navegue até o diretório `terraform/`.
   - Renomeie o arquivo `terraform.tfvars.example` para `terraform.tfvars`.
   - Edite `terraform.tfvars` e substitua `"seu-gcp-project-id-aqui"` pelo ID do seu projeto Google Cloud.

3. **Inicialize o Terraform:**
   - Ainda no diretório `terraform/`, execute o comando:

   ```bash
   terraform init
   ```

   - O Terraform irá detectar a configuração do backend e pedir para você confirmar a migração do estado. Digite `yes`.

Após estes passos, seu ambiente estará configurado corretamente.

## 5. Deploy da Aplicação

**Objetivo:** Realizar o deploy da Cloud Function de forma automatizada e segura.

**Passos:**

1. **Aplique a Configuração do Terraform:**
   No diretório `terraform/`, execute:

   ```bash
   terraform apply
   ```

   Confirme a aplicação digitando `yes`. Isto irá criar todos os recursos na GCP, incluindo a Service Account.

2. **Execute o Script de Deploy:**
   Na raiz do projeto, execute o script:

   ```bash
   bash gcp/deploy_gcp.sh
   ```

   O script irá obter as informações necessárias do Terraform e realizar o deploy da Cloud Function com a Service Account correta.
