-- migrate:up
CREATE TABLE public.promotedhistory
(
    id serial NOT NULL,
    user_id integer NOT NULL,
    moderator boolean NOT NULL,
    admin boolean NOT NULL,
    by integer NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT promotedhistory_users_fkey1 FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT promotedhistory_users_fkey2 FOREIGN KEY (by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.promotedhistory CASCADE
