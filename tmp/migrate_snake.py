import asyncio
import sys
import asyncpg
import yaml

BASE = '/home/sasha/work/bots/banyaSveta'

RENAMES = {
    '_files': [('createdAt', 'created_at'), ('updatedAt', 'updated_at'), ('extid', 'ext_id')],
    '_session': [('userTelegramId', 'user_telegram_id'), ('createdAt', 'created_at')],
    'posts': [('createdAt', 'created_at'), ('updatedAt', 'updated_at')],
    'userevents': [('createdAt', 'created_at'), ('updatedAt', 'updated_at'), ('extid', 'ext_id')],
    'users': [
        ('passwordHash', 'password_hash'),
        ('createdAt', 'created_at'),
        ('updatedAt', 'updated_at'),
        ('lastname', 'last_name'),
        ('sexid', 'sex_id'),
        ('refreshtoken', 'refresh_token'),
        ('avatarid', 'avatar_id'),
    ],
    'userstelegram': [('createdAt', 'created_at'), ('updatedAt', 'updated_at')],
}


async def main():
    apply = '--apply' in sys.argv

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

    class DryRun(Exception):
        pass

    print('MODE:', 'APPLY' if apply else 'DRY-RUN')
    try:
        async with conn.transaction():
            for table, cols in RENAMES.items():
                existing = {
                    r['column_name']
                    for r in await conn.fetch(
                        "select column_name from information_schema.columns "
                        "where table_schema='public' and table_name=$1",
                        table,
                    )
                }
                for old, new in cols:
                    if old not in existing:
                        print(f'  skip {table}.{old} (already renamed?)')
                        continue
                    if new in existing:
                        print(f'  SKIP {table}.{old} -> {new}: target already exists')
                        continue
                    sql = f'ALTER TABLE "{table}" RENAME COLUMN "{old}" TO "{new}"'
                    print('  SQL:', sql)
                    if apply:
                        await conn.execute(sql)
            if not apply:
                raise DryRun()
    except DryRun:
        pass

    print('DONE' if apply else 'DRY-RUN rolled back (nothing changed)')
    await conn.close()


asyncio.run(main())
