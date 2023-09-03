from src.config import settings

DATABASE_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': settings.DB_HOST,
                'port': settings.DB_PORT,
                'user': settings.DB_USER,
                'password': settings.DB_PASSWORD,
                'database': settings.DB_NAME,
            }
        }
    },
    "apps": {
        "models": {
            "models": ["aerich.models", "src.auth.models"],
            "default_connection": "default",
        },
    },
}
