all: run

run:
	sudo python3 glade.py
	#sudo python3 glade.py

clean:
	@sudo find . -name '*__pycache__' -exec rm -vrf {} \;
