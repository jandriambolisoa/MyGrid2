-- migrate:up
CREATE TABLE public.lostpw
(
    user_id integer NOT NULL,
    password character varying NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id),
    CONSTRAINT lostpw_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.lostpw;
