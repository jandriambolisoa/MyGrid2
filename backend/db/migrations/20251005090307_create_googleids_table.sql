-- migrate:up
CREATE TABLE public.googleids
(
    user_id integer NOT NULL,
    google_id bigint NOT NULL,
    PRIMARY KEY (user_id),
    CONSTRAINT googleids_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.googleids;
