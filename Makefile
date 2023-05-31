up:
	docker-compose build
	docker-compose up

start:
	docker-compose up

down:
	docker-compose down

ps:
	docker-compose ps

shell:
	docker-compose exec fast-todo ash

test:
	docker-compose exec fast-todo ash -c "python -m pytest src/tests/"

tailwind:
	docker-compose exec fast-todo ash -c "cd src/tailwindcss && npx tailwindcss -i ./styles/app.css -o ../static/css/tailwind.css --watch"

restart: down up