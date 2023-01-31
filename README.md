
curl http://127.0.0.1/disc --data '{"name":"A","artist":"A","lauched":"2023","style":"rock","quantity":"10"}'
curl http://127.0.0.1/discs
curl http://127.0.0.1/disc/1
curl http://127.0.0.1/disc/1 --request "DELETE"

curl http://127.0.0.1/client --data '{"name":"John Doe","document":"0001","birthdate":"12/31/2000","email":"john-doe@example.com","phone":"555-1234"}'
curl http://127.0.0.1/clients
curl http://127.0.0.1/client/1
curl http://127.0.0.1/client/1 --request "DELETE"

curl http://127.0.0.1/order --data '{"client_id":"1","disc_id":"1","quantity":"1"}'