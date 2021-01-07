How to run:
1. install Docker and setup docker according to their official guide
2. clone the source code
3. in your command line:</br>	
	a. go into the source directory</br>	
	b. execute $ docker-compose up

You can cancel the runtime with ctrl+C.
</br></br>

For consecutive runs, we need to clean the environment.
In the source directory:
1. execute $ docker-compose down
2. list docker images
3. remove the docker image with the name of this repository
</br></br>

MySQL Database is exposed on host port 3306.</br>
Username is 'user'</br>
Password is 'password'
