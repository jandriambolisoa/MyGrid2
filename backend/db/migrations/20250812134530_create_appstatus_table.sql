-- migrate:up
CREATE TABLE IF NOT EXISTS public.appstatus
(
    id serial NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT now(),
    version character varying COLLATE pg_catalog."default" NOT NULL,
    maintenance boolean NOT NULL DEFAULT false,
    notes character varying COLLATE pg_catalog."default",
    CONSTRAINT appstatus_pkey PRIMARY KEY (id)
)

-- migrate:down
DROP TABLE IF EXISTS public.appstatus CASCADE;
