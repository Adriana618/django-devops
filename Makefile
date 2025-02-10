ENV_PATH = ./secure_doc_analyzer/.env

include $(ENV_PATH)
export $(shell sed 's/=.*//' $(ENV_PATH))


up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f