-- migrate:up
CREATE TABLE IF NOT EXISTS public.bannedusernames
(
    id serial NOT NULL,
    username character varying COLLATE pg_catalog."default" NOT NULL,
    by integer NOT NULL,
    comment character varying COLLATE pg_catalog."default",
    CONSTRAINT bannedusernames_pkey PRIMARY KEY (id),
    CONSTRAINT bannedusernames_users_fkey FOREIGN KEY (by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

-- migrate:down
DROP TABLE IF EXISTS public.bannedusernames CASCADE;

