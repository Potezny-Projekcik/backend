-- Schema: mydb
DROP DATABASE IF EXISTS "Baza1";
CREATE DATABASE "Baza1";

-- Table: User
CREATE TABLE IF NOT EXISTS "User" (
  "userid" SERIAL PRIMARY KEY,
  "firstname" VARCHAR(45) NOT NULL,
  "lastname" VARCHAR(45) NOT NULL,
  "password" CHAR(128) NOT NULL,
  "birthdate" DATE NOT NULL,
  "isadmin" BOOLEAN NOT NULL DEFAULT false
);
ALTER TABLE "User" ADD COLUMN "last_login" timestamp with time zone;
ALTER TABLE "User" ADD COLUMN "username" varchar(150);

-- Table: Category
CREATE TABLE IF NOT EXISTS "Category" (
  "categoryid" SERIAL PRIMARY KEY,
  "categoryname" VARCHAR(45) NOT NULL
);

-- Table: Producer
CREATE TABLE IF NOT EXISTS "Producer" (
  "producerid" SERIAL PRIMARY KEY,
  "producername" VARCHAR(45)
);

-- Table: Director
CREATE TABLE IF NOT EXISTS "Director" (
  "directorid" SERIAL PRIMARY KEY,
  "directorfirstname" VARCHAR(45),
  "directorlastname" VARCHAR(45)
);

-- Table: Language
CREATE TABLE IF NOT EXISTS "Language" (
  "languageid" SERIAL PRIMARY KEY,
  "languagename" VARCHAR(45)
);

-- Table: Movie
CREATE TABLE IF NOT EXISTS "Movie" (
  "movieid" SERIAL PRIMARY KEY,
  "title" VARCHAR(45) NOT NULL,
  "genre" VARCHAR(45) NOT NULL,
  "countryoforigin" VARCHAR(45) NOT NULL,
  "productionyear" DATE NOT NULL,
  "suggestedage" VARCHAR(2)
);

-- Table: Producers
CREATE TABLE IF NOT EXISTS "Producers" (
  "producersid" SERIAL PRIMARY KEY,
  "producerid" INT NOT NULL,
  "movieid" INT NOT NULL,
  CONSTRAINT fk_producers_producer
    FOREIGN KEY ("producerid")
    REFERENCES "Producer" ("producerid"),
  CONSTRAINT fk_producers_movie
    FOREIGN KEY ("movieid")
    REFERENCES "Movie" ("movieid")
);

-- Table: Directors
CREATE TABLE IF NOT EXISTS "Directors" (
  "directorsid" SERIAL PRIMARY KEY,
  "directorid" INT NOT NULL,
  "movieid" INT NOT NULL,
  CONSTRAINT fk_directors_director
    FOREIGN KEY ("directorid")
    REFERENCES "Director" ("directorid"),
  CONSTRAINT fk_directors_movie
    FOREIGN KEY ("movieid")
    REFERENCES "Movie" ("movieid")
);

-- Table: Languages
CREATE TABLE IF NOT EXISTS "Languages" (
  "languagesid" SERIAL PRIMARY KEY,
  "languageid" INT NOT NULL,
  "movieid" INT NOT NULL,
  CONSTRAINT fk_languages_language
    FOREIGN KEY ("languageid")
    REFERENCES "Language" ("languageid"),
  CONSTRAINT fk_languages_movie
    FOREIGN KEY ("movieid")
    REFERENCES "Movie" ("movieid")
);


-- Table: UserMovies
CREATE TABLE IF NOT EXISTS "UserMovies" (
  "userid" INT NOT NULL,
  "movieid" INT NOT NULL,
  "usermovieid" SERIAL PRIMARY KEY,
  "sessiondate" DATE,
  "sessiontime" TIME,
  "sessionpriority" SMALLINT,
  CONSTRAINT fk_user
    FOREIGN KEY ("userid")
    REFERENCES "User" ("userid"),
  CONSTRAINT fk_movie
    FOREIGN KEY ("movieid")
    REFERENCES "Movie" ("movieid")
);

-- Table: MovieCategory
CREATE TABLE IF NOT EXISTS "MovieCategory" (
  "moviecategoryid" SERIAL PRIMARY KEY,
  "usermovieid" INT NOT NULL,
  "categoryid" INT NOT NULL,
  CONSTRAINT fk_usermovies
    FOREIGN KEY ("usermovieid")
    REFERENCES "UserMovies" ("usermovieid"),
  CONSTRAINT fk_category
    FOREIGN KEY ("categoryid")
    REFERENCES "Category" ("categoryid")
);


INSERT INTO "User" ("firstname", "lastname", "login", "password", "birthdate", "isadmin")
VALUES
    ('John', 'Doe', 'johndoe', 'password1', '1990-01-01', false),
    ('Jane', 'Smith', 'janesmith', 'password2', '1995-05-15', false);


INSERT INTO "Movie" ("title", "genre", "countryoforigin", "productionyear", "suggestedage")
VALUES
    ('Movie 1', 'Action', 'USA', '2022-01-01', 'PG'),
    ('Movie 2', 'Drama', 'UK', '2021-03-15', 'R'),
    ('Movie 3', 'Comedy', 'Canada', '2023-06-10', 'PG');

INSERT INTO "UserMovies" ("userid", "movieid", "sessiondate", "sessiontime", "sessionpriority")
VALUES
    (1, 1, '2023-05-30', '12:00:00', 1),
    (1, 2, '2023-05-30', '15:30:00', 2),
    (2, 3, '2023-05-31', '14:00:00', 1);

INSERT INTO "Category" ("categoryname")
VALUES
    ('Do piwa'),
    ('Na randewu'),
    ('Z ziomusiami');

