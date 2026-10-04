Secure File Transfer System — DevSecOps
A secure web-based file transfer application implemented with hybrid cryptography and extended into a complete DevOps/DevSecOps workflow covering automated CI/CD, configuration management, containerization, Kubernetes orchestration, security scanning, monitoring, logging/metrics, testing, and rollback.
Project focus: Secure application delivery from source code to a reproducible runtime, with automated validation and operational observability.

Table of Contents
- 1. Project Overview
- 2. Problem Statement
- 3. Objectives
- 4. How the Application Works
- 5. Security Model
- 6. Technology Stack
- 7. DevSecOps Architecture
- 8. Project Structure
- 9. DevOps CA Phases
  - Phase 0 — Application Baseline
  - Phase 1 — Deployment Strategy and CI/CD
  - Phase 2 — Configuration Management and IaC
  - Phase 3 — Containerization and Kubernetes Orchestration
  - Phase 4 — Monitoring and Observability
  - Phase 5 — Testing, Validation and Evidence
  - Phase 6 — External DevOps Challenge / Bonus
- 10. CI/CD Pipeline Flow
- 11. Docker Implementation
- 12. Ansible Configuration Management
- 13. Kubernetes Deployment
- 14. Rolling Update and Rollback
- 15. Prometheus Monitoring
- 16. Grafana Dashboard
- 17. Security and DevSecOps Controls
- 18. Testing
- 19. Local Setup
- 20. Useful Commands
- 21. Troubleshooting
- 22. Results and Validation
- 23. Challenges and Solutions
- 24. Lessons Learned
- 25. Future Enhancements
- 26. Academic Submission Evidence
- 27. Author
1. Project Overview
The Secure File Transfer System is a Flask-based web application for transferring files securely between sender and receiver endpoints.
The application combines:
- AES-256-EAX for efficient authenticated encryption of file contents.
- RSA-2048-OAEP for securely protecting the AES session key.
- Flask + Gunicorn for the web application runtime.
- PyCryptodome for cryptographic operations.
- Prometheus client instrumentation for application metrics.
- Docker for reproducible packaging.
- Ansible for configuration management and system provisioning.
- Kubernetes for deployment, rolling updates, and rollback.
- GitHub Actions for automated CI/CD.
- Trivy/pip-audit style security checks in the delivery workflow.
- Prometheus + Grafana for monitoring and visualization.
The DevOps extension transforms the original application into a repeatable delivery pipeline where code quality, security, deployment, and observability are treated as part of the same lifecycle.
2. Problem Statement
Traditional file-transfer applications can suffer from:
- insecure transport or storage of file contents,
- weak key management,
- manual application deployment,
- inconsistent server configuration,
- difficult rollback procedures,
- lack of operational visibility,
- and vulnerabilities being discovered only after deployment.
This project addresses these concerns by combining application-level cryptography with a DevSecOps delivery workflow.
3. Objectives
The main objectives are to:
1. Build a secure file-transfer service using hybrid cryptography.
2. Automate testing and application validation.
3. Package the application as a secure container image.
4. Provision/configure a runtime using Ansible.
5. Deploy the container with Kubernetes.
6. Demonstrate a Kubernetes rolling update and rollback.
7. Expose application metrics for Prometheus scraping.
8. Visualize availability, traffic, latency, and errors in Grafana.
9. Integrate security checks into the CI/CD lifecycle.
10. Document the complete process as a reproducible DevOps workflow.
4. How the Application Works
4.1 Sender Flow
1. A sender opens the sender interface.
2. The application accepts the file to be transferred.
3. A random AES-256 session key is generated.
4. The file is encrypted using AES-256 in EAX mode.
5. The AES key is encrypted using the receiver's RSA-2048 public key with OAEP padding.
6. The encrypted payload and metadata are associated with a transfer ID.
7. The receiver can retrieve and decrypt the file using the corresponding RSA private key.
4.2 Receiver Flow
1. The receiver generates/uses an RSA key pair.
2. The receiver exposes the public key for the sender workflow.
3. The sender encrypts the file with AES-256.
4. The sender encrypts the AES key with the RSA public key.
5. The receiver uses the RSA private key to recover the AES session key.
6. The receiver authenticates/decrypts the file contents.
7. The transfer is recorded in the application state/audit flow.
5. Security Model
The project uses hybrid cryptography because symmetric encryption is efficient for file contents while asymmetric cryptography is useful for secure key exchange.
AES-256-EAX
- Encrypts the file data efficiently.
- Provides authenticated encryption.
- Protects confidentiality and integrity of the encrypted payload.
RSA-2048-OAEP
- Protects the AES session key.
- OAEP provides secure RSA encryption padding.
- The receiver's private key is required to recover the AES key.
Additional application controls
- Maximum transfer size is limited by the application.
- File workspaces are isolated from source-code locations.
- The container runs as a non-root user.
- Linux capabilities are dropped in the Kubernetes security context.
- Privilege escalation is disabled.
- The Ansible-managed systemd service includes additional hardening directives.
- Security scanning is incorporated into the CI/CD pipeline.
6. Technology Stack
Area	Technology
Language	Python 3.12
Web Framework	Flask
Production Server	Gunicorn
Cryptography	PyCryptodome
Application Metrics	prometheus-client
Testing	pytest
Dependency Security	pip-audit / workflow security checks
Containerization	Docker
Image Security	Docker Scout / Trivy workflow integration
Configuration Management	Ansible
Service Management	systemd + Gunicorn
Orchestration	Kubernetes
Local Kubernetes	Minikube with Docker driver
Monitoring	Prometheus
Visualization	Grafana
CI/CD	GitHub Actions
Source Control	Git + GitHub


