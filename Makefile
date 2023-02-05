PACKAGE="TestMT"

create_env:
	conda env create --name ${PACKAGE} --file=environment.yml

build_kernel:
	python3 -m ipykernel install --user --name ${PACKAGE}

start_app_py:
	(cd ./app/ && sh ../start.sh)

build_docker:
	docker build --compress -t en-ru-translator:latest .

start_app_docker:
	sh docker_run.sh

start_app_k8s:
	minikube start --memory 7600 && \
	eval $(minikube docker-env) && \
	build_docker && \
	kubectl apply -f deployment/deployment.yaml && \
	kubectl apply -f deployment/service.yaml && \
	minikube service mt-serving-service
	# in another terminal potentially you can run: minikube dashboard

stress_test_k8s_server:
	minikube addons enable metrics-server && \
	# check: kubectl get deployment metrics-server -n kube-system
	sleep 10 && \
	kubectl apply -f deployment/autoscale.yaml && \
	# check: kubectl get hpa
	sleep 10 && \
	sh stresstest.sh

clean_k8s:
	kubectl delete -f deployment && minikube delete
