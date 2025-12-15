-- migrate:up
CREATE TABLE public.userobligations
(
    id serial NOT NULL,
    user_id integer NOT NULL,
    obligation character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT userobligations_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.userobligations CASCADE
