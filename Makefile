PACKAGE="TestMT"

env:
	conda env create --name ${PACKAGE} --file=environment.yml

kernel:
	python3 -m ipykernel install --user --name ${PACKAGE}