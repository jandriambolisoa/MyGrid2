-- migrate:up
CREATE TABLE public.sessionsresults
(
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    result integer NOT NULL,
    points numeric NOT NULL DEFAULT 0,
    PRIMARY KEY (session_id, driver_id),
    CONSTRAINT sessionsresults_sessions_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionsresults_drivers_fkey FOREIGN KEY (driver_id)
        REFERENCES public.drivers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.sessionsresults CASCADE
