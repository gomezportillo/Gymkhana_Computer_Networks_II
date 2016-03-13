all: run

run:
	python3 src/gymkhana.py
	#sudo python3 src/gymkhana.py

clean:
	@find . -name '*.pyc' -exec rm -vf {} \;
