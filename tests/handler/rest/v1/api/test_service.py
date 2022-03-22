import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.domain.api import API, APIField, APIFieldRepository, APIRepository
from app.handler.rest.v1.api import APIService
from app.handler.rest.v1.api.dto import APICreateDTO, APIFieldCreateDTO, APIPatchDTO


@pytest.fixture(scope="session")
def api_service():
    return APIService(api_field_repo=APIFieldRepository(), api_repo=APIRepository())


@pytest.fixture()
async def apis(session: AsyncSession):
    api_list = [
        API(name="test1", description="DESC1", url="url"),
        API(name="test2", description="DESC2", url="url"),
    ]
    api_field_list = [
        APIField(
            api=api_list[0],
            name="field1",
            description="field_desc1",
            type="field_type1",
        ),
        APIField(
            api=api_list[1],
            name="field2",
            description="field_desc2",
            type="field_type2",
        ),
    ]
    session.add_all(api_list + api_field_list)
    await session.flush()

    yield api_list

    for obj in api_list + api_field_list:
        session.delete(obj)
    await session.flush()


async def test_get_one_api(api_service: APIService, apis):
    idx = apis[0].idx
    result = await api_service.get_one(idx)

    assert apis[0].idx == result.id
    assert apis[0].name == result.name
    assert apis[0].description == result.description


async def test_get_one_api_not_found(api_service: APIService, apis):
    with pytest.raises(HTTPException) as exc:
        await api_service.get_one(2_147_483_647)
        assert exc.status_code == 404


async def test_get_api_list_all(api_service: APIService, apis):
    results = await api_service.retrieve(name="", cursor=0, size=10)
    assert len(results.datas) == 2
    for result, testdata in zip(results.datas, apis):
        assert result.name == testdata.name
        assert result.description == testdata.description


async def test_search_api_with_name(api_service: APIService, apis):
    results = await api_service.retrieve(name="test1", cursor=0, size=10)
    assert len(results.datas) == 1
    for result, testdata in zip(results.datas, apis):
        assert result.name == testdata.name
        assert result.description == testdata.description


async def test_create_api(api_service: APIService, session: AsyncSession):
    data = await api_service.create(
        APICreateDTO(
            name="test",
            url="url",
            fields=[APIFieldCreateDTO(name="field", type="type")],
        )
    )

    obj: API = await session.scalar(
        select(API)
        .where(API.idx == data.id, API.name == data.name, API.url == data.url)
        .options(joinedload(API.fields))
    )
    session.delete(obj.fields[0])
    session.delete(obj)
    await session.flush()
    assert obj.fields[0].name == "field"
    assert obj.fields[0].type == "type"


async def test_update_meta_data(api_service: APIService, apis, session: AsyncSession):
    obj = await api_service.update_meta_data(
        apis[0].idx,
        api_object=APIPatchDTO(
            name="newname", url="newurl", description="newdescription"
        ),
    )
    assert obj.name == "newname"
    assert obj.url == "newurl"
    assert obj.description == "newdescription"


async def test_delete(api_service: APIService, session: AsyncSession):
    api = API(name="api_to_delete")
    session.add(api)
    await session.flush([api])
    await session.refresh(api)

    await api_service.delete(api)
    assert None is (await session.scalar(select(API).where(API.idx == api.idx)))
