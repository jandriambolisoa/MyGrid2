-- migrate:up
CREATE TABLE public.scoresparameters
(
    championship_id integer NOT NULL,
    param character varying NOT NULL,
    value0 integer NOT NULL DEFAULT 0,
    value1 integer NOT NULL DEFAULT 0,
    value2 integer NOT NULL DEFAULT 0,
    PRIMARY KEY (param, championship_id),
    CONSTRAINT scoresparameters FOREIGN KEY (championship_id)
        REFERENCES public.championships (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

-- migrate:down
DROP TABLE public.scoresparameters CASCADE
