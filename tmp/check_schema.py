import asyncio
import sys

sys.path.insert(0, '/home/leontyevav/work/bots/banyaSveta')

from db import close_pool, get_pool, init_pool  # noqa: E402

TABLES = ('userstelegram', 'userevents', 'usereventtypes', 'bots')


async def main():
    await init_pool()
    pool = get_pool()
    for table in TABLES:
        cols = await pool.fetch(
            'select column_name, data_type from information_schema.columns '
            "where table_schema='public' and table_name=$1 order by ordinal_position",
            table,
        )
        print(f'--- {table} ---')
        for c in cols:
            print(f'  {c["column_name"]:28} {c["data_type"]}')
        print()


asyncio.run(main())
