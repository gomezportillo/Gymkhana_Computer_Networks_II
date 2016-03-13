all: run

run:
	sudo python3 src/gymkhana.py

clean:
	@find . -name '*__pycache__' -exec rm -vrf {} \;
	@find . -name '*.pyc' -exec rm -vf {} \;
