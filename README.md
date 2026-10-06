# End-to-end data platform on AWS: from raw e-commerce data to an AI layer over customer reviews

> 🚧 Work in progress — built incrementally, one layer per week. See [Progress](#progress).

## Overview

This project builds a data platform on AWS that turns raw e-commerce data into an AI-ready layer. It uses the public [Olist dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce): ~100k real orders from a Brazilian marketplace (2016–2018), across nine related tables, plus ~40k customer reviews written in Portuguese.

The goal is to go beyond a classic pipeline: reviews are enriched with order context from the modeled layer (delivery delay, product category, rating, region) and served through a RAG application, so sellers can ask questions like *"what do customers complain about in late deliveries?"* and get answers grounded in real data.

## Architecture

1. **Ingestion** — Python loads raw CSVs into the S3 bronze layer
2. **Processing** — AWS Glue (PySpark) cleans and deduplicates into silver
3. **Catalog** — Glue Data Catalog registers tables
4. **Transformation** — dbt on Amazon Athena builds the gold layer, with tests and lineage
5. **Orchestration** — Apache Airflow runs the end-to-end pipeline
6. **AI layer** — reviews enriched with gold-layer context, embedded and stored in a vector database
7. **RAG** — LangChain retrieval with LLM comparison (cost, latency, quality)
8. **Serving** — API on AWS Lambda + API Gateway, infrastructure as code with Terraform

## Tech stack

- **Cloud:** AWS (S3, Glue, Athena, Lambda, API Gateway, DynamoDB)
- **Infrastructure as code:** Terraform
- **Transformation:** dbt
- **Orchestration:** Apache Airflow
- **AI:** embeddings, vector database, LangChain
- **Language:** Python, SQL

## Repository structure

- `infra/` — Terraform configuration for all AWS resources
- `ingestion/` — Python scripts for data ingestion
- `dbt/` — transformation and data modeling
- `airflow/` — DAGs and orchestration
- `docs/` — documentation and IAM policies

## Getting started

### Prerequisites

- An AWS account
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) v2.32 or later
- [Terraform](https://developer.hashicorp.com/terraform/install) v1.16 or later

### Authentication

This project uses `aws login` (console credentials) instead of long-lived access keys.

1. Sign in through the CLI:

   ```bash
   aws login --profile <your-profile>
   ```

2. Terraform does not read `aws login` sessions directly yet. Create a second profile in `~/.aws/config` that exposes the session through `credential_process` ([see AWS docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sign-in.html)). The provider expects this profile to be named `olist-tf`.

3. Check the identity:

   ```bash
   aws sts get-caller-identity --profile olist-tf
   ```

### Deploy the infrastructure

```bash
cd infra
terraform init
terraform plan
terraform apply
```

## Design decisions

- **No access keys on disk** — authentication uses `aws login`, which issues short-lived credentials (refreshed every 15 minutes, valid up to 12 hours). Nothing secret is stored locally or in the repository.
- **Cost guardrails first** — a monthly spend limit and an AWS Budget were set before any resource was created.
- **Least privilege** — IAM policies grant only the actions each component needs (e.g. [read-only S3 access](docs/iam/s3-readonly-policy.json): `ListBucket` on the bucket, `GetObject` on its objects).
- **Pinned versions** — Terraform and the AWS provider are pinned to a major version, and the lock file is committed, so every `init` resolves the same provider.

## Progress

- [ ] **Week 1** — AWS account, cost guardrails, IAM, Terraform setup *(in progress)*
- [ ] **Week 2** — S3 bronze layer, Glue Catalog, Athena
- [ ] **Week 3** — Glue job (PySpark) and silver layer
- [ ] **Week 4** — dbt on Athena and Airflow orchestration
- [ ] **Weeks 5–8** — AI layer: enrichment, embeddings, RAG, API
- [ ] **Weeks 9–12** — reusable components, data quality, CI/CD, documentation
