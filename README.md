How to run:
1. install Docker and setup docker according to their official guide
2. clone the source code
3. in your command line:
	
	a. go into the source directory
	
	b. execute $ docker-compose up

You can cancel the runtime with ctrl+C.


For consecutive runs, we need to clean the environment.
In the source directory:
1. execute $ docker-compose down
2. list docker images
3. remove the docker image which name ends with "api"


MySQL Database is exposed on host port 3306.

Username is 'user'

Password is 'password'