7. DevSecOps Architecture
                           +----------------------+
                           |      Developer       |
                           |  Git / GitHub Push   |
                           +----------+-----------+
                                      |
                                      v
                         +-------------------------+
                         |     GitHub Actions      |
                         |-------------------------|
                         | Checkout                |
                         | Install dependencies    |
                         | Run pytest              |
                         | pip-audit/security     |
                         | Build Docker image      |
                         | Trivy scan             |
                         | Publish image (GHCR)   |
                         | Kubernetes smoke test  |
                         +-----------+-------------+
                                     |
                    +----------------+----------------+
                    |                                 |
                    v                                 v
          +------------------+              +---------------------+
          |      Docker      |              |     Ansible        |
          | Secure container |              | Runtime provisioning|
          +--------+---------+              +----------+----------+
                   |                                   |
                   v                                   v
          +--------------------------------------------------+
          |                    Kubernetes                     |
          |--------------------------------------------------|
          | Deployment: secure-file-transfer                  |
          | Service: NodePort                                |
          | Readiness / Liveness probes                       |
          | RollingUpdate strategy                            |
          | Rollback / revision history                       |
          +------------------------+-------------------------+
                                   |
                                   v
                         +---------------------+
                         | Secure File Transfer|
                         | Flask + Gunicorn    |
                         +----------+----------+
                                    |
                                    | /metrics
                                    v
                         +---------------------+
                         |     Prometheus       |
                         | 5 second scrape      |
                         +----------+----------+
                                    |
                                    v
                         +---------------------+
                         |       Grafana        |
                         | Uptime / Rate /      |
                         | Latency / Errors     |
                         +---------------------+
8. Project Structure
SecureFileTransfer-DevSecOps/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── ansible/
│   ├── files/
│   │   └── secure-file-transfer.service
│   ├── inventory
│   └── setup.yml
│
├── core/
│   ├── __init__.py
│   ├── crypto.py
│   ├── keygen.py
│   ├── logger.py
│   └── network.py
│
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│       ├── dashboards/
│       │   └── secure-file-transfer.json
│       └── provisioning/
│           ├── dashboards/
│           │   └── dashboard.yml
│           └── datasources/
│               └── prometheus.yml
│
├── tests/
│   └── test_application.py
│
├── web/
│   ├── app.py
│   └── templates/
│       ├── index.html
│       ├── receiver.html
│       └── sender.html
│
├── .dockerignore
├── .gitignore
├── docker-compose.monitoring.yml
├── Dockerfile
├── main.py
├── requirements.txt
├── requirements-dev.txt
├── run_ngrok.py
└── README.md
9. DevOps CA Phases
Phase 0 — Application Baseline
Before adding DevOps automation, the application was verified locally.
Baseline validation included:
- Flask application startup.
- Sender and receiver pages.
- RSA key generation.
- End-to-end secure transfer.
- Version endpoint.
- Invalid transfer handling.
- Prometheus /metrics endpoint.
The application test suite was executed with pytest and the baseline suite passed successfully.
Phase 1 — Deployment Strategy and CI/CD
Tool Selected
GitHub Actions was selected as the deployment automation platform.
The workflow is located at:
.github/workflows/ci-cd.yml
Pipeline responsibilities
The workflow is designed to:
1. Check out the repository.
2. Install the required Python version.
3. Install runtime and development dependencies.
4. Execute automated tests.
5. Run dependency/security checks.
6. Build the Docker image.
7. Run container security scanning.
8. Publish the image to GitHub Container Registry when configured.
9. Create a local Kubernetes test environment in the CI runner.
10. Deploy the application to Kubernetes.
11. Wait for rollout completion.
12. Perform smoke tests against /api/version and /metrics.
CI/CD flow
Git Push / Pull Request
        |
        v
   GitHub Actions
        |
        +--> Install dependencies
        |
        +--> pytest
        |
        +--> Security / dependency audit
        |
        +--> Docker build
        |
        +--> Trivy HIGH/CRITICAL scan
        |
        +--> Publish image
        |
        +--> Kubernetes deployment
        |
        +--> Rollout verification
        |
        +--> Smoke tests
