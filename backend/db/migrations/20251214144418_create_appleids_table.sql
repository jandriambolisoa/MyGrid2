-- migrate:up
CREATE TABLE public.appleids
(
    user_id integer NOT NULL,
    apple_id character varying NOT NULL,
    PRIMARY KEY (user_id),
    CONSTRAINT appleids_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.appleids;
