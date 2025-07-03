# Healthcare Platform

## Project Overview

The Healthcare Platform is a modern web application designed to streamline healthcare management for providers and patients. It offers secure patient data handling, appointment scheduling, and communication tools, all built with scalability and security in mind.

This project is developed as part of a professional software engineering course, with a strong emphasis on best practices in project planning, repository security, and automated quality assurance.

---

## Project Planning & Management

- **Project Board:**  
  [GitHub Project Board Link](<insert-your-project-board-link-here>)

- **Milestones & Epics:**  
  - Application Baseline
  - Containerization
  - Infrastructure as Code (IaC)
  - Continuous Deployment (CD) Pipeline

- **Task Management:**  
  All major milestones are broken down into actionable issues and tasks, tracked on the project board. Tasks are moved across columns ("To Do", "In Progress", "Done") as work progresses.

---

## Project Structure & Workflow

The project is organized into three main Epics, each with actionable tasks tracked as GitHub Issues and managed on the Project Board.

### 1. Project Planning & Management
- **Epic:** Project Planning & Management
- **Tasks:**
  - Create and maintain a GitHub Project board (columns: To Do, In Progress, Done)
  - Create high-level issues for course milestones (Containerization, IaC, CD Pipeline, etc.)
  - Break down each phase into detailed, actionable issues
  - Keep all issues updated and move them across board columns as work progresses
  - Ensure each pull request is linked to its corresponding issue

### 2. Repository Security & Git Usage
- **Epic:** Secure Repository Setup
- **Tasks:**
  - Create `develop` branch alongside `main`
  - Enable branch protection on `main` (PR required, at least 1 reviewer, CI status checks)
  - Use feature branches for all changes (e.g., `feature/login-form`)
  - Write clear, atomic commits with descriptive messages

### 3. Application Development & CI Pipeline
- **Epic:** Baseline Application & CI Setup
- **Tasks:**
  - Develop the initial application based on the approved proposal
  - Write unit tests for baseline functionality
  - Set up CI pipeline using GitHub Actions
  - Run linting and unit tests on every PR
  - Configure CI as a required status check for merging

---

## Secure Repository Setup

- **Branches:**  
  - `main` (protected)  
  - `develop` (active development)

- **Branch Protection Rules:**  
  - Pull Requests required before merging to `main`
  - At least one reviewer approval required
  - Status checks from CI pipeline must pass before merging

- **Workflow:**
  - All changes are made in feature branches (e.g., `feature/login-form`)
  - Each pull request must be linked to an issue and reviewed before merging
  - Commits should be clear, atomic, and descriptive

---

## Application Baseline

The initial version of the Healthcare Platform includes:

- Basic project structure (backend and/or frontend)
- Initial endpoints or UI components
- Linting and unit test setup

---

## Continuous Integration (CI)

- **CI Pipeline:**  
  Implemented using [GitHub Actions/Azure Pipelines].  
  - Runs on every Pull Request
  - Lints code for style and errors
  - Runs all unit tests
  - CI status checks are required to pass before merging to `main`

---

## Local Setup Instructions

### Prerequisites

- [Node.js](https://nodejs.org/) (v14+ recommended)
- [npm](https://www.npmjs.com/) or [yarn](https://yarnpkg.com/)
- [Git](https://git-scm.com/)

### Clone the Repository

```sh
git clone <your-repo-url>
cd hello_doc/Hello_Doc/healthcare-platform/server
```

### Install Dependencies

```sh
npm install
```

### Run the Application

```sh
npm start
```

### Run Linter

```sh
npm run lint
```

### Run Unit Tests

```sh
npm test
```

---

## Contributing

1. Create a feature branch from `develop`.
2. Commit your changes.
3. Open a Pull Request to `develop`.
4. Ensure all CI checks pass and request a review.

---

## License

This project is licensed under the MIT License.

---

## Links

- **Repository:** [GitHub Repo Link](<insert-your-repo-link-here>)
- **Project Board:** [Project Board Link](<insert-your-project-board-link-here>) 
