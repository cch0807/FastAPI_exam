import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.handler.rest.v1.segment import SegmentService
from app.handler.rest.v1.segment.dtos import (
    SegmentCreateDTO,
    SegmentPatchDTO,
    ParameterCreateDTO,
    SubSegmentCreateDTO,
)
from app.domain.segment import (
    Segment,
    Parameter,
    SubSegment,
    SegmentRepo,
    ParameterRepo,
    SubSegmentRepo,
)


@pytest.fixture(scope="session")
def segment_service():
    return SegmentService(
        segment_repo=SegmentRepo(),
        parameter_repo=ParameterRepo(),
        sub_seg_repo=SubSegmentRepo(),
    )


@pytest.fixture()
async def segments(session: AsyncSession):
    segment_list = [
        Segment(idx="1", name="test1", description="DESC1", status="Unchecked"),
        Segment(idx="2", name="test2", description="DESC2", status="Unchecked"),
    ]
    parameter_list = [
        Parameter(
            idx="1",
            segment=segment_list[0],
            name="param1",
            description="DESC1",
            type="type1",
            formula={"formula1": "formula1"},
        ),
        Parameter(
            idx="2",
            segment=segment_list[1],
            name="param2",
            description="DESC2",
            type="type2",
            formula={"formula2": "formula2"},
        ),
    ]
    subsegment_list = [
        SubSegment(
            idx="1",
            param1=parameter_list[0],
            param2=parameter_list[1],
            name="test1",
            description="DESC1",
        ),
        SubSegment(
            idx="2",
            param1=parameter_list[0],
            param2=parameter_list[1],
            name="test2",
            description="DESC2",
        ),
    ]

    await session.add_all(segment_list + parameter_list + subsegment_list)
    await session.flush()

    yield segment_list

    await session.delete(segment_list + parameter_list + subsegment_list)

    await session.flush()


async def read(segment_service: SegmentService, segments):
    results, cursor = await segment_service.read(cursor=0, size=10)
    assert len(results.datas) == 2


async def test_delete(segment_service: SegmentService, session: AsyncSession):
    segment = Segment(name="segment_to_delete")
    session.add(segment)
    await session.flush([segment])
    await session.refresh(segment)

    await segment_service.delete(segment)

    assert None is (
        await session.scalar(select(Segment).where(Segment.idx == segment.idx))
    )

async def test_update_status(segment_service: SegmentService, segments, session: AsyncSession):


# async def test_update_meta_data(api_service: APIService, apis, session: AsyncSession):
#     obj = await api_service.update_meta_data(
#         apis[0].idx,
#         api_object=APIPatchDTO(
#             name="newname", url="newurl", description="newdescription"
#         ),
#     )
#     assert obj.name == "newname"
#     assert obj.url == "newurl"
#     assert obj.description == "newdescription"