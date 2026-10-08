do $$
declare
    r record;
begin
    for r in
        select * from (values
            ('_files', 'createdAt', 'created_at'),
            ('_files', 'updatedAt', 'updated_at'),
            ('_files', 'extid', 'ext_id'),
            ('_session', 'userTelegramId', 'user_telegram_id'),
            ('_session', 'createdAt', 'created_at'),
            ('posts', 'createdAt', 'created_at'),
            ('posts', 'updatedAt', 'updated_at'),
            ('userevents', 'createdAt', 'created_at'),
            ('userevents', 'updatedAt', 'updated_at'),
            ('userevents', 'extid', 'ext_id'),
            ('users', 'passwordHash', 'password_hash'),
            ('users', 'createdAt', 'created_at'),
            ('users', 'updatedAt', 'updated_at'),
            ('users', 'lastname', 'last_name'),
            ('users', 'sexid', 'sex_id'),
            ('users', 'refreshtoken', 'refresh_token'),
            ('users', 'avatarid', 'avatar_id'),
            ('userstelegram', 'createdAt', 'created_at'),
            ('userstelegram', 'updatedAt', 'updated_at')
        ) as t(tbl, old_name, new_name)
    loop
        if exists (
            select 1 from information_schema.columns
            where table_schema = 'public'
              and table_name = r.tbl
              and column_name = r.old_name
        ) and not exists (
            select 1 from information_schema.columns
            where table_schema = 'public'
              and table_name = r.tbl
              and column_name = r.new_name
        ) then
            execute format(
                'alter table %I rename column %I to %I',
                r.tbl, r.old_name, r.new_name
            );
        end if;
    end loop;
end $$;
