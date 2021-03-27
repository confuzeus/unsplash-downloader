requirements:
	pip-compile --upgrade --generate-hashes --output-file requirements.txt requirements.in
	pip-sync requirements.txt
