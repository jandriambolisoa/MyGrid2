-- migrate:up
CREATE TABLE IF NOT EXISTS public.refreshtokens
(
    user_id integer NOT NULL,
    token character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT refreshtokens_pkey PRIMARY KEY (token)
);

-- migrate:down
DROP TABLE IF EXISTS public.refreshtokens;
