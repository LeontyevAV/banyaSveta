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

    print('=== camelCase / mixed-case columns ===')
    rows = await conn.fetch(
        "select table_name, column_name from information_schema.columns "
        "where table_schema='public' and column_name <> lower(column_name) "
        "order by table_name, ordinal_position"
    )
    for r in rows:
        print(f"  {r[0]}.{r[1]}")

    print('\n=== non-snake lowercase columns (no underscore, multiword candidates) ===')
    rows = await conn.fetch(
        "select table_name, column_name from information_schema.columns "
        "where table_schema='public' and column_name = lower(column_name) "
        "and column_name ~ '^[a-z]+(id|name|token)$' "
        "order by table_name"
    )
    for r in rows:
        print(f"  {r[0]}.{r[1]}")

    print('\n=== VIEWS ===')
    for r in await conn.fetch("select table_name, view_definition from information_schema.views where table_schema='public'"):
        print(' ', r[0])
        print('   ', (r[1] or '').replace('\n', ' ')[:300])

    print('\n=== FUNCTIONS / PROCEDURES (public) ===')
    for r in await conn.fetch(
        "select p.proname, pg_get_functiondef(p.oid) as def from pg_proc p "
        "join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' order by p.proname"
    ):
        d = (r[1] or '').replace('\n', ' ')
        hit = any(k in d for k in ('createdAt', 'updatedAt', 'userTelegramId', 'passwordHash'))
        print(f"  {r[0]}  {'<-- references camelCase!' if hit else ''}")

    print('\n=== TRIGGERS ===')
    for r in await conn.fetch(
        "select event_object_table, trigger_name, action_statement from information_schema.triggers "
        "where trigger_schema='public' order by event_object_table"
    ):
        d = (r[2] or '').replace('\n', ' ')
        hit = any(k in d for k in ('createdAt', 'updatedAt', 'userTelegramId', 'passwordHash'))
        print(f"  {r[0]}.{r[1]}  {'<-- references camelCase!' if hit else ''}")

    await conn.close()


asyncio.run(main())
