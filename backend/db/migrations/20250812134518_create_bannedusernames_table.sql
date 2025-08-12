-- migrate:up
CREATE TABLE IF NOT EXISTS public.bannedusernames
(
    id integer NOT NULL DEFAULT nextval('bannedusernames_id_seq'::regclass),
    username character varying COLLATE pg_catalog."default" NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT now(),
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

