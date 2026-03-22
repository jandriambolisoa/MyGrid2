-- migrate:up
CREATE TABLE public.sessionsreactions
(
    user_id integer NOT NULL,
    session_id integer NOT NULL,
    by integer NOT NULL,
    reaction character varying NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, session_id, by),
    CONSTRAINT sessionsreactions_users_fkey1 FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionsreactions_sessions_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionsreactions_users_fkey2 FOREIGN KEY (by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.sessionsreactions;
