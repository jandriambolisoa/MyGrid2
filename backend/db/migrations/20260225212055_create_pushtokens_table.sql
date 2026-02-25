-- migrate:up
CREATE TABLE public.pushtokens
(
    user_id integer NOT NULL,
    token character varying NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id),
    CONSTRAINT pushtokens_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.pushtokens;