Why CI/CD is important
The pipeline reduces manual errors, catches test/security failures before deployment, and makes the application's delivery process repeatable.
Phase 2 — Configuration Management and IaC
Tool Selected
Ansible was used for configuration management and repeatable runtime provisioning.
Files:
ansible/inventory
ansible/setup.yml
ansible/files/secure-file-transfer.service
Ansible responsibilities
The playbook configures:
- required OS packages,
- a dedicated sftapp service user/group,
- /opt/secure-file-transfer application directory,
- application workspace,
- Python virtual environment,
- Python dependencies,
- application source files,
- file ownership and permissions,
- systemd service configuration,
- service enablement and startup,
- application health validation.
Runtime configuration
The service runs using Gunicorn through systemd and binds to a local application port.
The systemd unit also applies security-oriented controls such as:
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
RestrictSUIDSGID=true
CapabilityBoundingSet=
UMask=0027
Validation
The Ansible playbook was syntax-checked and executed successfully with the local host inventory. The resulting systemd service was confirmed enabled/active, and /api/version returned HTTP 200.
Phase 3 — Containerization and Kubernetes Orchestration
Docker
The application was packaged using a multi-stage Docker build.
Key properties:
- Python 3.12 slim base image.
- Separate dependency-builder stage.
- Minimal runtime stage.
- Runtime package upgrade for current Debian security fixes available at build time.
- No unnecessary build tools copied into the final stage.
- Non-root appuser runtime.
- Restricted writable workspace.
- Gunicorn production server.
- Port 5000 exposed inside the container.
Kubernetes
Two primary manifests are provided:
k8s/deployment.yaml
k8s/service.yaml
The Deployment provides:
- 1 replica for the current application architecture,
- RollingUpdate strategy,
- maxUnavailable: 0,
- maxSurge: 1,
- readiness probe,
- liveness probe,
- CPU/memory requests and limits,
- non-root execution,
- disabled privilege escalation,
- dropped Linux capabilities.
The Service exposes the application through a Kubernetes NodePort.
Important architecture note
The current application keeps transfer state/audit state in process memory. Because of that limitation, the Kubernetes deployment uses one replica for predictable behavior. A future production architecture should externalize state to a shared database/object store before horizontally scaling the application.
Phase 4 — Monitoring and Observability
Prometheus
The application exposes:
/metrics
Prometheus configuration:
monitoring/prometheus.yml
Current scrape configuration:
global:
  scrape_interval: 5s
  evaluation_interval: 5s

scrape_configs:
  - job_name: secure-file-transfer
    metrics_path: /metrics
    static_configs:
      - targets:
          - "sft-app:5000"
