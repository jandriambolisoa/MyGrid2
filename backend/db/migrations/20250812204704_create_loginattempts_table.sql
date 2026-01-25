-- migrate:up
CREATE TABLE IF NOT EXISTS public.loginattempts
(
    address character varying COLLATE pg_catalog."default" NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT loginattempts_pkey PRIMARY KEY (address, created)
);

-- migrate:down
DROP TABLE IF EXISTS public.loginattempts CASCADE;
