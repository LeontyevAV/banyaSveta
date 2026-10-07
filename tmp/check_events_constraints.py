import asyncio
import sys

sys.path.insert(0, '/home/leontyevav/work/bots/banyaSveta')

from db import close_pool, get_pool, init_pool  # noqa: E402


async def main():
    await init_pool()
    pool = get_pool()
    print('--- constraints ---')
    rows = await pool.fetch(
        "select conname, pg_get_constraintdef(oid) as def "
        "from pg_constraint where conrelid='userevents'::regclass",
    )
    for r in rows:
        print(' ', r['conname'], '::', r['def'])
    print('--- indexes ---')
    rows = await pool.fetch(
        "select indexname, indexdef from pg_indexes "
        "where tablename='userevents'",
    )
    for r in rows:
        print(' ', r['indexname'], '::', r['indexdef'])
    await close_pool()


asyncio.run(main())
