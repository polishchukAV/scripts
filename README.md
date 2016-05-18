#!/bin/bash
set -e

for i in $(docker --host=$DOCKER_API_HOST ps -a | grep selenium | awk '{print $1}')
do
	docker --host=$DOCKER_API_HOST rm -f $i
    echo "container $i deleted"
done

results="./results.xml"
if [ -f "$results" ]
then
	rm -f $results.old && mv $results $results.old
fi


#Check state of container and if containers don't exist run it
#HUB
HUB_ID=$(docker --host=$DOCKER_API_HOST ps | grep "selenium/hub" | awk '{print $1}')
if [ -z "$HUB_ID" ]
then 
    	HUB_ID=`docker --host=$DOCKER_API_HOST run -d --name hub -p 0.0.0.0:8082:4444 selenium/hub`
        sleep 5
fi

#CHROME
CHR_ID=$(docker --host=$DOCKER_API_HOST ps| grep "selenium/node-chrome-debug" | awk '{print $1}')
if [ -z "$CHR_ID" ]
then 
    	CHR_ID=`docker --host=$DOCKER_API_HOST run -d  --link hub:hub -p 0.0.0.0:8083:5900 --name chrome-deb selenium/node-chrome-debug`
        sleep 5
fi

#FIREFOX
FFX_ID=$(docker --host=$DOCKER_API_HOST ps| grep "selenium/node-firefox-debug" | awk '{print $1}')
if [ -z "$FFX_ID" ]
then 
    	FFX_ID=`docker --host=$DOCKER_API_HOST run -d  --link hub:hub -p 0.0.0.0:8084:5900 --name fire-deb selenium/node-firefox-debug`
        sleep 5
fi

#RUN TESTS
py.test -v --junit-xml=$results ./python-ui-tests/test_suit.py   

#docker --host=$DOCKER_API_HOST rm -f $HUB_ID
#docker --host=$DOCKER_API_HOST rm -f $CHR_ID
#docker --host=$DOCKER_API_HOST rm -f $FFX_ID

#docker --host=$DOCKER_API_HOST rmi -f selenium/hub
#docker --host=$DOCKER_API_HOST rmi -f selenium/node-chrome-debug
