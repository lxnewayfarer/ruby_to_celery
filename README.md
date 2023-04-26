## Example of connection of Ruby with Python/Celery via RabbitMQ

Add message to RabbitMQ `requests` queue from Ruby script, then "heavy" process this message and return this message reversed to `responses` queue with `correlation_id`.

It allows to connect Ruby script with heavy Celery worker when it is required

### Up containers:
`docker-compose up -d`

### Run heavy RabbitMQ server:

`celery -A tasks worker --loglevel=INFO`

`python3 main.py`

### Check response:
`ruby try.rb`

RabbitMQ interface: http://localhost:15672/ 