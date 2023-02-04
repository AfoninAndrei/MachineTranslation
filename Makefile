PACKAGE="TestMT"

env:
	conda env create --name ${PACKAGE} --file=environment.yml

kernel:
	python3 -m ipykernel install --user --name ${PACKAGE}

build_docker:
	docker build --compress -t en-ru-translator:latest .

start:
	(cd ./app/ && sh ../start.sh)