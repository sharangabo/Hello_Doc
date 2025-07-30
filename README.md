# CI/CD Final Project

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)
[![CI/CD Pipeline](https://github.com/yourusername/ci-cd-final-project/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/ci-cd-final-project/actions/workflows/ci.yml)

This project demonstrates a complete CI/CD pipeline implementation using Tekton, GitHub Actions, and Kubernetes. It includes a sample Flask counter service. It serves as a practical example of modern DevOps practices and continuous integration/continuous deployment workflows.

## Features

- Automated testing and quality checks
- Containerized application deployment
- Kubernetes integration
- GitHub Actions workflow automation
- Tekton pipeline implementation
- File-based data persistence for counters (`counters.json`)

## Prerequisitess

- Python 3.9+
- Docker
- Kubernetes cluster
- Tekton installation
- GitHub account

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ci-cd-final-project.git
cd ci-cd-final-project
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application locally:

   The application uses Gunicorn as specified in the `Procfile`. You can run it using:
   ```bash
   honcho start
   ```
   Alternatively, for development, you can use Flask's built-in server (ensure `FLASK_APP` environment variable is set to `service:app`):
   ```bash
   export FLASK_APP=service:app  # On Windows: set FLASK_APP=service:app
   flask run --host=0.0.0.0 --port=8000
   ```

## Running Tests

To run the automated tests, use the following command:
```bash
nosetests -v --with-spec --spec-color
```
**Note on Python 3.10+:** `nosetests` version `1.3.7` (as used in this project) has an incompatibility with Python 3.10+ (`AttributeError: module 'collections' has no attribute 'Callable'`). The CI pipeline runs tests using Python 3.9, where this issue does not occur. If running locally on Python 3.10+, you might encounter this error.

## Project Structure

- `service/` - Main application code
- `tests/` - Unit and integration tests
- `.github/` - GitHub Actions workflows
- `.tekton/` - Tekton pipeline definitions
- `labs/` - Lab exercises and documentation

## CI/CD Pipeline

The project implements a complete CI/CD pipeline that includes:

- Automated testing
- Code quality checks
- Container image building
- Kubernetes deployment
- Environment promotion

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on IBM-CD0215EN-SkillsNetwork Introduction to CI/CD
- Instructor: John Rofrano, Senior Technical Staff Member, DevOps Champion, @ IBM Research

## <h3 align="center"> © IBM Corporation 2022. All rights reserved. <h3/>
