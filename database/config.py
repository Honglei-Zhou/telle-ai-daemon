username = 'postgres'
password = 'cognitiveati'
host = 'telle-ai-database.cqh3eh5shl0r.us-east-2.rds.amazonaws.com'
port = 5432
prod_db = 'telle_ai_prod'

db_string = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(username, password, host, port, prod_db)

ipinfo_access_token = '362e2dc65c9e7a'

redis_host = 'telle-redis.telle.production'
# redis_host = 'redis'
redis_port = 6379

thread_number = 20
