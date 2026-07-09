# Elad Press | Assignment for Codsec

This project is a REST service that measures the response time of any HTTP resource.

The project is written with Python using the FastAPI package.

The project can be deployed in multiple ways:

### Production

1. Using the manifests in [manifests/](../manifests) on a Kubernetes instance
2. Using the [terraform/](../terraform) directory to deploy using AWS ECS

Of course, these two ways contradict each other, as ECS is incompatible with k8s manifests. I chose to deploy on ECS instead of EKS because this is a much cheaper and simpler solution for a project of this scale. EKS is for projects of much bigger scale that need the complexity.

### Testing

If you want to run this project for testing/development purposes, you can:

3. Run it locally with a virtualenv:

   ```
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   uvicorn app.main:app
   ```

4. Run the Docker image from Docker Hub:

   ```
   docker run -d -p 8000:8000 eladpress/codsec-assignment:latest-main
   ```

5. Build the Docker image locally and run it:

   ```
   docker build -t codsec .
   docker run -d -p 8000:8000 codsec
   ```

