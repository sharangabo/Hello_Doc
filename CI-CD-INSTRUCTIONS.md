# CI/CD Pipeline Implementation Instructions

This project implements a complete CI/CD pipeline using GitHub Actions, Tekton, and OpenShift.

## GitHub Actions CI Pipeline

The GitHub Actions workflow is configured in `.github/workflows/ci.yml` and will automatically run on push to the main branch or when pull requests are created against the main branch.

It performs:

- Linting with flake8 and pylint
- Unit testing with nose

## Tekton Pipeline on OpenShift

The Tekton pipeline components are in the `.tekton` directory and include:

- Individual tasks for linting, testing, building, and deploying
- A complete pipeline that chains these tasks together
- A PipelineRun template to trigger the pipeline

### Prerequisites

1. Access to an OpenShift cluster with Tekton/OpenShift Pipelines installed
2. OpenShift CLI (`oc`) installed and logged in
3. A project/namespace where you have permissions to create resources

### Setup and Deployment

1. **Create a project in OpenShift (if needed)**:

   ```bash
   oc new-project your-project-name
   ```

2. **Apply the Tekton Tasks**:

   ```bash
   oc apply -f .tekton/lint-task.yaml
   oc apply -f .tekton/unit-test-task.yaml
   oc apply -f .tekton/build-image-task.yaml
   oc apply -f .tekton/deploy-task.yaml
   ```

3. **Apply the Pipeline**:

   ```bash
   oc apply -f .tekton/ci-pipeline.yaml
   ```

4. **Create the PVC for the workspace**:

   ```bash
   oc apply -f .tekton/pipeline-run.yaml --selector kind=PersistentVolumeClaim
   ```

5. **Run the Pipeline**:

   ```bash
   oc apply -f .tekton/pipeline-run.yaml --selector kind=PipelineRun
   ```

6. **Monitor Pipeline Execution**:

   ```bash
   # View PipelineRuns
   oc get pipelineruns

   # Get detailed status
   oc describe pipelinerun app-ci-pipeline-run

   # View logs
   tkn pipelinerun logs app-ci-pipeline-run -f
   ```

7. **Access the Deployed Application**:
   After successful deployment, you can access the application via the route:
   ```bash
   oc get route flask-app
   ```

## Pipeline Architecture

1. **GitHub Actions CI**:

   - Triggered on push/PR to main
   - Lints and tests code
   - Provides quick feedback

2. **Tekton Pipeline (OpenShift)**:
   - **Lint Task**: Code quality check
   - **Test Task**: Unit tests
   - **Build Task**: Builds container image
   - **Deploy Task**: Deploys to OpenShift

## Continuous Delivery

The automated deployment to OpenShift means changes pushed to the main branch will:

1. Trigger CI on GitHub
2. Trigger the Tekton pipeline (manually or via webhooks if configured)
3. Deploy the updated application

## Troubleshooting

- If tasks fail, check the logs with `tkn taskrun logs <taskrun-name>`
- For deployment issues, check the OpenShift UI or use `oc status`
- Ensure the service account running the pipeline has the necessary permissions
