BEGIN TRANSACTION;

INSERT INTO publisher (publisher_name) VALUES
    ('Asmodii'), ('Tac Toc');
COMMIT;

BEGIN TRANSACTION;
-- John a acheté le jeu Living Forest le 10/01/2010.
-- John a acheté 3 jeux Unlock le 20/01/2020.
-- Jenny a acheté 2 jeux Detective le 21/01/2020.
INSERT INTO gameboard (title, category, publisher_id, publishing_date, nb_players) VALUES
    ('Living Forest', 'deck building', (SELECT publisher_id FROM publisher WHERE publisher_name = 'Tac Toc'), CURRENT_DATE, 1),
    ('Unlock', 'puzzle', (SELECT publisher_id FROM publisher WHERE publisher_name = 'Asmodii'), CURRENT_DATE, 1),
    ('Detective', 'puzzle', (SELECT publisher_id FROM publisher WHERE publisher_name = 'Asmodii'), CURRENT_DATE, 1),
    ('Kirk is missing', 'narrative', (SELECT publisher_id FROM publisher WHERE publisher_name = 'Asmodii'), CURRENT_DATE, 4);
-- Jenny a 25 ans.
-- John a 23 ans.
-- Yvan a 62 ans.
-- Yvonne a 67 ans.
-- Jordy a 18 ans.
INSERT INTO client (client_name, email, password, birthdate) VALUES
    ('Jenny', '', '', CURRENT_DATE - 25 * INTERVAL '1 year'),
    ('John', '', '', CURRENT_DATE - 23 * INTERVAL '1 year'),
    ('Yvan', '', '', CURRENT_DATE - 62 * INTERVAL '1 year'),
    ('Yvonne', '', '', CURRENT_DATE - 67 * INTERVAL '1 year'),
    ('Jordy', '', '', CURRENT_DATE - 18 * INTERVAL '1 year'),
    ('Bruce', '', 'bruce@tout.fr', CURRENT_DATE);

COMMIT;

BEGIN TRANSACTION;
-- Le jeu Living Forest est édité par Tac Toc.
-- Les jeux Unlock et Detective sont édités par Asmodii.
-- Asmodii a édité Kirk is missing.
-- Bruce est joignable à bruce@tout.fr.
-- Living Forest est un deck building.
-- Unlock et Detective sont des jeux de puzzle
INSERT INTO purchase (client_id, gameboard_id, purchase_date, quantity) VALUES
    ((SELECT client_id FROM client WHERE client_name = 'John'), (SELECT gameboard_id FROM gameboard WHERE title = 'Living Forest'), '2010-01-10', 1),
    ((SELECT client_id FROM client WHERE client_name = 'John'), (SELECT gameboard_id FROM gameboard WHERE title = 'Living Forest'), '2010-01-12', 1),
    ((SELECT client_id FROM client WHERE client_name = 'John'), (SELECT gameboard_id FROM gameboard WHERE title = 'Unlock'), '2010-01-20', 3),
    ((SELECT client_id FROM client WHERE client_name = 'Yvan'), (SELECT gameboard_id FROM gameboard WHERE title = 'Kirk is missing'), '2010-01-20', 5),
    ((SELECT client_id FROM client WHERE client_name = 'Jenny'), (SELECT gameboard_id FROM gameboard WHERE title = 'Detective'), '2010-01-10', 2);

INSERT INTO purchase (client_id, gameboard_id, purchase_date, quantity) VALUES
    ((SELECT client_id FROM client WHERE client_name = 'Bruce'), (SELECT gameboard_id FROM gameboard WHERE title = 'Living Forest'), '2010-01-10', 1),
    ((SELECT client_id FROM client WHERE client_name = 'Bruce'), (SELECT gameboard_id FROM gameboard WHERE title = 'Unlock'), '2010-01-10', 1),
        ((SELECT client_id FROM client WHERE client_name = 'Bruce'), (SELECT gameboard_id FROM gameboard WHERE title = 'Detective'), '2010-01-10', 1),
    ((SELECT client_id FROM client WHERE client_name = 'Bruce'), (SELECT gameboard_id FROM gameboard WHERE title = 'Kirk is missing'), '2010-01-10', 1);


COMMIT;
