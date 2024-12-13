CREATE SCHEMA chinook 

CREATE TABLE chinook.movie (
	film_id serial NOT NULL,
	title varchar(255) NOT NULL,
	description text NULL,
	release_year int4 NULL,
	language_id int2 NOT NULL,
	rental_duration int2 DEFAULT 3 NOT NULL,
	rental_rate numeric(4, 2) DEFAULT 4.99 NOT NULL,
	length int2 NULL,
	replacement_cost numeric(5, 2) DEFAULT 19.99 NOT NULL,
	rating text DEFAULT 'G'::text NULL,
	last_update timestamp(6) DEFAULT now() NOT NULL,
	special_features _text NULL,
	fulltext tsvector NOT NULL
);
CREATE TABLE chinook.film_actor (
	actor_id int2 NOT NULL,
	film_id int2 NOT NULL,
	last_update timestamp(6) DEFAULT now() NOT NULL
);

CREATE TABLE chinook.film_category (
	film_id int2 NOT NULL,
	category_id int2 NOT NULL,
	last_update timestamp(6) DEFAULT now() NOT NULL
);

CREATE TABLE chinook.category (
	category_id serial4 NOT NULL,
	"name" varchar(25) NOT NULL,
	last_update timestamp(6) DEFAULT now() NOT NULL
);