-- migrate:up
CREATE TABLE public.userscollectibles
(
    user_id integer NOT NULL,
    collectible_id integer NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    views integer NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, collectible_id),
    CONSTRAINT userscollectibles_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT userscollectibles_collectibles_fkey FOREIGN KEY (collectible_id)
        REFERENCES public.collectibles (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.userscollectibles;
