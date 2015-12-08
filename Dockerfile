FROM ubuntu
MAINTAINER Alex Mattson
ADD ./ ./
EXPOSE 80
# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv && \
  rm -rf /var/lib/apt/lists/*
CMD ["python","server.py"]
# ENTRYPOINT ["/bin/bash"]
