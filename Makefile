all: run

run:
	sudo python3 src/gymkhana.py

clean:
	@find . -name '*.pyc' -exec rm -vf {} \;
