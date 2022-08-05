# Dockerized Python Command-Line Program

## Common Usage
Python command-line tool allows to:
- download chemical compound information from API ebi-ac-uk
- view downloaded data as as a table in command line

---
## Prerequsites
- Python 3.9.x
- Python Virtual Environment (preferable)
- Git
- Docker
- Docker compose
---
## Common setup
Clone the repo and install the dependencies.
```
git clone https://github.com/pyforge3-final-project-anag.git
cd pyforge3-final-project-anag/
```

Download Docker Desktop from [the official website](https://docs.docker.com/desktop/). It will automatically install docker compose for you.

Navigate to Docker Desktop, there on Homepage there is [PostgreSQL docker official image](https://hub.docker.com/_/postgres).
Start running the official docker image.
You can check that it is working correct from CLI by following instructions provided in the container **PostgreSQL Overview**. 

The app is connected to PostgreSQL database so in order to run this app first connect to database. After connecting to database, create `.env` file similar to `.env_sample` file and specify all environmental variables.

### Run application locally

If virtual environment is available run the following command

```
python3 -m pip install -r requirements.txt
```

else:
```
pip3 install -r requirements.txt
```

After starting postgres:latest container successfully, application can be run locally. 

Navigate to the root directory and from there run command
```
python3 src/app.py
```

Result should be the following:
![executed_test_cases](__screenshots/local_run.png?raw=true "Title")

### Build Images and Run Containers With Docker Client

After starting postgres:latest container successfully, python image can be created. 

Navigate to the source directory and from there run command in order to build the image
```
cd src
docker build -t python-app-1 .
```
After successful build, run the container by the command
```
docker run -it python-app-1
```

After running python app image, in CLI content of PostgreSQL table content should be printed out:
![executed_test_cases](__screenshots\docker_client_result.png?raw=true "Title")

### Run Containers With Docker Compose

Another option to run docker container it is by using this command after moving back to the root directroy
```
cd ..
docker compose up
``` 
in the directory where docker compose file is located.

After finishig tasks, the container can be switched off by running this command 
```
docker compose down
```

Result should be the following:

![executed_test_cases](__screenshots/docker_compose_result.png?raw=true "Title")
---
## Testing
Run tests in the command line by following command
```
python -m unittest discover -s tests
```
In the command line following result should be present:

![executed_test_cases](__screenshots/executed_test_cases.png?raw=true "Title")
---
## Logging

For troubleshooting and debugging purposes logs are preserved in `console.log` file, which is created automatically upon running the application, be that locally or in container.

The beginning of the file looks like this:
![console_log](__screenshots/console_log.png?raw=true "Title")