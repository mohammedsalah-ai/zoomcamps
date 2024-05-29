FROM quay.io/jupyter/tensorflow-notebook:latest
LABEL purpose="all tools, one place"
RUN pip3 install mlflow==2.13.0
ENTRYPOINT [ "/bin/bash" ]

# docker container run -it -p 8888:8888 -v ./notebooks:/home/jovyan/work --name notebook --restart unless-stopped mlflow/tensorflow