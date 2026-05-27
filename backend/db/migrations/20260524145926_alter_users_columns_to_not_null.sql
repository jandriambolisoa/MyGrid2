-- migrate:up
ALTER TABLE IF EXISTS public.users
    ALTER COLUMN email DROP NOT NULL;

ALTER TABLE IF EXISTS public.users
    ALTER COLUMN password DROP NOT NULL;

-- migrate:down
ALTER TABLE IF EXISTS public.users
    ALTER COLUMN email SET NOT NULL;

ALTER TABLE IF EXISTS public.users
    ALTER COLUMN password SET NOT NULL;
