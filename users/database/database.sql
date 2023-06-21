-- Table: public.users
CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    name character varying(255),
    age integer,
    description character varying(255),
    created_at timestamp without time zone DEFAULT now()
)