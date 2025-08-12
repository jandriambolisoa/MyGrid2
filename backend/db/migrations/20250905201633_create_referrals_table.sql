-- migrate:up
CREATE TABLE public.referrals
(
    user_id integer NOT NULL,
    referral integer NOT NULL,
    PRIMARY KEY (user_id),
    CONSTRAINT referrals_users_fkey1 FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT referrals_users_fkey2 FOREIGN KEY (referral)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.referrals;
