-- migrate:up
CREATE TABLE public.eventstranslations
(
    event_id integer NOT NULL,
    language character varying NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (event_id, language),
    CONSTRAINT eventstranslations_events_fkey FOREIGN KEY (event_id)
        REFERENCES public.events (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.eventstranslations CASCADE
