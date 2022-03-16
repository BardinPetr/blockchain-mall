#! /bin/bash

docker build -f ./frontend/Dockerfile.pre ./frontend -t registry.gitlab.com/onti-fintech/onti-2022-fintech/fintech2022004/mall/bardinpetr/frontend-base:latest
docker push registry.gitlab.com/onti-fintech/onti-2022-fintech/fintech2022004/mall/bardinpetr/frontend-base:latest

docker build -f ./backend/Dockerfile.pre ./backend -t registry.gitlab.com/onti-fintech/onti-2022-fintech/fintech2022004/mall/bardinpetr/backend-base:latest
docker push registry.gitlab.com/onti-fintech/onti-2022-fintech/fintech2022004/mall/bardinpetr/backend-base:latest
