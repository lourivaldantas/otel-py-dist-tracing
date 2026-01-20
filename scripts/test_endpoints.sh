#!/bin/sh
while true; do
curl http://localhost:5001/getUsers
sleep 120
curl http://localhost:5001/rotaErrada
curl http://localhost:5001/getUsers
sleep 180
done