The verified Prometheus target was:
http://sft-app:5000/metrics
health: up
scrape interval: 5s
Grafana
The dashboard is provisioned from:
monitoring/grafana/dashboards/secure-file-transfer.json
The dashboard tracks the four main CA metrics:
Application Uptime
sft_uptime_seconds
Request Rate
sum(rate(sft_http_requests_total[1m]))
Average Latency
1000 * sum(rate(sft_http_request_duration_seconds_sum[1m]))
/
sum(rate(sft_http_request_duration_seconds_count[1m]))
Error Rate
100 * sum(rate(sft_http_errors_total[1m]))
/
sum(rate(sft_http_requests_total[1m]))
The dashboard is configured for rapid refresh and a recent time window so application traffic can be observed during testing.
Phase 5 — Testing, Validation and Evidence
Testing was performed at multiple layers.
Application tests
Run:
python -m pytest -v
The existing suite covers scenarios including:
- home page redirect,
- sender page availability,
- receiver page availability,
- version endpoint,
- RSA key generation,
- end-to-end secure transfer,
- invalid transfer ID rejection.
Docker validation
The container was built and run locally, and the following were verified:
/api/version  -> HTTP 200
/metrics      -> HTTP 200
Kubernetes validation
Validated operations include:
Deployment
Service
Pod readiness
Rolling update
Rollout status
Rollout history
Rollback
Application API verification
Monitoring validation
Prometheus was verified using its readiness endpoint and target API. The application target was reported as health: up with no scrape error.
Phase 6 — External DevOps Challenge / Bonus
The academic task optionally allows participation in an external DevOps challenge such as a Kaggle, Devpost, cloud, or similar competition.
This section should contain only genuine evidence after a real submission.
Recommended evidence to add here when applicable:
- challenge name,
- official challenge link,
- submission timestamp,
- submission/leaderboard screenshot,
- repository link or PR link,
- participation badge, if issued.
Do not claim participation, ranking, or a submission unless the corresponding evidence exists.

10. CI/CD Pipeline Flow
The complete intended delivery flow is:
Developer
   |
   | git push / pull request
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +----> Automated tests
   |
   +----> Dependency/security audit
   |
   +----> Docker build
   |
   +----> Trivy security scan
   |
   +----> Image publication
   |
   +----> Kubernetes deployment
   |
   +----> Rollout status check
   |
   +----> Smoke tests
   |
   v
Running Application
   |
   +----> Prometheus metrics
   |
   v
Grafana dashboard
11. Docker Implementation
Build the image
docker build --build-arg APP_VERSION=1.0.0 -t secure-file-transfer:v1 .
Build a second version for rolling-update demonstration:
docker build --build-arg APP_VERSION=2.0.0 -t secure-file-transfer:v2 .
List images:
docker images secure-file-transfer
Run locally
docker run -d \
  --name sft-local \
  -p 5001:5000 \
  secure-file-transfer:v1
