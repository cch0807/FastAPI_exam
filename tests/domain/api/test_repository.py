import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.api import API, APIRepository


@pytest.fixture(scope="session")
def api_repository():
    return APIRepository()


@pytest.fixture()
async def apis(session: AsyncSession):
    api_list = [
        API(name="test1", description="DESC1"),
        API(name="test2", description="DESC2"),
    ]
    session.add_all(api_list)
    await session.flush()
    yield api_list
    await session.delete(api_list[0])
    await session.delete(api_list[1])


async def test_repository_retrive_for_pagination(
    session, api_repository: APIRepository, apis
):
    results, cursor = await api_repository.retrieve_for_pagination(
        name="", size=10, cursor=0
    )

    assert len(results) == 2
    with pytest.raises(Exception):
        results[0].fields


async def test_repository_retrieve_for_pagination_returning_no_data(
    session, api_repository: APIRepository, apis
):
    results, cursor = await api_repository.retrieve_for_pagination(
        name="!@#@$#&%(*)$!@)*&%#_)$$(@_%_)IMPOSSIBLE_NAME", size=10, cursor=0
    )

    assert len(results) == 0
    assert cursor == 0
    with pytest.raises(Exception):
        results[0].fields


async def test_repository_retrive_for_pagination_with_name(
    session, api_repository: APIRepository, apis
):
    results, cursor = await api_repository.retrieve_for_pagination(
        name="test1", size=10, cursor=0
    )

    assert len(results) == 1
    assert results[0].name == "test1"
    with pytest.raises(Exception):
        results[0].fields
