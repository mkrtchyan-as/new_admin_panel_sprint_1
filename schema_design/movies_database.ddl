CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created TIMESTAMP with time zone,
    modified TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name TEXT NOT NULL,
    created TIMESTAMP with time zone,
    modified TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created TIMESTAMP with time zone,
    modified TIMESTAMP with time zone
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    person_id uuid NOT NULL,
    role TEXT NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id, role);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    film_work_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone
);

CREATE UNIQUE INDEX film_work_genre_idx ON content.genre_film_work (film_work_id, genre_id);
