-- migrate:up
CREATE TABLE public.teams
(
    id serial NOT NULL,
    name character varying NOT NULL,
    color character varying NOT NULL,
    PRIMARY KEY (id)
);

-- migrate:down
DROP TABLE public.teams CASCADE
