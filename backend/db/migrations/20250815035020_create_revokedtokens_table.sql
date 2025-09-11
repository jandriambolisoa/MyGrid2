-- migrate:up
CREATE TABLE IF NOT EXISTS public.revokedtokens
(
    token character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT revokedtokens_pkey PRIMARY KEY (token)
);

-- migrate:down
DROP TABLE IF EXISTS public.revokedtokens CASCADE;
