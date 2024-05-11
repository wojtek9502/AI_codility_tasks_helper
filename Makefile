python = .venv/bin/python
pip = .venv/bin/pip


up:
	docker compose up --build -d

down:
	docker compose down

rebuild:
    docker-compose build
    docker compose up -d --force-recreate

uninstall-unrequired-libraries:
	$(pip) freeze | grep -v -f requirements.txt - | grep -v '^#' | xargs $(pip) uninstall -y || echo "OK, you dont have any unrequired libraries"

install: uninstall-unrequired-libraries
	$(pip) install -r requirements.txt

install-venv:
	$(python) -m virtualenv .venv --python python3

update-requirements:
	$(pip) freeze > requirements.txt

