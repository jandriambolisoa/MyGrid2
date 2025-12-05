-- migrate:up
CREATE TABLE public.championships
(
    id serial NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT championships_name_unique UNIQUE (name)
);

-- migrate:down
DROP TABLE public.championships CASCADE
