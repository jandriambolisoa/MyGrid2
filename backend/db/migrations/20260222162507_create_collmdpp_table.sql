-- migrate:up
CREATE TABLE public.coll_multiple_drivers_perfect_prediction
(
    id serial NOT NULL,
    collectible_id integer NOT NULL,
    drivers_id integer[] NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT collmdpp_collectibles_fkey FOREIGN KEY (collectible_id)
        REFERENCES public.collectibles (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);


-- migrate:down
DROP TABLE IF EXISTS public.coll_multiple_drivers_perfect_prediction;
