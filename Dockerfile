FROM ubuntu
MAINTAINER Alex Mattson
ADD ./ ./
EXPOSE 8080
# install Python
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
# install twisted 
RUN ["pip","install","twisted"]
# fire up the server
CMD ["python","twisted_server.py"]
# ENTRYPOINT ["/bin/bash"]
