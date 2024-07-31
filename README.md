# FastAPI Hatch Template

-----

## Table of Contents

- [Rationale](#Rationale)
- [Installation](#installation)
- [Running the Unit Tests](#running-the-unit-tests)
- [Code Linting](#code-linting)
- [Supported Scripts](#supported-scripts)
- [Folder Structure](#folder-structure)
- [License](#license)


## Rationale

The purpose of this project is to provide a comprehensive starter package for FastAPI projects, incorporating best practices I have gathered over the years. Each time I begin a new project or tackle a home assignment, I spend a significant amount of time setting up a solid foundation for a Python FastAPI project. This template aims to streamline that process.

### Key Features of the FastAPI Hatch Template

- Modern FastAPI project with async SQLAlchemy and Alembic for database operations
- Hatch integration for streamlined package and environment management
- Async unit testing with Pytest and Testcontainers for isolated database testing
- Docker Compose setup for PostgreSQL database
- Comprehensive configuration in pyproject.toml
- Separated virtual environments for development, testing, and pre-commit hooks
- Pre-commit hooks and linters (Ruff, Pyright, Bandit) for code quality
- CLI management commands, including async database seeding
- uv package manager for improved performance
- Incorporates latest web app best practices (as of 2024)

## Dependencies

- Docker - [https://orbstack.dev/](https://orbstack.dev/) (Recommended: Install Orb Stack via the website or by running `brew install orbstack`)
- Hatch - [https://hatch.pypa.io/latest/install/](https://hatch.pypa.io/latest/install/)

## Installation

1. Clone the repository:
    ```console
    git clone https://github.com/cdragos/fastapi-hatch-template
    ```

2. Install the Python version using Hatch:
    ```console
    hatch python install 3.12
    ```

3. Create the virtual environments:
    ```console
    hatch env create
    hatch env create test
    hatch env create hooks
    ```

4. Run Docker Compose to start the PostgreSQL server:
    ```console
    docker compose up
    ```

5. Run the database migrations:
    ```console
    hatch run upgrade
    ```

6. Seed the database with initial data:
    ```console
    hatch run seed_db
    ```

7. Run the FastAPI development server:
    ```console
    hatch run dev
    ```

8. Curl the users endpoint:
    ```console
    curl http://localhost:8000/users
    ```

## Running the Unit Tests

Unit tests require Docker to be installed, as they use Testcontainers. These tests are self-contained, using a clean database that rollbacks test data after each test.

1. Run the unit tests:
   ```console
   hatch run test:test
   ```

## Code Linting

We have two ways to ensure that our code is linted and formatted.

1. Use Hatch formatting after making changes:
    ```console
    hatch fmt -f        # Run ruff format
    hatch fmt -l        # Run ruff
    hatch fmt --check   # Run ruff check, Pyright, and Bandit
    ```

2. Use the pre-commit hook:
    ```console
    hatch env shell hooks       # Activate the hooks environment
    pre-commit install          # Install the pre-commit hooks
    pre-commit run --all-files  # Run the pre-commit hooks
    ```

## Supported Scripts

The project supports a variety of scripts to streamline development, database operations, testing, and code quality checks.

### Development and Database Operations
- **dev**: Runs the FastAPI development server.
```console
  hatch run dev
```
- make_migrations: Creates a new database migration with Alembic.
```console
  hatch run make_migrations
```
- upgrade: Applies all pending database migrations.
```console
  hatch run upgrade
```
- seed_db: Seeds the database with initial data.
```console
  hatch run seed_db
```
### Testing

- test: Executes all unit tests using Pytest.
```console
  hatch run test:test
```

### Code Quality and Linting

- hatch fmt -f: Automatically fixes code formatting issues with Ruff.
```console
  hatch fmt -f
```

- hatch fmt -l: Runs the Ruff linter.
```console
  hatch fmt -l
```

- hatch fmt --check: Checks code formatting and runs a series of linting checks (Ruff, Pyright, Bandit) to ensure code quality.
```console
  hatch fmt --check
```

## Folder Structure

This structure highlights the main components of your FastAPI Hatch Template:

- `alembic/`: Contains database migration scripts and configurations.
- `seeds/`: Stores seed data files for populating the database.
- `src/`: The main source code directory.
  - `fastapi_hatch_template/`: Core application package.
    - `api/`: Defines API routes and endpoints.
    - `db/`: Manages database connections and sessions.
    - `schemas/`: Contains Pydantic models for request/response validation.
  - `models/`: Defines SQLAlchemy ORM models.
  - `scripts/`: Holds utility scripts, such as data seeding.
  - `tests/`: Contains test files and configurations.
- `docker-compose.yml`: Docker Compose configuration for setting up the development environment.
- `pyproject.toml`: Project configuration and dependency management.

## License

`fastapi-hatch-template` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
