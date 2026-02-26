-- migrate:up
CREATE TABLE public.wdcpredictions
(
    user_id integer NOT NULL,
    championship_id integer NOT NULL,
    driver_id integer NOT NULL,
    potential integer NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, championship_id),
    CONSTRAINT wdcpredictions_users_fkey FOREIGN KEY (user_id)
        REFERENCES public.users (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT wdcpredictions_championships_fkey FOREIGN KEY (championship_id)
        REFERENCES public.championships (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    CONSTRAINT wdcpredictions_drivers_fkey FOREIGN KEY (driver_id)
        REFERENCES public.drivers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE IF EXISTS public.wdcpredictions;
