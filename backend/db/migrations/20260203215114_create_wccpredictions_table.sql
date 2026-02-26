-- migrate:up
CREATE TABLE public.wccpredictions
(
    user_id integer NOT NULL,
    championship_id integer NOT NULL,
    team_id integer NOT NULL,
    potential integer NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, championship_id),
    CONSTRAINT wccpredictions_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT wccpredictions_championships_fkey FOREIGN KEY (championship_id)
        REFERENCES public.championships (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT wccpredictions_teams_fkey FOREIGN KEY (team_id)
        REFERENCES public.teams (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.wccpredictions;
