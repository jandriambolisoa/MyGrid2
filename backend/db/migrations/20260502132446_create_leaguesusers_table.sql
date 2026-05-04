-- migrate:up
CREATE TABLE public.leaguesusers
(
    league_id integer NOT NULL,
    user_id integer NOT NULL,
    organizer boolean NOT NULL DEFAULT false,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (league_id, user_id),
    CONSTRAINT leaguesusers_leagues_fkey FOREIGN KEY (league_id)
        REFERENCES public.leagues (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT leaguesusers_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.leaguesusers;
