#!/bin/bash
sleep 150
docker stop bwg_web_2 &
sleep 100
docker start bwg_web_2


