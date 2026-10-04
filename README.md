🔐 Secure File Transfer System — DevSecOps
A secure Flask file-transfer application extended into an end-to-end DevOps/DevSecOps workflow.
BTech DevOps CA | TH1

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20App-000000?logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-Orchestrated-326CE5?logo=kubernetes&logoColor=white" alt="Kubernetes">
  <img src="https://img.shields.io/badge/Ansible-IaC%20%2F%20Config%20Management-EE0000?logo=ansible&logoColor=white" alt="Ansible">
  <img src="https://img.shields.io/badge/Prometheus-Monitoring-E6522C?logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-Dashboard-F46800?logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=githubactions&logoColor=white" alt="GitHub Actions">
</p>

👥 Authors
#	Name	Student ID
1	Mithlesh Yadav	23070122265
2	Velagala Prapul Krishna Reddy	23070122232
3	Rishi Modi	23070122180


🎯 Project at a Glance
Application: Secure file transfer using hybrid cryptography
Backend: Flask + Gunicorn
Encryption: AES-256-EAX + RSA-2048-OAEP
Delivery: GitHub Actions → Docker → Kubernetes
Configuration: Ansible + systemd
Observability: Prometheus + Grafana
Security: Non-root containers + capability restrictions + dependency/image scanning
Why this project?
The original file-transfer application is combined with DevOps practices so that the software can be tested, secured, packaged, deployed, updated, rolled back, and monitored through a repeatable workflow.
🏗️ Architecture
```mermaid
flowchart LR
    A[Developer] --> B[GitHub]
    B --> C[GitHub Actions]
    C --> D[Tests + Security Scan]
    C --> E[Docker Build]
    E --> F[Kubernetes]
    G[Ansible] --> F
    F --> H[Secure File Transfer App]
    H --> I[/metrics]
    I --> J[Prometheus]
    J --> K[Grafana]
```
🚀 DevOps CA — Phase Summary
Phase	Requirement	Implementation	Status
1	Deployment Strategy / CI-CD	GitHub Actions	✅
2	Configuration Management / IaC	Ansible + systemd	✅
3	Containerization / Orchestration	Docker + Kubernetes	✅
4	Monitoring / Logging	Prometheus + Grafana	✅
5	Reflection / Report	Architecture, results, challenges & lessons	✅
6	External Challenge / Bonus	Optional; requires genuine submission proof	⭕


1️⃣ Phase 1 — CI/CD with GitHub Actions
What we implemented
The workflow in .github/workflows/ci-cd.yml automates the delivery lifecycle:
Push / Pull Request
        ↓
Checkout source
        ↓
Install dependencies
        ↓
Run pytest
        ↓
Dependency security check
        ↓
Build Docker image
        ↓
Container security scan
        ↓
Publish / deploy workflow stages
        ↓
Kubernetes smoke tests
Key DevSecOps controls
- Automated unit/integration testing
- Dependency vulnerability checking
- Docker image vulnerability scanning
- Reproducible Docker builds
- Kubernetes deployment verification
- Smoke tests for /api/version and /metrics
File: .github/workflows/ci-cd.yml
2️⃣ Phase 2 — Configuration Management with Ansible
Ansible provisions the application runtime consistently instead of relying on manual server configuration.
Automated configuration
- Installs Python runtime packages
- Creates dedicated sftapp user/group
- Creates /opt/secure-file-transfer
- Creates an isolated Python virtual environment
- Copies application files and requirements
- Creates and configures a systemd service
- Enables and starts Gunicorn
- Performs a health check on /api/version
Service hardening
The systemd unit applies controls such as:
- NoNewPrivileges=true
- PrivateTmp=true
- ProtectHome=true
- ProtectSystem=strict
- restricted write paths
- dedicated non-login application user
Files:
ansible/inventory
ansible/setup.yml
ansible/files/secure-file-transfer.service
3️⃣ Phase 3 — Docker + Kubernetes
Docker
The final Dockerfile uses a multi-stage build:
Builder stage
    ↓
