-- migrate:up
CREATE TABLE public.leaguesinvites
(
    league_id integer NOT NULL,
    code character varying NOT NULL,
    password character varying,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    exp timestamp with time zone NOT NULL DEFAULT NOW() + interval '1 hour',
    PRIMARY KEY (code),
    CONSTRAINT leaguesinvites_leagues_fkey FOREIGN KEY (league_id)
        REFERENCES public.leagues (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.leaguesusers;
