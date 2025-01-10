FROM python:3.12-alpine

ENV NAMESPACE="jupyterhub"

RUN apk add gcc
RUN pip install --upgrade pip
RUN pip install kubernetes
RUN pip install lscsde_workspace_mgmt
RUN MULTIDICT_NO_EXTENSIONS=1 pip install kopf
RUN mkdir -p /src
RUN mkdir -p /repos
RUN chmod 0777 /repos
ADD ./src/ /src

CMD kopf run /src/service.py -A --standalone

ENV REQUIRED_APPROVAL_TYPES="INFORMATION_GOVERNANCE,DATA_ENGINEER"
ENV CHECK_DUPLICATE_EMAIL="True"