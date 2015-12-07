FROM centos
ADD ./ ./
EXPOSE 80
CMD python ./server.py
