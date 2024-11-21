from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.config import Config

# Create engine
engine = create_engine(
    Config.DATABASE_URL, 
    echo=Config.FLASK_DEBUG,
    pool_pre_ping=True,  # Test connection before using
    pool_recycle=3600    # Recycle connections after 1 hour
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a thread-local session factory
db_session = scoped_session(SessionLocal)

def get_db():
    """
    Dependency that creates a new database session for each request
    and closes it after the request is complete
    """
    db = db_session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initialize the database - create all tables
    """
    from app.models.user import Base as UserBase
    from app.models.employee import Base as EmployeeBase
    
    UserBase.metadata.create_all(bind=engine)
    EmployeeBase.metadata.create_all(bind=engine)