#kill all running processes associated with docker
docker kill $(docker ps -a -q)

#remove the containers
docker rm $(docker ps -a -q)
