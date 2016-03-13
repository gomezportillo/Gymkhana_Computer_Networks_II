all: run

run:
	sudo python3 src/gymkhana.py

clean:
	@sudo find . -name '*__pycache__' -exec rm -vrf {} \;
