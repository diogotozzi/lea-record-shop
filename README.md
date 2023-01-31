# Add user to 'docker' group
# sudo usermod -aG docker $(whoami)

# Delete all containers
# docker rm $(docker ps -a -q)

# Delete all images
# docker rmi $(docker images -q)

# --- Gitlab --- #

# docker build -t registry.gitlab.com/lea/lea/nginx:base-prod -f docker/nginx/Dockerfile-prod docker/nginx/. && docker push registry.gitlab.com/lea/lea/nginx:base-prod
# docker build -t registry.gitlab.com/lea/lea/php:base-prod -f docker/php/Dockerfile-prod docker/php/. && docker push registry.gitlab.com/lea/lea/php:base-prod


sanic server.app --dev

curl http://127.0.0.1:8000/discs
curl http://127.0.0.1:8000/disc/1
curl http://127.0.0.1:8000/disc --data '{"name":"A","artist":"Aa","lauched":"2023","style":"rock","quantity":"150"}'

curl http://127.0.0.1:8000/clients
curl http://127.0.0.1:8000/client/1
curl http://127.0.0.1:8000/client --data '{"name":"John Doe","document":"0001","birthdate":"12/31/2000","email":"john-doe@example.com","phone":"555-1234"}'
curl http://127.0.0.1:8000/client/1 --request "DELETE"

curl http://127.0.0.1:8000/order --data '{"client_id":"3","disc_id":"1","quantity":"1"}'