Test:
curl http://localhost:5001/api/version
12. Ansible Configuration Management
Inventory
The current inventory uses the local machine for demonstration:
[secure_file_transfer]
localhost ansible_connection=local ansible_python_interpreter=/usr/bin/python3 ansible_become_method=sudo
Syntax check
ansible-playbook -i ansible/inventory ansible/setup.yml --syntax-check
Execute the playbook
ansible-playbook -i ansible/inventory ansible/setup.yml -K
Validate the service
systemctl is-enabled secure-file-transfer
systemctl is-active secure-file-transfer
curl http://127.0.0.1:5002/api/version
13. Kubernetes Deployment
Start Minikube
minikube start --driver=docker
Verify:
kubectl get nodes
Expected node status:
Ready
Load local images
minikube image load secure-file-transfer:v1
minikube image load secure-file-transfer:v2
Verify:
minikube image ls | grep secure-file-transfer
Validate manifests
kubectl apply --dry-run=client -f k8s/deployment.yaml
kubectl apply --dry-run=client -f k8s/service.yaml
Deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl rollout status deployment/secure-file-transfer
Check:
kubectl get deployment
kubectl get pods -l app=secure-file-transfer
kubectl get service secure-file-transfer
Access the application
kubectl port-forward service/secure-file-transfer 5005:5000
Then:
http://localhost:5005
API verification:
curl http://localhost:5005/api/version
14. Rolling Update and Rollback
14.1 Verify v1
The initial deployment was validated with:
Image: secure-file-transfer:v1
APP_VERSION: 1.0.0
The API returned:
{"application":"Secure File Transfer System","status":"running","version":"1.0.0"}
14.2 Update to v2
A strategic patch can update both image and application version as a single pod-template change:
{
  "spec": {
    "template": {
      "spec": {
        "containers": [
          {
            "name": "secure-file-transfer",
            "image": "secure-file-transfer:v2",
            "env": [
              {
                "name": "APP_VERSION",
                "value": "2.0.0"
              }
            ]
          }
        ]
      }
    }
  }
}
Apply:
kubectl patch deployment secure-file-transfer --type=strategic --patch-file patch.json
kubectl rollout status deployment/secure-file-transfer
Verify:
kubectl get deployment secure-file-transfer -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl get deployment secure-file-transfer -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="APP_VERSION")].value}'
curl http://localhost:5005/api/version
Expected application version:
2.0.0
14.3 Rollback
kubectl rollout undo deployment/secure-file-transfer
kubectl rollout status deployment/secure-file-transfer
Verify:
kubectl get deployment secure-file-transfer -o jsonpath='{.spec.template.spec.containers[0].image}'
kubectl get deployment secure-file-transfer -o jsonpath='{.spec.template.spec.containers[0].env[?(@.name=="APP_VERSION")].value}'
curl http://localhost:5005/api/version
Expected final version:
secure-file-transfer:v1
1.0.0
14.4 Rollout evidence
Useful commands:
kubectl rollout history deployment/secure-file-transfer
kubectl get rs -l app=secure-file-transfer
kubectl get pods -l app=secure-file-transfer -o wide
This demonstrates that Kubernetes created and switched between ReplicaSets during the update and rollback process.
15. Prometheus Monitoring
Monitoring stack
The project includes a Docker Compose monitoring stack:
docker-compose.monitoring.yml
Start it with:
docker compose -f docker-compose.monitoring.yml up -d
Check containers:
docker ps
The local demonstration used host ports that avoid collisions with other services:
Secure File Transfer app : 5003
Prometheus               : 9091
Grafana                  : 3001
Prometheus health check
curl http://localhost:9091/-/ready
Expected:
Prometheus Server is Ready.
Prometheus target check
curl http://localhost:9091/api/v1/targets
The verified target was:
sft-app:5000/metrics
health: up
lastError: ""
Generate application traffic
Successful requests:
1..50 | ForEach-Object {
    Invoke-WebRequest -UseBasicParsing http://localhost:5003/api/version | Out-Null
}
Generate a few error responses to make the error-rate panel observable:
1..10 | ForEach-Object {
    try {
        Invoke-WebRequest -UseBasicParsing http://localhost:5003/not-found | Out-Null
    } catch {}
}
16. Grafana Dashboard
Open:
http://localhost:3001
Dashboard:
Secure File Transfer - DevOps Monitoring
The dashboard provides:
1. Application Uptime
Shows application uptime in seconds.
2. Request Rate
Shows current request throughput.
3. Average Latency
Shows average HTTP request latency in milliseconds.
4. Error Rate
Shows failed request percentage.
These panels provide a basic but meaningful operational view of the application and satisfy the core monitoring requirement.
17. Security and DevSecOps Controls
Security is integrated across multiple layers instead of being treated as a final-stage activity.
Application security
- AES-256-EAX authenticated encryption.
- RSA-2048-OAEP key protection.
- File-size limiting.
- Transfer ID validation.
- Application-level audit/logging support.
Container security
- Multi-stage build.
- Slim runtime base image.
- Non-root runtime user.
- Runtime package security updates.
- No unnecessary build-stage content in final image.
Kubernetes security
runAsNonRoot: true
allowPrivilegeEscalation: false
capabilities:
  drop:
    - ALL
