import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.segment import Segment, SegmentRepo


@pytest.fixture("session")
def segments_repository():
    return SegmentRepo()


@pytest.fixture()
async def segments(session: AsyncSession):
    segment_list = [
        Segment(name="test1", description="DESC1", status="Requested"),
        Segment(name="test2", description="DESC2", status="Requested"),
    ]
    await session.flush()
    yield segment_list
    await session.delete(segment_list[0])
    await session.delete(segment_list[1])


async def test_repository_retrieve_for_pagenation(
    session, segment_repository: SegmentRepo, segments
):
    results, cursor = await segment_repository.retrieve_for_pagenation(
        size=10, cursor=0
    )
    assert len(results) == 2
    with pytest.raises(Exception):
        results[0].parameter


# async def test_repository_retrive_for_pagenation(
#   session, segment_repository: SegmentRepo, segments
# ):
#   results, cursor = await segment_repository.retrieve_for_

# @pytest.mark.skip
# def test_repository_retrive_with_name(session, segment_repository):
#   segments = segment_repository.retrieve_with_name(name="test1")
