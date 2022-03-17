# TODO: 파일 이름을 변경하고, pytest가 가져오는 파일에 포함하도록 설정할 것
import pytest
from pytest import FixtureRequest, MonkeyPatch
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import create_database, database_exists, drop_database

from app.domain._base import BaseEntity
from app.infra import db

TEST_DB_URI = "postgresql+psycopg2://postgres:postgres@db/test"
ASYNC_TEST_DB_URI = "postgresql+asyncpg://postgres:postgres@db/test"


@pytest.fixture(scope="session")
def prepare_database():
    """테스트용 데이터베이스 생성 및 스키마 생성."""
    if not database_exists(TEST_DB_URI):
        create_database(TEST_DB_URI)

    _engine = create_engine(TEST_DB_URI)
    BaseEntity.metadata.create_all(bind=_engine, checkfirst=False)

    yield
    drop_database(TEST_DB_URI)


# TODO: autouse를 끄고, 데이터베이스 모킹이 되지 않았을 때 테스트가 실패하는 fixture를 추가
@pytest.fixture(scope="function", autouse=True)
async def engine(prepare_database, monkeypatch: MonkeyPatch, request: FixtureRequest):
    mock_engine = create_async_engine(ASYNC_TEST_DB_URI)
    monkeypatch.setattr(db, "engine", mock_engine)
    return mock_engine


@pytest.fixture(scope="function")
def session(engine, request: FixtureRequest, monkeypatch: MonkeyPatch):
    """테스트 데이터 생성을 위한 모킹된 세션"""

    def mocked_scopefunc():
        return request.node.name

    mock_session = async_scoped_session(
        sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=False,
            class_=AsyncSession,
        ),
        scopefunc=mocked_scopefunc,
    )
    monkeypatch.setattr(db, "session", mock_session)
    return mock_session


async def test_db_mocking(session: AsyncSession):
    assert "test" == await session.scalar("SELECT current_database()")
