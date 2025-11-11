-- migrate:up
CREATE TABLE public.sessionspredictions
(
    session_id integer NOT NULL,
    user_id integer NOT NULL,
    driver_id integer NOT NULL,
    mygrid integer NOT NULL,
    potential integer NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (session_id, user_id, driver_id),
    UNIQUE (session_id, mygrid),
    CONSTRAINT sessionspredictions_sessions_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionspredictions_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionspredictions_drivers_fkey FOREIGN KEY (driver_id)
        REFERENCES public.drivers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.sessionspredictions CASCADE
