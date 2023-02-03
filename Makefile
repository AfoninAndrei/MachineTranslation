PACKAGE="TestMT"

env:
	conda env create --name ${PACKAGE} --file=environment.yml

kernel:
	python3 -m ipykernel install --user --name ${PACKAGE}

build_docker:
	docker build -t EN-RU-Translator:latest .
