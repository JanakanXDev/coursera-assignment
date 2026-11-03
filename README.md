# OpenShift CI/CD Pipeline – Product Catalogue Application

## Project overview

This project implements a small but functional Flask product catalogue API designed for a Coursera final assignment. The application exposes a REST API for listing, retrieving, creating, updating, and deleting products, and is intended to run in an OpenShift container on port 8080.

## Objectives

- Build a Flask-based REST API with validation and appropriate HTTP status codes.
- Provide local unit testing and automated linting with Flake8 and Nose.
- Configure GitHub Actions to run CI checks on pushes and pull requests to the `main` branch.
- Define Tekton pipeline tasks and a Pipeline that clones, lints, tests, builds, and deploys the application.
- Create OpenShift manifests for a Deployment, Service, Route, PVC, and RBAC configuration.

## Technology stack

- Python 3.10
- Flask
- SQLite
- Nose
- Flake8
- Docker and Buildah
- GitHub Actions
- OpenShift Pipelines / Tekton

## Application features

The application includes the following endpoints:

- `GET /` – application metadata
- `GET /health` – health check endpoint
- `GET /api/products` – list all products
- `GET /api/products/<id>` – fetch a single product
- `POST /api/products` – create a product
- `PUT /api/products/<id>` – update a product
- `DELETE /api/products/<id>` – delete a product

The implementation uses a small SQLite-backed data store and validates invalid input to return correct HTTP status codes.

## Architecture and CI/CD workflow

The repository is organized into an application layer, tests, container definitions, CI workflow, and OpenShift Tekton resources.

The CI/CD flow is as follows:

1. GitHub Actions triggers on pushes, pull requests, or manual dispatch.
2. Dependencies are installed with `pip`.
3. Flake8 checks the application and tests.
4. Nose runs the unit tests.
5. Tekton tasks clean the workspace, clone the repository, lint, test, build with Buildah, and deploy the image.
6. OpenShift resources expose the application through a Kubernetes Service and an OpenShift Route.

## Repository directory structure

```text
coursera-assignment/
├── README.md
├── app/
│   ├── __init__.py
│   └── routes.py
├── tests/
│   ├── __init__.py
│   └── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── .flake8
├── .github/
│   └── workflows/
│       └── workflow.yml
├── .tekton/
│   ├── tasks.yml
│   ├── pipeline.yml
│   └── pipelinerun.yml
├── openshift/
│   ├── pvc.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── route.yaml
│   └── rbac.yaml
├── docs/
│   ├── DEPLOYMENT.md
│   ├── TROUBLESHOOTING.md
│   └── evidence/
│       └── README.md
├── .gitignore
└── .tekton/
```

## GitHub Actions explanation

The workflow in `.github/workflows/workflow.yml` runs automatically when code is pushed to `main`, when a pull request targets `main`, or when the workflow is manually dispatched.

It performs the following steps:

1. `Checkout source code`
2. `Set up Python`
3. `Install dependencies`
4. `Lint with flake8`
5. `Run unit tests with nose`

This ensures the code is linted and tested before it is merged or released.

## Local validation

Run the project checks locally with:

```bash
pip install -r requirements.txt -r requirements-dev.txt
flake8 app tests
PYTHONPATH=. nosetests -v tests
```

## OpenShift notes

Use `oc project` or `oc project -q` to identify the active namespace. The Tekton PipelineRun file expects the current project and the internal registry image path to be configured before execution.

For Buildah on a restricted cluster, the cluster administrator may need to authorize the service account with a privileged SCC, for example:

```bash
oc adm policy add-scc-to-user privileged -z tekton-pipeline -n <project>
```

## Next steps

- Commit the project to the repository.
- Push to GitHub.
- Create the OpenShift resources and run the PipelineRun.
- Validate the application through the generated Route.
