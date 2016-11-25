# Autonomous Vehicle Cloud

Make sure to install the following dependencies:

- Python 3.5 - http://askubuntu.com/a/710865
- Python modules - `pip install -r requirements.txt`

To run the server and the client, cd into the direcotry, then run `./server.py` in one terminal and `./client.py` in another


## Docker instructions

0. Make sure Docker is installed and Docker daemon is running.
1. Build the server image by running `sudo docker build -t connected-cloud .`
2. Run the Docker container using the newly created image by `sudo docker run capstone-server`

