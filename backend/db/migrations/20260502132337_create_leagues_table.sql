-- migrate:up
CREATE TABLE public.leagues
(
    id serial NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    colors character varying[] NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id)
);

-- migrate:down
DROP TABLE IF EXISTS public.leagues;
