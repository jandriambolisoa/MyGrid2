\restrict oxliJAPtW600MgzTwlv6eZcydCmd0P7ipDIlyw2a7HJoVZCNJ8bJvY0cLoUxc8G

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: citext; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS citext WITH SCHEMA public;


--
-- Name: EXTENSION citext; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION citext IS 'data type for case-insensitive character strings';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: appleids; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appleids (
    user_id integer NOT NULL,
    apple_id character varying NOT NULL
);


--
-- Name: appstatus; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.appstatus (
    id integer NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    version character varying NOT NULL,
    maintenance boolean DEFAULT false NOT NULL,
    notes character varying
);


--
-- Name: appstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.appstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: appstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.appstatus_id_seq OWNED BY public.appstatus.id;


--
-- Name: bannedhistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bannedhistory (
    id integer NOT NULL,
    user_id integer NOT NULL,
    banned boolean NOT NULL,
    by integer NOT NULL,
    reason character varying NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: bannedhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bannedhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bannedhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bannedhistory_id_seq OWNED BY public.bannedhistory.id;


--
-- Name: bannedusernames; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.bannedusernames (
    id integer NOT NULL,
    username character varying NOT NULL,
    by integer NOT NULL,
    comment character varying
);


--
-- Name: bannedusernames_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bannedusernames_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bannedusernames_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bannedusernames_id_seq OWNED BY public.bannedusernames.id;


--
-- Name: championships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.championships (
    id integer NOT NULL,
    name character varying NOT NULL
);


--
-- Name: championships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.championships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: championships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.championships_id_seq OWNED BY public.championships.id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.drivers (
    id integer NOT NULL,
    firstname character varying NOT NULL,
    lastname character varying NOT NULL,
    codename character varying NOT NULL
);


--
-- Name: drivers_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.drivers_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: drivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.drivers_id_seq OWNED BY public.drivers.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.events (
    id integer NOT NULL,
    name character varying NOT NULL,
    color character varying NOT NULL,
    championship_id integer NOT NULL
);


--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: eventstranslations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.eventstranslations (
    event_id integer NOT NULL,
    language character varying NOT NULL,
    name character varying NOT NULL
);


--
-- Name: googleids; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.googleids (
    user_id integer NOT NULL,
    google_id bigint NOT NULL
);


--
-- Name: loginattempts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.loginattempts (
    address character varying NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: premiumhistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.premiumhistory (
    id integer NOT NULL,
    user_id integer NOT NULL,
    premium boolean NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: premiumhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.premiumhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: premiumhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.premiumhistory_id_seq OWNED BY public.premiumhistory.id;


--
-- Name: promotedhistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.promotedhistory (
    id integer NOT NULL,
    user_id integer NOT NULL,
    moderator boolean NOT NULL,
    admin boolean NOT NULL,
    by integer NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: promotedhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.promotedhistory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: promotedhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.promotedhistory_id_seq OWNED BY public.promotedhistory.id;


--
-- Name: scores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scores (
    user_id integer NOT NULL,
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    score integer NOT NULL
);


--
-- Name: sessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    name character varying NOT NULL,
    datetime timestamp with time zone NOT NULL,
    event_id integer NOT NULL,
    competitive boolean NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username public.citext NOT NULL,
    email public.citext NOT NULL,
    password character varying NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL,
    modified timestamp with time zone DEFAULT now() NOT NULL,
    language character varying,
    image character varying,
    referralcode character varying NOT NULL,
    verified boolean DEFAULT false NOT NULL
);


--
-- Name: ranks_championships_mv; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW public.ranks_championships_mv AS
 SELECT championships.id AS championship_id,
    users.id AS user_id,
    COALESCE(sum(scores.score), (0)::bigint) AS score,
    row_number() OVER (PARTITION BY championships.id ORDER BY (sum(scores.score)) DESC) AS rank
   FROM ((((public.scores
     LEFT JOIN public.users ON ((users.id = scores.user_id)))
     LEFT JOIN public.sessions ON ((sessions.id = scores.session_id)))
     LEFT JOIN public.events ON ((events.id = sessions.event_id)))
     LEFT JOIN public.championships ON ((championships.id = events.championship_id)))
  GROUP BY championships.id, users.id
  ORDER BY COALESCE(sum(scores.score), (0)::bigint) DESC
  WITH NO DATA;


--
-- Name: ranks_events_mv; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW public.ranks_events_mv AS
 SELECT events.id AS event_id,
    championships.id AS championship_id,
    users.id AS user_id,
    COALESCE(sum(scores.score), (0)::bigint) AS score,
    row_number() OVER (PARTITION BY events.id ORDER BY (sum(scores.score)) DESC) AS rank
   FROM ((((public.scores
     LEFT JOIN public.users ON ((users.id = scores.user_id)))
     LEFT JOIN public.sessions ON ((sessions.id = scores.session_id)))
     LEFT JOIN public.events ON ((events.id = sessions.event_id)))
     LEFT JOIN public.championships ON ((championships.id = events.championship_id)))
  GROUP BY events.id, championships.id, users.id
  ORDER BY COALESCE(sum(scores.score), (0)::bigint) DESC
  WITH NO DATA;


--
-- Name: ranks_sessions_mv; Type: MATERIALIZED VIEW; Schema: public; Owner: -
--

CREATE MATERIALIZED VIEW public.ranks_sessions_mv AS
 SELECT sessions.id AS session_id,
    championships.id AS championship_id,
    users.id AS user_id,
    COALESCE(sum(scores.score), (0)::bigint) AS score,
    row_number() OVER (PARTITION BY championships.id ORDER BY (sum(scores.score)) DESC) AS rank
   FROM ((((public.scores
     LEFT JOIN public.users ON ((users.id = scores.user_id)))
     LEFT JOIN public.sessions ON ((sessions.id = scores.session_id)))
     LEFT JOIN public.events ON ((events.id = sessions.event_id)))
     LEFT JOIN public.championships ON ((championships.id = events.championship_id)))
  GROUP BY sessions.id, championships.id, users.id
  ORDER BY COALESCE(sum(scores.score), (0)::bigint) DESC
  WITH NO DATA;


--
-- Name: referrals; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.referrals (
    user_id integer NOT NULL,
    referral integer NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: refreshtokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.refreshtokens (
    user_id integer NOT NULL,
    token character varying NOT NULL
);


--
-- Name: revokedtokens; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.revokedtokens (
    token character varying NOT NULL
);


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying NOT NULL
);


--
-- Name: scoresparameters; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.scoresparameters (
    championship_id integer NOT NULL,
    param character varying NOT NULL,
    value0 integer DEFAULT 0 NOT NULL,
    value1 integer DEFAULT 0 NOT NULL,
    value2 integer DEFAULT 0 NOT NULL
);


--
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- Name: sessionspredictions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessionspredictions (
    session_id integer NOT NULL,
    user_id integer NOT NULL,
    driver_id integer NOT NULL,
    mygrid integer NOT NULL,
    potential integer NOT NULL,
    created timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: sessionsregistrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessionsregistrations (
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    team_id integer NOT NULL,
    prediction integer NOT NULL
);


--
-- Name: sessionsresults; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessionsresults (
    session_id integer NOT NULL,
    driver_id integer NOT NULL,
    result integer NOT NULL,
    points numeric DEFAULT 0 NOT NULL
);


--
-- Name: sessionstranslations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sessionstranslations (
    session_id integer NOT NULL,
    language character varying NOT NULL,
    name character varying NOT NULL
);


--
-- Name: teams; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.teams (
    id integer NOT NULL,
    name character varying NOT NULL,
    color character varying NOT NULL
);


--
-- Name: teams_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.teams_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: teams_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.teams_id_seq OWNED BY public.teams.id;


--
-- Name: userobligations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.userobligations (
    id integer NOT NULL,
    user_id integer NOT NULL,
    obligation character varying NOT NULL
);


--
-- Name: userobligations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.userobligations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: userobligations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.userobligations_id_seq OWNED BY public.userobligations.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: appstatus id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appstatus ALTER COLUMN id SET DEFAULT nextval('public.appstatus_id_seq'::regclass);


--
-- Name: bannedhistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedhistory ALTER COLUMN id SET DEFAULT nextval('public.bannedhistory_id_seq'::regclass);


--
-- Name: bannedusernames id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedusernames ALTER COLUMN id SET DEFAULT nextval('public.bannedusernames_id_seq'::regclass);


--
-- Name: championships id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.championships ALTER COLUMN id SET DEFAULT nextval('public.championships_id_seq'::regclass);


--
-- Name: drivers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drivers ALTER COLUMN id SET DEFAULT nextval('public.drivers_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: premiumhistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.premiumhistory ALTER COLUMN id SET DEFAULT nextval('public.premiumhistory_id_seq'::regclass);


--
-- Name: promotedhistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promotedhistory ALTER COLUMN id SET DEFAULT nextval('public.promotedhistory_id_seq'::regclass);


--
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- Name: teams id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams ALTER COLUMN id SET DEFAULT nextval('public.teams_id_seq'::regclass);


--
-- Name: userobligations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.userobligations ALTER COLUMN id SET DEFAULT nextval('public.userobligations_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: appleids appleids_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appleids
    ADD CONSTRAINT appleids_pkey PRIMARY KEY (user_id);


--
-- Name: appstatus appstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appstatus
    ADD CONSTRAINT appstatus_pkey PRIMARY KEY (id);


--
-- Name: bannedhistory bannedhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedhistory
    ADD CONSTRAINT bannedhistory_pkey PRIMARY KEY (id);


--
-- Name: bannedusernames bannedusernames_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedusernames
    ADD CONSTRAINT bannedusernames_pkey PRIMARY KEY (id);


--
-- Name: championships championships_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.championships
    ADD CONSTRAINT championships_name_unique UNIQUE (name);


--
-- Name: championships championships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.championships
    ADD CONSTRAINT championships_pkey PRIMARY KEY (id);


--
-- Name: drivers drivers_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_name_unique UNIQUE (firstname, lastname);


--
-- Name: drivers drivers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.drivers
    ADD CONSTRAINT drivers_pkey PRIMARY KEY (id);


--
-- Name: events events_championship_id_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_championship_id_name_key UNIQUE (championship_id, name);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: eventstranslations eventstranslations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eventstranslations
    ADD CONSTRAINT eventstranslations_pkey PRIMARY KEY (event_id, language);


--
-- Name: googleids googleids_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.googleids
    ADD CONSTRAINT googleids_pkey PRIMARY KEY (user_id);


--
-- Name: loginattempts loginattempts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.loginattempts
    ADD CONSTRAINT loginattempts_pkey PRIMARY KEY (address, created);


--
-- Name: premiumhistory premiumhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.premiumhistory
    ADD CONSTRAINT premiumhistory_pkey PRIMARY KEY (id);


--
-- Name: promotedhistory promotedhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promotedhistory
    ADD CONSTRAINT promotedhistory_pkey PRIMARY KEY (id);


--
-- Name: referrals referrals_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_pkey PRIMARY KEY (user_id);


--
-- Name: refreshtokens refreshtokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.refreshtokens
    ADD CONSTRAINT refreshtokens_pkey PRIMARY KEY (token);


--
-- Name: revokedtokens revokedtokens_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.revokedtokens
    ADD CONSTRAINT revokedtokens_pkey PRIMARY KEY (token);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: scores scores_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_pkey PRIMARY KEY (user_id, session_id, driver_id);


--
-- Name: scoresparameters scoresparameters_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scoresparameters
    ADD CONSTRAINT scoresparameters_pkey PRIMARY KEY (param, championship_id);


--
-- Name: sessions sessions_name_event_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_name_event_id_key UNIQUE (name, event_id);


--
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- Name: sessionspredictions sessionspredictions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionspredictions
    ADD CONSTRAINT sessionspredictions_pkey PRIMARY KEY (session_id, user_id, driver_id);


--
-- Name: sessionspredictions sessionspredictions_session_id_user_id_mygrid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionspredictions
    ADD CONSTRAINT sessionspredictions_session_id_user_id_mygrid_key UNIQUE (session_id, user_id, mygrid);


--
-- Name: sessionsregistrations sessionsregistrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsregistrations
    ADD CONSTRAINT sessionsregistrations_pkey PRIMARY KEY (session_id, driver_id);


--
-- Name: sessionsregistrations sessionsregistrations_session_id_prediction_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsregistrations
    ADD CONSTRAINT sessionsregistrations_session_id_prediction_key UNIQUE (session_id, prediction);


--
-- Name: sessionsresults sessionsresults_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsresults
    ADD CONSTRAINT sessionsresults_pkey PRIMARY KEY (session_id, driver_id);


--
-- Name: sessionstranslations sessionstranslations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionstranslations
    ADD CONSTRAINT sessionstranslations_pkey PRIMARY KEY (session_id, language);


--
-- Name: teams teams_name_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_name_unique UNIQUE (name);


--
-- Name: teams teams_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.teams
    ADD CONSTRAINT teams_pkey PRIMARY KEY (id);


--
-- Name: userobligations userobligations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.userobligations
    ADD CONSTRAINT userobligations_pkey PRIMARY KEY (id);


--
-- Name: users users_email_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_unique UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_referralcode_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_referralcode_unique UNIQUE (referralcode);


--
-- Name: users users_username_unique; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_unique UNIQUE (username);


--
-- Name: appleids appleids_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.appleids
    ADD CONSTRAINT appleids_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bannedhistory bannedhistory_users_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedhistory
    ADD CONSTRAINT bannedhistory_users_fkey1 FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bannedhistory bannedhistory_users_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedhistory
    ADD CONSTRAINT bannedhistory_users_fkey2 FOREIGN KEY (by) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: bannedusernames bannedusernames_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.bannedusernames
    ADD CONSTRAINT bannedusernames_users_fkey FOREIGN KEY (by) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: events events_championships_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_championships_fkey FOREIGN KEY (championship_id) REFERENCES public.championships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: eventstranslations eventstranslations_events_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eventstranslations
    ADD CONSTRAINT eventstranslations_events_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: googleids googleids_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.googleids
    ADD CONSTRAINT googleids_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: premiumhistory premiumhistory_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.premiumhistory
    ADD CONSTRAINT premiumhistory_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: promotedhistory promotedhistory_users_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promotedhistory
    ADD CONSTRAINT promotedhistory_users_fkey1 FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: promotedhistory promotedhistory_users_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.promotedhistory
    ADD CONSTRAINT promotedhistory_users_fkey2 FOREIGN KEY (by) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: referrals referrals_users_fkey1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_users_fkey1 FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: referrals referrals_users_fkey2; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.referrals
    ADD CONSTRAINT referrals_users_fkey2 FOREIGN KEY (referral) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: scores scores_drivers_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_drivers_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: scores scores_sessions_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_sessions_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: scores scores_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scores
    ADD CONSTRAINT scores_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: scoresparameters scoresparameters; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.scoresparameters
    ADD CONSTRAINT scoresparameters FOREIGN KEY (championship_id) REFERENCES public.championships(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessions sessions_events_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_events_fkey FOREIGN KEY (event_id) REFERENCES public.events(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionspredictions sessionspredictions_drivers_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionspredictions
    ADD CONSTRAINT sessionspredictions_drivers_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionspredictions sessionspredictions_sessions_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionspredictions
    ADD CONSTRAINT sessionspredictions_sessions_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionspredictions sessionspredictions_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionspredictions
    ADD CONSTRAINT sessionspredictions_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionsregistrations sessionsregistrations_drivers_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsregistrations
    ADD CONSTRAINT sessionsregistrations_drivers_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionsregistrations sessionsregistrations_sessions_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsregistrations
    ADD CONSTRAINT sessionsregistrations_sessions_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionsregistrations sessionsregistrations_teams_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsregistrations
    ADD CONSTRAINT sessionsregistrations_teams_fkey FOREIGN KEY (team_id) REFERENCES public.teams(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionsresults sessionsresults_drivers_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsresults
    ADD CONSTRAINT sessionsresults_drivers_fkey FOREIGN KEY (driver_id) REFERENCES public.drivers(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionsresults sessionsresults_sessions_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionsresults
    ADD CONSTRAINT sessionsresults_sessions_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: sessionstranslations sessionstranslations_session_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sessionstranslations
    ADD CONSTRAINT sessionstranslations_session_fkey FOREIGN KEY (session_id) REFERENCES public.sessions(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: userobligations userobligations_users_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.userobligations
    ADD CONSTRAINT userobligations_users_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict oxliJAPtW600MgzTwlv6eZcydCmd0P7ipDIlyw2a7HJoVZCNJ8bJvY0cLoUxc8G


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('20250809102916'),
    ('20250809110104'),
    ('20250811140523'),
    ('20250811151709'),
    ('20250811151957'),
    ('20250812134518'),
    ('20250812134530'),
    ('20250812204704'),
    ('20250815035020'),
    ('20250815042221'),
    ('20250905201633'),
    ('20251005090307'),
    ('20251016185212'),
    ('20251016185235'),
    ('20251016185242'),
    ('20251016185248'),
    ('20251016185252'),
    ('20251016185314'),
    ('20251016185326'),
    ('20251016185342'),
    ('20251016185411'),
    ('20251025085552'),
    ('20251025085636'),
    ('20251026175506'),
    ('20251105212600'),
    ('20251108095319'),
    ('20251108095327'),
    ('20251205204059'),
    ('20251214144418');