INSERT INTO "MovieCategory" ("usermovieid", "categoryid")
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO "Director" ("directorfirstname", "directorlastname")
VALUES
    ('Christopher', 'Nolan'),
    ('Quentin', 'Tarantino'),
    ('Steven', 'Spielberg');

INSERT INTO "Directors" ("directorid", "movieid")
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO "Producer" ("producername")
VALUES
    ('Jerry Bruckheimer'),
    ('Scott Rudin'),
    ('Kathleen Kennedy');

INSERT INTO "Producers" ("producerid", "movieid")
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

INSERT INTO "Language" ("languagename")
VALUES
    ('English'),
    ('French'),
    ('Spanish');

INSERT INTO "Languages" ("languageid", "movieid")
VALUES
    (1, 1),
    (2, 2),
    (3, 3);

CREATE OR REPLACE VIEW UserMoviesByCategory AS
SELECT
  c.categoryid,
  um.usermovieid,
  m.title,
  m.genre,
  m.countryoforigin,
  m.productionyear,
  m.suggestedage,
  d.directorfirstname,
  d.directorlastname,
  p.producername,
  l.languagename
FROM
  "UserMovies" um
  INNER JOIN "Movie" m ON um.movieid = m.movieid
  INNER JOIN "MovieCategory" mc ON um.usermovieid = mc.usermovieid
  INNER JOIN "Category" c ON mc.categoryid = c.categoryid
  LEFT JOIN "Directors" dm ON dm.movieid = m.movieid
  LEFT JOIN "Director" d ON d.directorid = dm.directorid
  LEFT JOIN "Producers" pm ON pm.movieid = m.movieid
  LEFT JOIN "Producer" p ON p.producerid = pm.producerid
  LEFT JOIN "Languages" lm ON lm.movieid = m.movieid
  LEFT JOIN "Language" l ON l.languageid = lm.languageid;


CREATE OR REPLACE VIEW "MovieDetails" AS
SELECT M.*, L.languagename, D.directorfirstname, D.directorlastname, P.producername
FROM "Movie" M
LEFT JOIN "Languages" ML ON M.movieid = ML.movieid
LEFT JOIN "Language" L ON ML.languageid = L.languageid
LEFT JOIN "Directors" MD ON M.movieid = MD.movieid
LEFT JOIN "Director" D ON MD.directorid = D.directorid
LEFT JOIN "Producers" MP ON M.movieid = MP.movieid
LEFT JOIN "Producer" P ON MP.producerid = P.producerid;


CREATE OR REPLACE VIEW UserMovieDetails AS
SELECT
  um.usermovieid,
  m.title,
  m.genre,
  m.countryoforigin,
  m.productionyear,
  m.suggestedage,
  d.directorfirstname,
  d.directorlastname,
  p.producername,
  l.languagename
FROM
  "UserMovies" um
  INNER JOIN "Movie" m ON um.movieid = m.movieid
  LEFT JOIN "Directors" dm ON dm.movieid = m.movieid
  LEFT JOIN "Director" d ON d.directorid = dm.directorid
  LEFT JOIN "Producers" pm ON pm.movieid = m.movieid
  LEFT JOIN "Producer" p ON p.producerid = pm.producerid
  LEFT JOIN "Languages" lm ON lm.movieid = m.movieid
  LEFT JOIN "Language" l ON l.languageid = lm.languageid;

CREATE OR REPLACE VIEW UserCategories AS
SELECT
  c.categoryid,
  c.categoryname,
  um.userid,
  u.firstname,
  u.lastname
FROM
  "Category" c
  INNER JOIN "MovieCategory" mc ON c.categoryid = mc.categoryid
  INNER JOIN "UserMovies" um ON mc.usermovieid = um.usermovieid
  INNER JOIN "User" u ON um.userid = u.userid;

CREATE OR REPLACE VIEW UncategorizedUserMoviesByCategory AS
SELECT
  NULL AS categoryid,
  um.usermovieid,
  m.title,
  m.genre,
  m.countryoforigin,
  m.productionyear,
  m.suggestedage,
  d.directorfirstname,
  d.directorlastname,
  p.producername,
  l.languagename
FROM
  "UserMovies" um
  INNER JOIN "Movie" m ON um.movieid = m.movieid
  LEFT JOIN "Directors" dm ON dm.movieid = m.movieid
  LEFT JOIN "Director" d ON d.directorid = dm.directorid
  LEFT JOIN "Producers" pm ON pm.movieid = m.movieid
  LEFT JOIN "Producer" p ON p.producerid = pm.producerid
  LEFT JOIN "Languages" lm ON lm.movieid = m.movieid
  LEFT JOIN "Language" l ON l.languageid = lm.languageid
WHERE
  um.usermovieid NOT IN (
    SELECT usermovieid
    FROM "MovieCategory"
  );


CREATE TRIGGER enforce_user_access_control_trigger
BEFORE DELETE OR UPDATE ON "User"
FOR EACH ROW
EXECUTE FUNCTION enforce_user_access_control();


CREATE OR REPLACE FUNCTION prevent_duplicate_movies()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM "Movie"
    WHERE title = NEW.title AND EXISTS (
      SELECT 1
      FROM "Producers" p
      WHERE p.movieid = NEW.movieid AND p.producerid IN (
        SELECT producerid
        FROM "Producers"
        WHERE movieid <> NEW.movieid
      )
    )
  ) THEN
    RAISE EXCEPTION 'A movie with the same title and producer already exists in the database.';
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_duplicate_movies_trigger
BEFORE INSERT ON "Movie"
FOR EACH ROW
EXECUTE FUNCTION prevent_duplicate_movies();

