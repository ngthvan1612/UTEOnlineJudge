
migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

static:
	python3 manage.py collectstatic --noinput

run:
	python3 manage.py runserver


deploy:
	sudo docker-compose -f docker-compose.prod.yml down
	sudo docker-compose -f docker-compose.prod.yml build

deployrmv:
	sudo docker volume rm $$(sudo docker volume ls -q)

rundeploy:
	sudo docker-compose -f docker-compose.prod.yml up
