# CIS OneOps Enterprise Production Release

## Architecture Overview
CIS OneOps is a full-featured, enterprise-grade Cybersecurity Operations Platform. It is built on a microservices architecture designed for high availability, multi-tenancy, and real-time processing.

### Tech Stack
- **Backend**: FastAPI (Python), SQLAlchemy (PostgreSQL), Kafka (Event Streaming)
- **Frontend**: React, Tailwind CSS, WebSockets
- **IAM**: Keycloak (OIDC/SSO/MFA)
- **Secrets**: HashiCorp Vault
- **Infrastructure**: Kubernetes, Helm, HAProxy, NGINX Ingress, PostgreSQL HA
- **Monitoring**: Prometheus & Grafana
- **Databases**: PostgreSQL (Relational), Elasticsearch (Logs), Vector Database (AI Context)

## Core Modules

### 1. Advanced SIEM & SIEM Engine
- **Real-time Log Ingestion**: High-throughput ingestion via Kafka.
- **ECS Normalization**: Maps raw logs to Elastic Common Schema.
- **Correlation Engine**: Supports temporal correlation (X events in Y time).
- **MITRE ATT&CK Mapping**: Automatic enrichment of alerts with Tactic/Technique IDs.
- **Custom Rule Engine**: Flexible YAML-based detection rules.

### 2. Enterprise SOAR Engine
- **Visual Playbook Executor**: DAG-based workflow execution.
- **Human Approval Gates**: Suspension of sensitive workflows pending manual authorization.
- **Workflow Versioning**: Track and manage multiple versions of playbooks.
- **Automated Actions**: IP blocking, User isolation, Token revocation, ServiceNow integration.

### 3. AI Security Assistant (RAG)
- **RAG Architecture**: Context-aware analysis using a vector database.
- **Threat Hunting Agent**: Autonomous investigation of security incidents.
- **Multi-LLM Support**: Integration with OpenAI and local Ollama.
- **Incident Summarization**: Automated root-cause analysis and reporting.

### 4. SOC & Case Management
- **Lifecycle Tracking**: End-to-end incident management from detection to resolution.
- **SLA & Escalations**: Automated tracking of response times and escalation policies.
- **Remediation Workflows**: Self-healing infrastructure and automated patching.

### 5. Asset Management (CMDB) & Threat Intel
- **Asset Inventory**: Comprehensive tracking of servers, cloud resources, and endpoints.
- **Vulnerability Management**: Integration with scanners (Nessus, OpenVAS).
- **Threat Intel Feeds**: Enrichment from MISP, OpenCTI, OTX, VirusTotal, and AbuseIPDB.

## Deployment Guide
Refer to `infrastructure/helm/` for production-ready Kubernetes deployment.
Use `infrastructure/docker/docker-compose.yml` for development and testing.