Host/service security
Ansible/systemd configuration includes:
NoNewPrivileges
PrivateTmp
ProtectHome
ProtectSystem
RestrictSUIDSGID
CapabilityBoundingSet
UMask
CI/CD security
The CI/CD workflow integrates:
- dependency/security auditing,
- container image scanning,
- blocking of fixable HIGH/CRITICAL vulnerabilities,
- controlled image publication,
- deployment verification.
Security scanning result
During local hardening, the Docker image reached a state where the Docker Scout policy for fixable critical/high vulnerabilities passed. Remaining high-severity findings were associated with vulnerabilities for which an updated fixed package was not yet available to the image at the time of testing.
The project does not disable the security scan to hide findings.
18. Testing
Run all tests
python -m pytest -v
Expected baseline suite
The project currently contains tests covering:
Home route behavior
Sender page
Receiver page
Version endpoint
RSA key generation
End-to-end secure transfer
Invalid transfer ID handling
Compile validation
The CI workflow also performs Python compilation checks on the main application modules before producing a build artifact.
19. Local Setup
Prerequisites
Install/configure:
- Git
- Python 3.12+
- Docker Desktop
- Docker Compose
- kubectl
- Minikube
- Ansible (Linux/WSL recommended for the Ansible phase)
- GitHub account for Actions/Container Registry functionality
Clone
git clone https://github.com/MITHLESH55/SecureFileTransfer-DevSecOps.git
cd SecureFileTransfer-DevSecOps
Python environment
Windows PowerShell:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Linux/WSL:
python3 -m venv .venv
source .venv/bin/activate
Install dependencies
Runtime:
pip install -r requirements.txt
Development/testing:
pip install -r requirements-dev.txt
Run application directly
python main.py
For production-style local execution, use Gunicorn as defined by the project/container configuration.
20. Useful Commands
Git
git status
git branch
git log --oneline --decorate -10
git pull
git push
Docker
docker build -t secure-file-transfer:v1 .
docker images secure-file-transfer
docker ps
docker logs <container>
docker rm -f <container>
Docker Compose monitoring
docker compose -f docker-compose.monitoring.yml up -d
docker compose -f docker-compose.monitoring.yml ps
docker compose -f docker-compose.monitoring.yml logs -f
Kubernetes
kubectl get nodes
kubectl get pods
kubectl get deployments
kubectl get services
kubectl rollout status deployment/secure-file-transfer
kubectl rollout history deployment/secure-file-transfer
kubectl rollout undo deployment/secure-file-transfer
Minikube
minikube status
minikube start --driver=docker
minikube stop
minikube image load secure-file-transfer:v1
Ansible
ansible --version
ansible all -i ansible/inventory -m ping
ansible-playbook -i ansible/inventory ansible/setup.yml --syntax-check
ansible-playbook -i ansible/inventory ansible/setup.yml -K
21. Troubleshooting
Port 5000 is already in use
Use another host port:
docker run -p 5001:5000 secure-file-transfer:v1
The Docker Compose monitoring stack also uses a non-default host mapping to avoid collisions.
Port 5005 is already in use
A previous Kubernetes port-forward may still be running. Reuse that terminal/session or identify the process using port 5005 before starting another forwarding command.
Docker Compose reports container-name conflicts
Remove the stale project containers and recreate the stack:
docker rm -f sft-app sft-prometheus sft-grafana
docker compose -f docker-compose.monitoring.yml up -d
Prometheus is not reachable on port 9090
Check the actual host mapping:
docker ps
The local demonstration used:
9091 -> 9090
so the browser/API endpoint is:
http://localhost:9091
Grafana is not reachable on port 3000
Check:
docker ps
The local demonstration used:
3001 -> 3000
so use:
http://localhost:3001
Minikube node is stopped
minikube start --driver=docker
kubectl get nodes
Kubernetes image cannot be pulled
Load local images into Minikube:
minikube image load secure-file-transfer:v1
minikube image load secure-file-transfer:v2
The Kubernetes Deployment is configured for local-image usage during the demonstration.
22. Results and Validation
The DevOps extension was validated across the major assignment requirements.
Application
- Secure file transfer workflow operates correctly.
- RSA key generation works.
- Version endpoint returns application status/version.
- Prometheus metrics endpoint is exposed.
Docker
- Multi-stage image builds successfully.
- Application starts with Gunicorn.
- Container runs as a non-root user.
- Security hardening reduced fixable vulnerability exposure.
Ansible
- Playbook syntax validated.
- Runtime user and directories created.
- Python environment provisioned.
- systemd service enabled/started.
- Application health check returned HTTP 200.
Kubernetes
- Minikube cluster became Ready.
- v1 image deployed.
- Service exposed application.
- v2 rolling update completed successfully.
- v2 application version was verified.
- Rollback completed successfully.
- v1 application version was verified after rollback.
Monitoring
- Prometheus became Ready.
- secure-file-transfer target reported health: up.
- Grafana dashboard was provisioned for uptime, request rate, latency, and error rate.
Repository
The completed work was committed and pushed to the project's GitHub repository.
23. Challenges and Solutions
Challenge 1 — Kubernetes cluster initialization
Docker Desktop's built-in Kubernetes cluster failed during kind/kubeadm initialization.
Solution
An existing Minikube installation was used with the Docker driver:
minikube start --driver=docker
This provided a working local Kubernetes environment without changing the application architecture.
Challenge 2 — Host port conflicts
Multiple local projects were already using common ports such as 5000, 9090, and 3000.
Solution
Non-conflicting host mappings were used:
Application   5003
Prometheus    9091
Grafana       3001
Kubernetes    5005 port-forward
Challenge 3 — Kubernetes rollback revision consistency
Changing the Deployment image and environment variable in separate commands can create multiple revisions and make rollback less predictable.
Solution
The demonstration updated the image and APP_VERSION together in one pod-template change so the rollback represented a coherent application version.
Challenge 4 — Container vulnerability hardening
The initial container image contained several security findings.
Solution
A multi-stage image and runtime package updates were introduced. The final local security policy check passed for fixable HIGH/CRITICAL findings while leaving the security scan enabled.
Challenge 5 — Application state and replicas
The current application stores transfer-related state in memory.
Solution
The demonstration kept the Deployment at one replica and documented the architectural limitation. Production horizontal scaling would require moving state to shared persistent storage.
24. Lessons Learned
1. Automation is only useful when it is repeatable. GitHub Actions, Ansible, Docker, and Kubernetes make the environment reproducible instead of relying on manual steps.
2. Security must be integrated early. Dependency and image scans are more effective when they run inside the delivery pipeline.
3. Deployment and rollback should be tested, not just documented. The project actually performed a v1 → v2 rolling update and a rollback to v1.
4. Observability is part of deployment quality. A deployment is more trustworthy when uptime, traffic, latency, errors, and application health can be observed.
5. Architecture affects orchestration choices. Kubernetes replica count cannot be selected independently of how application state is stored.
6. Local environments need deliberate resource and port management. Docker Desktop, Minikube, and existing projects may compete for the same local resources.
25. Future Enhancements
For a production-ready evolution, the following improvements are recommended:
- Move transfer metadata/state from in-memory dictionaries to PostgreSQL or Redis.
- Store encrypted files in durable object storage or a persistent volume.
- Add authentication and role-based authorization.
- Add TLS/HTTPS for client-to-service communication.
- Implement stronger secret management using Kubernetes Secrets or an external secret manager.
- Add centralized structured logging.
- Add alerting rules in Prometheus/Alertmanager.
- Add persistent Grafana/Prometheus storage.
- Add automated integration tests against the Kubernetes deployment.
- Publish signed container images with SBOM and provenance attestations.
- Use an ingress controller and TLS certificates instead of NodePort in a production deployment.
- Introduce horizontal scaling after state has been externalized.
26. Academic Submission Evidence
For the DevOps CA/PBL submission, the recommended evidence set is:
Step 1 — CI/CD
- .github/workflows/ci-cd.yml
- GitHub Actions workflow run screenshot
- Pipeline flow/architecture diagram
Step 2 — Ansible
- ansible/inventory
- ansible/setup.yml
- ansible/files/secure-file-transfer.service
- Playbook execution output
- systemctl is-active / health-check output
Step 3 — Docker + Kubernetes
- Dockerfile
- k8s/deployment.yaml
- k8s/service.yaml
- Kubernetes deployment screenshot
- v1 API response
- v2 rolling-update screenshot
- rollback screenshot
- kubectl rollout history output
Step 4 — Monitoring
- monitoring/prometheus.yml
- Prometheus target showing health: up
- Grafana dashboard screenshot with:
  - Application Uptime
  - Request Rate
  - Average Latency
  - Error Rate
