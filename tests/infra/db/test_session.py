from app.infra.db.conn import session


async def test_inject_session():
    from app.infra.db.conn import inject_session

    @inject_session
    async def hi():
        return await session.scalar("SELECT 1")

    func_return = await hi()

    assert func_return == 1
