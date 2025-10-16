-- migrate:up
CREATE TABLE public.sessionsregistrations
(
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    team_id integer NOT NULL,
    prediction integer NOT NULL,
    PRIMARY KEY (session_id, driver_id),
    CONSTRAINT sessionsregistrations_sessions_fkey FOREIGN KEY (session_id)
        REFERENCES public.sessions (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionsregistrations_drivers_fkey FOREIGN KEY (driver_id)
        REFERENCES public.drivers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT sessionsregistrations_teams_fkey FOREIGN KEY (team_id)
        REFERENCES public.teams (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.sessionsregistrations CASCADE
