# MODEL DEPLOYMENT, MONITORING & PRODUCTIONIZATION  
---

## Overview
This document describes the **end-to-end productionization of the Titanic Survival Prediction model**, focusing on deployment, monitoring, observability.

---

## Deployed Model Summary
- **Model Type:** XGBoost Classifier
- **Training Status:** Final tuned model
- **Inference Mode:** Real-time API-based predictions

The model deployed in this stage is the **same artifact validated during evaluation**, ensuring no training–serving skew.

---

## API-Based Model Serving (FastAPI)

### Framework Selection
The model was deployed using **FastAPI**, chosen for:
- High-performance request handling
- Native support for data validation
- Automatic API documentation (Swagger UI)
- Clean separation between logic and schema

This enables the model to be consumed by external systems without coupling inference logic to notebooks or scripts.

---

### API Endpoints Implemented

#### Health Check Endpoint
- **Route:** `/`
- **Purpose:** Confirms API availability and readiness
- **Use Case:** Monitoring, container checks, load balancers

#### Prediction Endpoint
- **Route:** `/predict`
- **Method:** POST
- **Purpose:** Generates survival predictions from structured passenger data

Each request is processed independently, ensuring stateless inference behavior.

---

## Input Schema Validation (Pydantic)

### Why Validation Matters
Incorrect inputs can silently degrade predictions or crash production systems. To prevent this, **strict schema validation** is enforced using Pydantic.

The input schema ensures:
- All required features are present
- Feature datatypes match model expectations
- Invalid requests fail early with explicit error messages

This protects the model from unpredictable user inputs and prevents inference-time failures.

---

## Prediction Flow & Request Lifecycle

Each `/predict` request follows a deterministic flow:

1. Incoming JSON is validated against the input schema
2. A **unique request ID** is generated for traceability
3. Input data is converted into a structured DataFrame
4. The model produces probability-based predictions
5. A final binary decision is derived
6. Results are returned as a structured response

This consistent pipeline ensures stable, explainable prediction behavior.

---

## Prediction Logging & Observability

To make predictions auditable and debuggable, **detailed logging was implemented** for every request.

Each log entry contains:
- Timestamp
- Request ID
- Model version
- Full input feature snapshot
- Prediction probability
- Final prediction output

### Why Logging Is Critical
Prediction logs enable:
- Post-deployment debugging
- Root cause analysis for incorrect predictions
- Model performance monitoring over time

Each prediction can be uniquely traced using its request ID, a core requirement for production ML systems.

---

## Post-Deployment Data Drift Monitoring

### Why Drift Detection Is Needed
Once deployed, real-world data may differ from training data. This phenomenon — **data drift** — can silently degrade model performance.

To detect drift early, a statistical monitoring pipeline was implemented.

---

### Drift Detection Strategy
- Training data distributions were compared against live input distributions
- Key numerical features were monitored
- Statistical testing was performed using the **Kolmogorov–Smirnov (KS) test**

Features monitored:
- Age
- Fare
- Passenger Class

For each feature:
- A p-value is calculated
- Drift is flagged when statistical significance is detected
- Results are stored in a structured JSON report

This enables proactive model health monitoring.

---

## Containerization with Docker

### Why Docker?
Docker ensures that the application:
- Runs consistently across environments
- Has isolated dependencies
- Can be deployed without manual setup
- Is cloud-ready

---

### Container Architecture
The Docker configuration:
- Uses a lightweight Python base image
- Installs only required dependencies
- Copies application source code
- Exposes the FastAPI service port
- Starts the API server using Uvicorn

Port mapping allows the API to be accessed from the host machine while running inside a container.

---

## Deployment Validation

The containerized application was validated by:
- Successfully starting the FastAPI service
- Accessing Swagger UI from the browser
- Sending prediction requests
- Verifying logs and drift reports

This confirms that the system is **deployment-ready**.

---

## Key Outcomes of Day 5

By the end of Day 5, the project achieved:

- A production-grade inference API
- Strict input validation
- Persistent prediction logging
- Automated data drift detection
- Docker-based deployment readiness

---

## Artifacts Generated
- `deployment/api.py`
- `prediction_logs.csv`
- `monitoring/drift_checker.py`
- `monitoring/drift_report.json`
- `Dockerfile`
- `requirement.txt`
- `.env.example`

