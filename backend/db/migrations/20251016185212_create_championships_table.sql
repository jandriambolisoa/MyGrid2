-- migrate:up
CREATE TABLE public.championships
(
    id serial NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (id)
);

-- migrate:down
DROP TABLE public.championships CASCADE
