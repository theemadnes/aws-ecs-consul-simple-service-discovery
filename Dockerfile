FROM ubuntu
MAINTAINER Alex Mattson
ADD ./ ./
EXPOSE 8080
# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
RUN ["pip","install","twisted"]
RUN ["pip","install","dnspython"]
CMD ["python","twisted_server.py"]
# ENTRYPOINT ["/bin/bash"]
