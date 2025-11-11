-- migrate:up
CREATE TABLE public.scores
(
    user_id integer NOT NULL,
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    score integer NOT NULL,
    PRIMARY KEY (user_id, session_id, driver_id),
    CONSTRAINT scores_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT scores_sessions_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT scores_drivers_fkey FOREIGN KEY (driver_id)
        REFERENCES public.drivers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.scores CASCADE