Install Python dependencies
    ↓
Minimal runtime stage
    ↓
Security updates
    ↓
Non-root appuser
    ↓
Gunicorn
This keeps build dependencies out of the runtime image and reduces unnecessary packages.
File: Dockerfile
Kubernetes
The application is deployed with:
- Deployment
- Service
- readiness probe
- liveness probe
- resource requests/limits
- non-root security context
- dropped Linux capabilities
- rolling-update strategy
Files:
k8s/deployment.yaml
k8s/service.yaml
Rolling update + rollback evidence
The deployment was tested with two application versions:
v1 → v2  ✅ Rolling update
v2 → v1  ✅ Rollback
Verification was performed through /api/version, confirming the application returned to 1.0.0 after rollback.
Architecture note: the current application keeps transfer state in memory. For that reason, the CA demonstration keeps the deployment at 1 replica. A production multi-replica version would move shared state/storage outside the application process.

4️⃣ Phase 4 — Monitoring with Prometheus + Grafana
The Flask application exposes a Prometheus endpoint:
GET /metrics
Prometheus scrapes:
http://sft-app:5000/metrics
with a 5-second scrape interval.
Dashboard metrics
Metric	Purpose
Application Uptime	Service availability/runtime
Request Rate	Requests per second
Average Latency	Response performance
Error Rate	Failed request percentage


Configuration:
monitoring/prometheus.yml
monitoring/grafana/provisioning/
monitoring/grafana/dashboards/secure-file-transfer.json
Monitoring stack
Secure File Transfer App
          ↓
       /metrics
          ↓
      Prometheus
          ↓
       Grafana
5️⃣ Phase 5 — Testing & Validation
Application tests
The project includes automated tests under tests/ covering:
- receiver/sender pages
- version endpoint
- RSA key generation
- secure end-to-end transfer
- invalid transfer handling
Run:
python -m pytest -v
Baseline validation completed with 7 tests passing.
Kubernetes validation
Useful checks:
kubectl get deployment
kubectl get pods
kubectl get service
kubectl rollout status deployment/secure-file-transfer
Monitoring validation
curl http://localhost:<prometheus-port>/-/ready
curl http://localhost:<prometheus-port>/api/v1/targets
The configured Secure File Transfer Prometheus target was verified with health up.
🔐 Security
Application security
- AES-256-EAX authenticated encryption
- RSA-2048-OAEP key protection
- PyCryptodome cryptographic implementation
Container / runtime security
- Non-root container user
- Dropped Linux capabilities in Kubernetes
- Privilege escalation disabled
- Hardened systemd service
- Minimal runtime image
DevSecOps security
Security checks are integrated into the delivery workflow using dependency and container scanning stages.
📁 Repository Structure
SecureFileTransfer-DevSecOps/
│
├── .github/workflows/ci-cd.yml
├── ansible/
│   ├── files/secure-file-transfer.service
│   ├── inventory
│   └── setup.yml
├── core/
│   ├── crypto.py
│   ├── keygen.py
│   ├── logger.py
│   └── network.py
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
├── tests/
│   └── test_application.py
├── web/
│   ├── app.py
│   └── templates/
├── Dockerfile
├── docker-compose.monitoring.yml
├── main.py
├── requirements.txt
└── README.md
⚙️ Quick Start
1. Clone
git clone https://github.com/MITHLESH55/SecureFileTransfer-DevSecOps.git
cd SecureFileTransfer-DevSecOps
2. Run locally
python -m venv venv
Windows:
venv\Scripts\Activate.ps1
Linux/macOS:
source venv/bin/activate
Install dependencies:
pip install -r requirements.txt
Run:
python main.py
3. Run tests
python -m pytest -v
4. Build Docker image
docker build -t secure-file-transfer:v1 .
5. Run Docker
docker run --rm -p 5000:5000 secure-file-transfer:v1
☸️ Kubernetes Quick Commands
Start Minikube:
minikube start --driver=docker
Load a local image:
minikube image load secure-file-transfer:v1
Deploy:
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/secure-file-transfer
Port-forward:
kubectl port-forward service/secure-file-transfer 5005:5000
Test:
http://localhost:5005/api/version
📊 Monitoring Quick Start
Start the monitoring stack:
docker compose -f docker-compose.monitoring.yml up -d
Typical local mappings in this setup:
Service	Host URL
Secure File Transfer	http://localhost:5003
Prometheus	http://localhost:9091
Grafana	http://localhost:3001


