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
        host=s['pg_host'],
        port=s['pg_port'],
        database=s['pg_database'],
        user=s['pg_username'],
        password=p,
    )

    tables = await conn.fetch(
        "select table_name from information_schema.tables "
        "where table_schema='public' and table_type='BASE TABLE' order by table_name"
    )
    seqs = await conn.fetch(
        "select sequence_name from information_schema.sequences "
        "where sequence_schema='public' order by sequence_name"
    )

    print('SEQUENCES:', ', '.join(r[0] for r in seqs) or '-')
    print()

    for t in tables:
        tn = t[0]
        print('=' * 60)
        print('TABLE:', tn)
        cols = await conn.fetch(
            "select column_name, data_type, is_nullable, column_default "
            "from information_schema.columns "
            "where table_schema='public' and table_name=$1 order by ordinal_position",
            tn,
        )
        for c in cols:
            print(f"  {c[0]:28} {c[1]:18} {'NULL' if c[2] == 'YES' else 'NOT NULL':8} {c[3] or ''}")

        pk = await conn.fetch(
            "select a.attname from pg_index i "
            "join pg_attribute a on a.attrelid=i.indrelid and a.attnum = any(i.indkey) "
            "where i.indrelid=($1)::regclass and i.indisprimary",
            tn,
        )
        if pk:
            print('  PK:', ', '.join(r[0] for r in pk))

        fks = await conn.fetch(
            "select conname, pg_get_constraintdef(c.oid) from pg_constraint c "
            "where c.conrelid=($1)::regclass and c.contype='f' order by conname",
            tn,
        )
        for fk in fks:
            print('  FK:', fk[0], '->', fk[1])

        idx = await conn.fetch(
            "select indexname, indexdef from pg_indexes "
            "where schemaname='public' and tablename=$1 order by indexname",
            tn,
        )
        for ix in idx:
            print('  IDX:', ix[0])

        cnt = await conn.fetchval(f'select count(*) from "{tn}"')
        print('  ROWS:', cnt)
        print()

    # Показать несколько строк из каждой таблицы (первые 3)
    print('=' * 60)
    print('SAMPLE DATA')
    for t in tables:
        tn = t[0]
        rows = await conn.fetch(f'select * from "{tn}" limit 3')
        print(f'--- {tn} ---')
        for r in rows:
            print('  ', dict(r))
        print()

    await conn.close()


asyncio.run(main())
