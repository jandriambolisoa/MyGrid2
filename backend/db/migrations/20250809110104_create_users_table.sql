-- migrate:up
CREATE TABLE public.users
(
    id serial NOT NULL,
    username citext NOT NULL,
    email citext NOT NULL,
    password character varying NOT NULL,
    created timestamp with time zone NOT NULL DEFAULT NOW(),
    modified timestamp with time zone NOT NULL DEFAULT NOW(),
    language character varying,
    image character varying,
    referralcode character varying NOT NULL,
    verified boolean NOT NULL DEFAULT false,
    PRIMARY KEY (id),
    CONSTRAINT users_email_unique UNIQUE (email),
    CONSTRAINT users_username_unique UNIQUE (username),
    CONSTRAINT users_referralcode_unique UNIQUE (referralcode)
);

-- migrate:down
DROP TABLE public.users CASCADE