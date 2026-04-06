# using portainer to build image:
#    name: n8n-custom:v0.1.0
#    URL: https://github.com/VictorArsjad/homelab.git#add-actual-budget-api-and-n8n-integration
#    dockerfile path: docker/stacks/n8n/Dockerfile

# dockerfile is unused

FROM docker.n8n.io/n8nio/n8n:1.123.5
USER root

RUN apk add --no-cache python3 make g++

RUN npm install -g @actual-app/api

USER node