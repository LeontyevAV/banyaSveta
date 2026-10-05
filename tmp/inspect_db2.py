import asyncio
import asyncpg
import yaml

BASE = '/home/sasha/work/bots/banyaSveta'


async def main():
    with open(f'{BASE}/settings.yaml') as f:
        s = yaml.safe_load(f)
    p = None
    with open(f'{BASE}/.env') as f:
        for l in f:
            if l.strip().startswith('PG_PASSWORD'):
                p = l.split('=', 1)[1].strip().strip('"').strip("'")
                break

    conn = await asyncpg.connect(
        host=s['pg_host'], port=s['pg_port'],
        database=s['pg_database'], user=s['pg_username'], password=p,
    )

    enums = await conn.fetch(
        "select t.typname, e.enumlabel from pg_type t "
        "join pg_enum e on e.enumtypid=t.oid order by t.typname, e.enumsortorder"
    )
    print('ENUMS:')
    cur = None
    for r in enums:
        if r[0] != cur:
            cur = r[0]
            print(' ', cur, '=', end=' ')
        print(r[1], end=' ')
    print('\n')

    print('BOTS:')
    for r in await conn.fetch('select id, name, ext_bot_id from bots order by id'):
        print(f"  {r['id']}: {r['name']} (ext_bot_id={r['ext_bot_id']})")

    print('\nUSEREVENTTYPES:')
    for r in await conn.fetch('select id, name from usereventtypes order by id'):
        print(f"  {r['id']}: {r['name']}")

    print('\nEXTENSION:')
    for r in await conn.fetch("select extname from pg_extension order by extname"):
        print(' ', r[0])

    await conn.close()


asyncio.run(main())
