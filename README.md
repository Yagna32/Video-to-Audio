# Video-to-Audio
3:52:00

develop service > write docker file and push on docker hub > write yaml files for container orchestration > deploy on kubernetes cluster 

To set scale of replicas : 
kubectl scale deployment --replicas=0 gateway
To make image : docker build .
To give name : docker tag image_id new_name
To deploy on kubernetes cluster:
kubectl apply -f ./
To delete files created on K8s:
kubectl delete -f ./ 
To test microservice architecture : minikube tunnel
To add an addon in minikube for eg. ingress
minkube addons enable ingress
minikube addons list //check status and list addons

#rabbitmq:
durability :
 Durable:queue exists even when the container restarts 
 Transient: queue does not exists if container stops 

#Error:
0. Converter crashes after video uploads(fixed)