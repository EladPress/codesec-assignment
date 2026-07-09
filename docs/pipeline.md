# The CI pipeline in this project
This CI process builds, tests and pushes a Docker Image which contains the application.

## Tests Job
This job lints the app's code and runs the tests from the [tests/](../tests) directory.
It ```pip install```s and then uses Ruff to lint the project and pytest to run the tests.

## Build Job
This job builds the Docker Image and saves it as an artifact for the next stages. It does not push the image because it should not be pushed before all tests pass.

## Sanity Check Job
This job uses the built image and runs sanity checks on it, as in runs some checks on ```/health``` and ```/measure``` and checks if the expected status codes are received.

## Trivy Scan Job
THis job uses Trivy to scan the image for vulnerabilities.
The results are saved as an artifact that's saved for 7 days. (A production environment will of course offload these to a storage solution/DB of some kind.)
NOTE: No vulnerability will fail this build because removing vulnerabilities is not a part of this assignment.

## Push Image Job
This job logs in to Docker hub and then pushes the built image. The pushed image will have the following name+tag:
docker.io/eladpress/codsec-assignment:{BRANCH_NAME-BUILD_NUMBER}