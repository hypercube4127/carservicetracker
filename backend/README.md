# Flask App Backend

This project is a Flask-based backend application designed to provide authentication and user management services. It uses various Flask extensions for database management, JWT authentication, and CORS handling.

## Table of Contents

- [Manual installation](#manual-installation)
  - [Requirements](#requirements)
  - [Steps](#steps)
- [Dockerized installation](#dockerized-installation)
  - [Requirements](#requirements-1)
  - [Steps](#steps-1)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [pyproject.toml](#pyprojecttoml)

## Manual installation
### Requirenments

- Python 3.12 (if you don't want to use the containerized development mode)

### Steps
1. Clone this repository

2. Install dependencies using Poetry:

  ```
  poetry install
  ```

3. Set up environment variables:

  Create a `.env` file in the root directory with the following content:

  ```env
  FLASK_PORT=5000
  DB_URL=postgresql://postgres:password@db/mydb
  SECRET_KEY=your_secret_key
  ```
4. Run project
  ```
  poetry run start
  ```

## Dockerized installation
### Requirenments

- Docker (optional, for containerized development)

### Steps

To start this project in devcontainers, follow these steps:

1. Install Docker on your machine if you haven't already.

2. Clone this repository to your local machine.

3. Open the project in Visual Studio Code.

4. Install recommended [Remote - Development extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack) in Visual Studio Code.

5. Click on the blue icon in the bottom left corner of Visual Studio Code and select "Remote-Containers: Reopen in Container".

6. Visual Studio Code will now build the containers and start the project inside the container.

7. Once the container is up and running, you can check the project at `http://localhost:4200`.

That's it! You have successfully started the project in devcontainers. Happy coding!

## Configuration

### Environment Variables

- `FLASK_PORT`: The port on which the Flask app will run.
- `DB_URL`: The database URL for SQLAlchemy.
- `SECRET_KEY`: The secret key for JWT and Flask sessions.

### pyproject.toml

The `pyproject.toml` file contains project metadata and dependencies. It also includes custom configurations:

```toml
[custom]
app-title = "Flask App"
```
## Basic Commands to flask migrations

### Create a Migration
After making changes to your models, generate a new migration file:
```
flask db migrate -m "Add a description of the changes"
```
This creates a migration script in the migrations/versions/ folder.

### Apply a Migration
Apply the migration to your database:
```
flask db upgrade
```

### Downgrade a Migration
If you need to undo the last migration:
```
flask db downgrade
```

### Show Migration Status
To see the current migration status:
```
flask db current
```