Open Grafana and select:
Secure File Transfer - DevOps Monitoring
🧪 Useful DevOps Commands
# Git
 git status
 git log --oneline -5

# Docker
docker images secure-file-transfer
docker ps

docker scout cves secure-file-transfer:v1

# Ansible
ansible-playbook -i ansible/inventory ansible/setup.yml

# Kubernetes
kubectl get deployments
kubectl get pods
kubectl get svc
kubectl rollout history deployment/secure-file-transfer
kubectl rollout undo deployment/secure-file-transfer

# Monitoring
docker compose -f docker-compose.monitoring.yml ps
🛠️ Challenges & Solutions
Challenge	Solution
Docker host-port conflicts	Used available host mappings while keeping container ports unchanged
Docker image vulnerabilities	Hardened the runtime image and added scanning to CI
Kubernetes cluster unavailable	Switched from failed Docker Desktop Kubernetes startup to the existing Minikube Docker driver
Rolling-update rollback consistency	Updated image and APP_VERSION together in one Deployment revision
Monitoring connectivity	Used the Docker Compose network target sft-app:5000
Stateful application design	Kept Kubernetes replicas at 1 for the current in-memory transfer state


💡 Lessons Learned
- CI/CD makes testing and delivery repeatable.
- Ansible reduces configuration drift.
- Docker gives a consistent runtime.
- Kubernetes provides controlled deployment and rollback.
- Prometheus + Grafana make application behavior observable.
- DevSecOps works best when security checks happen before deployment, not after it.
🔮 Future Enhancements
- External shared storage/database for transfer state
- Multi-replica high-availability deployment
- TLS/HTTPS with certificate management
- Kubernetes Ingress
- Secret management using Kubernetes Secrets or Vault
- Persistent audit logging
- Centralized logs with Loki/ELK
- Production cloud deployment
📌 Academic Submission Mapping
CA Requirement	Repository Evidence
Deployment strategy	.github/workflows/ci-cd.yml
Configuration management	ansible/setup.yml, ansible/inventory
Service configuration	ansible/files/secure-file-transfer.service
Dockerization	Dockerfile
Kubernetes deployment	k8s/deployment.yaml
Kubernetes service	k8s/service.yaml
Rolling update	Kubernetes rollout history / v2 verification
Rollback	kubectl rollout undo + v1 verification
Metrics	/metrics endpoint
Prometheus	monitoring/prometheus.yml
Grafana	monitoring/grafana/
Tests	tests/test_application.py
Documentation	README.md


🏁 Final Result
This project demonstrates a complete DevSecOps lifecycle:
Secure Application
       ↓
Automated Testing
       ↓
Security Validation
       ↓
Containerization
       ↓
Configuration Management
       ↓
Kubernetes Deployment
       ↓
Rolling Update / Rollback
       ↓
Prometheus Monitoring
       ↓
Grafana Visualization
Outcome: the Secure File Transfer application is packaged and documented as a repeatable DevOps workflow instead of a manually deployed standalone application.

📎 Repository
GitHub: https://github.com/MITHLESH55/SecureFileTransfer-DevSecOps
<p align="center">
  <b>Secure File Transfer System • DevOps / DevSecOps CA</b><br>
  Built with Python, Docker, Kubernetes, Ansible, GitHub Actions, Promet
