-- migrate:up
CREATE TABLE public.bannedhistory
(
    id serial NOT NULL,
    user_id integer NOT NULL,
    banned boolean NOT NULL,
    by integer NOT NULL,
    reason character varying NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id),
    CONSTRAINT bannedhistory_users_fkey1 FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT bannedhistory_users_fkey2 FOREIGN KEY (by)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.bannedhistory CASCADE
