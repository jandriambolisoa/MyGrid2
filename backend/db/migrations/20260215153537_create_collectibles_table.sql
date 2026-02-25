-- migrate:up
CREATE TABLE public.collectibles
(
    id serial NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT collectibles_name_unique UNIQUE (name)
);

-- migrate:down
DROP TABLE IF EXISTS public.collectibles;
