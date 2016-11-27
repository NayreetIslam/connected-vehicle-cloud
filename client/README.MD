# Connected Vehicle Cloud

Make sure to install the following dependencies:

- Python 3.5 - http://askubuntu.com/a/710865
- Python modules - `pip3 install -r requirements.txt`

To run the server and the client, cd into the direcotry, then run `./server.py` in one terminal and `./client.py` in another


## Docker instructions

0. Make sure Docker is installed and Docker daemon is running.

1. Build the server image by running one of the following commands:
1a. For ARM devices: `sudo docker build -f Dockerfile_arm -t connected-cloud-server .`
1b. For x86 devices: `sudo docker build -f Dockerfile_x86 -t connected-cloud-server .`
2. Run the Docker container using the newly created image by `sudo docker run -p 8765:8765 connected-cloud-server`

3. Build the client image for testing by running one of the following commands:
3a. For ARM devices: `sudo docker build -f Dockerfile_arm -t connected-cloud-client .`
3b. For x86 devices: `sudo docker build -f Dockerfile_x86 -t connected-cloud-client .`
4. Run the Docker container using the newly created image by `sudo docker run -it connected-cloud-client -i 'ServerIP'`
