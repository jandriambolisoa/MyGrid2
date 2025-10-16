-- migrate:up
CREATE TABLE public.teams
(
    id serial NOT NULL,
    name character varying NOT NULL,
    color character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT teams_name_unique UNIQUE (name)
);

-- migrate:down
DROP TABLE public.teams CASCADE
