# Flask-Angular App Frontend

## Table of Contents

- [Manual installation](#manual-installation)
  - [Requirements](#requirements)
  - [Steps](#steps)
- [Dockerized installation](#dockerized-installation)
  - [Requirements](#requirements-1)
  - [Steps](#steps-1)

## Manual installation

### Requirenments

- node.js (if you don't want to use the containerized development mode)

### Steps

1. Clone this repository

2. Install dependencies using Node Package Manager:

  ```
  npm install
  ```
3. Run project

  ```
  npm run serve
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