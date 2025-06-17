truc: 
	echo "This is a Makefile example."

install :
	@echo "Installing the application..."
	pip-compile requirements.in
	pip install -r requirements.txt --quiet
	pip install -e . --quiet
	@echo "✅ Application installed successfully. "

.PHONY : train
train : install
	@echo "Training the model..."
	@echo "This may take a while, please be patient."
	@echo "Running training script..."
	python -c "from main import train; train()"
	@echo "✅ Model trained successfully."

.PHONY : tests
tests :
	@echo "Running tests..."


###################################################

# Web

run_api:
	@echo "Starting the FastAPI application..."
	uvicorn api.webapi:api --host 0.0.0.0 --port 8000 --reload

test_api:
	@echo "Running API tests..."
	curl -X 'GET' \
		'http://127.0.0.1:${PORT}/predict?PassengerId=1&Pclass=1&Name=John%20Doe&Sex=male&Age=30&SibSp=0&Parch=0&Ticket=A%2F5%2021171&Fare=7.25&Cabin=C85&Embarked=S' \
		-H 'accept: application/json'


###################################################

# Docker
docker_build_api:
	@echo "Building Docker image..."
	docker build -t myapi:latest .

docker_run_api: docker_build_api
	@echo "Running Docker container..."
	docker run -p ${PORT}:${PORT} -e PORT=${PORT} myapi:latest

docker_build_gcp_api : 
# If you are on linux : 
# docker build -t $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) .
# If you are on macOS m4 is not supported, so we use the --platform flag
	docker build --platform linux/amd64 -t $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) .

push : docker_build_gcp_api
	@echo "Pushing Docker image to Google Container Registry..."
	docker push $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION)

deploy: push
	gcloud run deploy $(IMAGE_NAME) \
		--image $(LOCATION)-docker.pkg.dev/$(PROJECT_ID)/$(REPOSITORY)/$(IMAGE_NAME):$(VERSION) \
		--platform managed \
		--region $(LOCATION) \
		--allow-unauthenticated \
		--project $(PROJECT_ID)

