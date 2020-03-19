# microservice-template

## Dependencies
1. python3
2. packages see requirements.txt

## Develop
1. ``pip3 install requirements.txt``
2. start with ``python3 template.py``
3. add whichever route you want, and do whatever you want regarding
to algorithms, requests, data processing, data mining,
machine learning, machine reasoning, etc, in your route
4. return a json as seen in the code

--> every functionality created and published like this can be consumed online by inseri


## Publish on Dockerhub
Always add your dependencies to requirements.txt, otherwise they
the docker built will fail

1. ``docker build -t microservice-template .``
2. Start it locally to test it: 
``docker run -p 8080:8080 microservice-template``
3. ``docker login``
4. ``docker tag <DockerImageId> user/imageName:tag``
5. ``docker push user/imagename:tag``
