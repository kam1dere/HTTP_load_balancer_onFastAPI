#!/bin/bash


docker-compose up -t 100 --scale web=6 &
python3 spam.py &

bash ./restart.sh &
#sleep 35
#docker-compose logs --no-color >& docker_logs.txt && grep -P '"GET / HTTP/1.1" 200 OK' docker_logs.txt > webs_ok.txt &
#python3 final.py &
#sleep 10
#done




