-- migrate:up
CREATE TABLE public.sessionstranslations
(
    session_id integer NOT NULL,
    language character varying NOT NULL,
    name character varying NOT NULL,
    PRIMARY KEY (session_id, language),
    CONSTRAINT sessionstranslations_session_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.sessionstranslations CASCADE
