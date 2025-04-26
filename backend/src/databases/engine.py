from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..config import settings

engine = create_async_engine(url=settings.DB, echo=True)
main_session = async_sessionmaker(bind=engine)
