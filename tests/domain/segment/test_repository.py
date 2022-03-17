import pytest

from app.domain.segment import Segment, SegmentRepo


@pytest.fixture("session")
def segments_repository():
    return SegmentRepo()


@pytest.fixture()
async def segments(session):
    segment_list = []
    session.add_all(segment_list)
    yield
    session.remove(segment_list)

# @pytest.mark.skip
# def test_repository_retrive_with_name(session, segment_repository):
#   segments = segment_repository.retrieve_with_name(name="test1")
