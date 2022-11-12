#!/bin/bash

docker-compose up -t 350 --scale web=6 -d &

python3 spam.py &
bash ./restart.sh &

sleep 50
for ((i=1; i <= 30; i++))
do
  docker-compose logs --no-color >& docker_logs.txt && grep -P '"GET / HTTP/1.1" 200 OK' docker_logs.txt > webs_ok.txt &
  python3 get_statistics.py &
  sleep 10
done




