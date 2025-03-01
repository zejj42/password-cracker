from app.db.persistence import PersistenceLayer
from app.db.redis_persistence import RedisPersistence


def get_persistence() -> PersistenceLayer:
    return RedisPersistence()
