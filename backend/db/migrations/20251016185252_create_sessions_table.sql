-- migrate:up
CREATE TABLE public.sessions
(
    id serial NOT NULL,
    name character varying NOT NULL,
    datetime timestamp with time zone NOT NULL,
    event_id integer NOT NULL,
    competitive boolean NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (name, event_id),
    CONSTRAINT sessions_events_fkey FOREIGN KEY (event_id)
        REFERENCES public.events (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.sessions CASCADE
