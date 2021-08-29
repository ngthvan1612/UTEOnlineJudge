migrate:
	python manage.py makemigrations
	python manage.py migrate

static:
	python manage.py collectstatic --noinput

run:
	python manage.py runserver


deploy:
	echo "Chua co"


startcelery:
	mkdir -p celery/log
	mkdir -p celery/pid
	celery -A uteoj worker -l INFO
	# celery multi start 3 -c:1-3 4 -Q:1 celery_queue1 -Q:2 celery_queue2 -Q:3 celery_queue3 -A uteoj --pidfile=./celery/pid/%n.txt --logfile=./celery/log/%n.txt

stopcelery:
	# celery multi stop 3 -Q:1 celery_queue1 -Q:2 celery_queue2 -Q:3 celery_queue3 -A uteoj --pidfile=./celery/pid/%n.txt --logfile=./celery/log/%n.txt
	ps auxww | grep 'celery worker' | awk '{print $$2}' | xargs kill -9