Step 5 — Report
Prepare a 4–5 slide summary containing:
1. Architecture.
2. CI/CD pipeline flow.
3. Configuration management and Kubernetes deployment.
4. Challenges and solutions.
5. Results and lessons learned.
Step 6 — Bonus
Attach external challenge proof only when there is a genuine submission, badge, PR, leaderboard entry, or other verifiable evidence.
27. Authors
This project was collaboratively developed by the following team members:
1. Mithlesh Yadav — Roll No. 23070122265
   BTech Computer Science Engineering, Symbiosis Institute of Technology, Pune
2. Velagala Prapul Krishna Reddy — Roll No. 23070122232
3. Rishi Modi — Roll No. 23070122180
Project Repository
GitHub: MITHLESH55/SecureFileTransfer-DevSecOps
Final DevSecOps Summary
                        SECURE FILE TRANSFER
                                  |
          +-----------------------+------------------------+
          |                       |                        |
      Security                 DevOps                 Observability
          |                       |                        |
   AES-256-EAX             GitHub Actions            Prometheus
   RSA-2048-OAEP           Docker                    Grafana
   Non-root                 Ansible                  /metrics
   Security scan            Kubernetes               Uptime
   Hardened systemd        Rolling Update            Rate
                            Rollback                  Latency
                                                      Errors
Result: a secure application was extended into a structured DevSecOps delivery lifecycle with automated validation, configuration management, secure containerization, Kubernetes orchestration, rollback capability, and operational monitoring.
