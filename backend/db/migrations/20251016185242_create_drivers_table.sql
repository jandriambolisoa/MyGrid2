-- migrate:up
CREATE TABLE public.drivers
(
    id serial NOT NULL,
    firstname character varying NOT NULL,
    lastname character varying NOT NULL,
    codename character varying NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT drivers_name_unique UNIQUE (firstname, lastname)
);

-- migrate:down
DROP TABLE public.drivers CASCADE
