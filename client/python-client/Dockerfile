FROM frolvlad/alpine-python3

RUN apk update
RUN apk add --update bash
WORKDIR /src
ADD client.py /src
ADD requirements.txt /src
#RUN pip install --upgrade pip
RUN cd /src && pip3 install -r requirements.txt
#ENTRYPOINT /bin/bash
EXPOSE 8765
CMD python3.5 -u ./client.py

