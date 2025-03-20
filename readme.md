# User Creation and Login Service using Python FastAPI

This service provides endpoints for user registration and authentication using Python FastAPI. It allows users to register with a username and password and authenticate themselves to access protected resources. The service ensures secure handling of user credentials and supports JWT-based authentication.

## Installation

### Prerequisites:

- Python 3.6 or later
- pip
- Docker Desktop

### Environment Variables

To test the code locally, create a `.env` file and add the following environment variables:

```ini
DATABASE_CONNECTION_STRING=<Enter the connection string for the PostgreSQL database or the SQLite DB path>
JWT_SECRET=<Base64-encoded string for the JWT secret>
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_MINUTES=<Desired token expiration time in minutes>
```

### Installing Dependencies

Run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

### Running the Server Locally

To start the FastAPI server locally, execute:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables automatic reloading of the application upon code changes. The server will be accessible at [http://localhost:8000](http://localhost:8000).

## Deployment

To deploy the application, build a Docker image and push it to a container registry such as [Docker Hub](https://hub.docker.com), [Azure Container Registry](https://azure.microsoft.com/en-us/products/container-registry), or [Amazon Elastic Container Registry](https://aws.amazon.com/ecr/).

### Building the Docker Image

Run the following command to build the Docker image:

```bash
docker build -t <image-name>:<tag> .
```

### Pushing the Image to a Container Registry

First, log in to the container registry:

```bash
docker login <registry-url> -u <username> -p <password>
```

> **Note:** The `registry-url` is not required when using Docker Hub.

Then, push the Docker image:

```bash
docker push <registry-url/username>/<image-name>:<tag>
```

### Deploying the Container

Once the image is pushed, deploy it using a container service such as:

- **Azure**: Azure Container Instances, Azure App Service
- **AWS**: Amazon ECS, AWS Fargate
- **Google Cloud**: Cloud Run, GKE

This ensures a scalable and managed deployment of your FastAPI service.
