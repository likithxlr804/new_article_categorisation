from celery import Celery
import redis
print(redis.Redis)  # This should not raise any error


# Configure the Celery app with Redis as the broker
app = Celery('tasks', broker='redis://localhost:6379/0')

# Set the result backend to Redis as well
app.conf.result_backend = 'redis://localhost:6379/0'
