# PyForge3 Final Project
## Dockerized Python Command-Line Program
Download Docker Desktop from [the official website](https://docs.docker.com/desktop/). It will automatically install docker compose for you.

Navigate to Docker Desktop, there on Homepage there is [PostgreSQL docker official image](https://hub.docker.com/_/postgres).
Start running the official docker image.
You can check that it is working correct from CLI by following instructions provided in the container **PostgreSQL Overview**. 

In my code Port is hardcoded in variable `db_port`, which will require to be changed since it rotates after starting postgres:latest container anew.

After starting postgres:latest container successfully, python image can be created. Navigate to the app directory and from there run command `docker build -t python-app-1 .`. After successful build, run the image by the command `docker run -it python-app-1`.

After running python app image, in CLI content of PostgreSQL table content should be printed out.

Another option to build the docker image and run it is by using this command `docker compose up` in the directory where docker compose file is located. After finishig tasks, the container can be switched off by running this command `docker compose down`.