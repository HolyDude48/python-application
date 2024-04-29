Start minikube with metrics server
==================================
minikube start --extra-config=kubelet.housekeeping-interval=10s --nodes 2 -p multinode-mini\
minikube addons enable metrics-server -p multinode-mini

Create secret for DB password
=============================
kubectl create secret generic db-password --from-literal=password=xxxxxx -n python

Install python app
==================
helm upgrade --install pythonapp . -n python

Configure database for python app
=================================
kubectl exec -it mysql-pod-name -- sh\
mysql -u root -p\
CREATE DATABASE pythonapp;\
USE pythonapp;\
CREATE TABLE user_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    place VARCHAR(255) NOT NULL
);

Accessing the application
=========================
kubectl port-forward svc/pythonapp 5000:5000 -n python\
Hit localhost:5000 in the browser
