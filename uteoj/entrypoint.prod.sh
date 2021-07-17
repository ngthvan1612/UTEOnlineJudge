while ! python manage.py sqlflush > /dev/null 2>&1 ;do
  echo "Waiting for the db to be ready."
  sleep 1
done