-- migrate:up
CREATE TABLE public.premiumhistory
(
    id serial NOT NULL,
    user_id integer NOT NULL,
    premium boolean NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT premiumhistory_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.premiumhistory CASCADE
