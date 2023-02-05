while sleep 0.01;

do curl -X POST http://$(minikube ip):30001/predict -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"input": "This is text in english"}';

done