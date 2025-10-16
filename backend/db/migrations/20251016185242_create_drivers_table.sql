-- migrate:up
CREATE TABLE public.drivers
(
    id serial NOT NULL,
    firstname character varying NOT NULL,
    longname character varying NOT NULL,
    codename character varying NOT NULL,
    PRIMARY KEY (id)
);

-- migrate:down
DROP TABLE public.drivers CASCADE
