-- migrate:up
CREATE TABLE public.events
(
    id serial NOT NULL,
    name character varying NOT NULL,
    color character varying[] NOT NULL,
    flag character varying NOT NULL,
    championship_id integer NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (championship_id, name),
    CONSTRAINT events_championships_fkey FOREIGN KEY (championship_id)
        REFERENCES public.championships (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.events CASCADE
