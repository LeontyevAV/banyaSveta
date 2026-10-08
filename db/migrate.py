import asyncio
import sys
from pathlib import Path

import asyncpg

from config import settings

MIGRATIONS_DIR = Path(__file__).resolve().parent / 'migrations'
MIGRATIONS_TABLE = '_migrations'


async def ensure_migrations_table(conn: asyncpg.Connection) -> None:
    await conn.execute(
        f"""
        create table if not exists {MIGRATIONS_TABLE} (
            name text primary key,
            applied_at timestamptz not null default now()
        )
        """
    )


def discover_migrations() -> list[Path]:
    if not MIGRATIONS_DIR.exists():
        return []
    return sorted(MIGRATIONS_DIR.glob('*.sql'), key=lambda p: p.name)


async def get_applied(conn: asyncpg.Connection) -> set[str]:
    rows = await conn.fetch(f'select name from {MIGRATIONS_TABLE}')
    return {r['name'] for r in rows}


async def get_pending(conn: asyncpg.Connection) -> list[Path]:
    applied = await get_applied(conn)
    return [m for m in discover_migrations() if m.name not in applied]


async def apply_migrations(
    conn: asyncpg.Connection,
    *,
    dry_run: bool = False,
) -> list[str]:
    await ensure_migrations_table(conn)
    pending = await get_pending(conn)
    applied_now: list[str] = []
    for path in pending:
        if dry_run:
            applied_now.append(path.name)
            continue
        sql = path.read_text(encoding='utf-8')
        async with conn.transaction():
            await conn.execute(sql)
            await conn.execute(
                f'insert into {MIGRATIONS_TABLE} (name) values ($1)',
                path.name,
            )
        applied_now.append(path.name)
    return applied_now


async def _connect() -> asyncpg.Connection:
    return await asyncpg.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_username,
        password=settings.pg_password,
    )


async def _cmd_status() -> None:
    conn = await _connect()
    try:
        await ensure_migrations_table(conn)
        applied = await get_applied(conn)
        migrations = discover_migrations()
        if not migrations:
            print('Миграций не найдено.')
            return
        for path in migrations:
            mark = 'applied' if path.name in applied else 'pending'
            print(f'  [{mark}] {path.name}')
    finally:
        await conn.close()


async def _cmd_apply(dry_run: bool) -> None:
    conn = await _connect()
    try:
        applied = await apply_migrations(conn, dry_run=dry_run)
    finally:
        await conn.close()
    if not applied:
        print('Нет новых миграций.')
        return
    print('Будут применены:' if dry_run else 'Применены:')
    for name in applied:
        print('  ', name)


def main() -> None:
    args = sys.argv[1:]
    dry_run = '--dry-run' in args
    command = next((a for a in args if not a.startswith('-')), 'apply')
    if command == 'status':
        asyncio.run(_cmd_status())
    elif command == 'apply':
        asyncio.run(_cmd_apply(dry_run))
    else:
        print('Использование: python -m db.migrate [apply|status] [--dry-run]')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
