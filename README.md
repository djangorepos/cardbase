Credit Card base example

Deployment:
- git clone https://github.com/djangorepos/cardbase.git
- cd cardbase
- docker-compose up --build -d
- docker ps
- docker exec -it  </your container web/> python manage.py collectstatic --noinput
- docker exec -it  </your container web/> python manage.py makemigrations
- docker exec -it  </your container web/> python manage.py migrate
- docker-compose up