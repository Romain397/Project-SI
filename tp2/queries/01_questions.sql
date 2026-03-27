
-- Noms des clients qui ont un age > 20
SELECT client_name, birthdate FROM client WHERE EXTRACT(year from CURRENT_DATE) - EXTRACT(year from birthdate) > 20;

-- Afficher tous les clients

SELECT client_name, birthdate FROM client;

-- Afficher les les clients qui ont un age > 20 avec une CTE

WITH old_clients AS (
    SELECT * FROM client WHERE EXTRACT(year from CURRENT_DATE) - EXTRACT(year from birthdate) > 20
) SELECT client_name, birthdate FROM old_clients;

-- Afficher tous les clients qui n'ont pas un age > 20 en reprenant entièrement la requête précédente sans modifier l'opérateur d'inégalité
-- EXCEPT ???

SELECT client_name, birthdate FROM client
EXCEPT
SELECT client_name, birthdate FROM client WHERE EXTRACT(year from CURRENT_DATE) - EXTRACT(year from birthdate) > 20;

-- Noms de clients ayant acheté le jeu de société ayant pour id 2

SELECT DISTINCT client_name FROM client NATURAL JOIN purchase WHERE gameboard_id = 2;

SELECT
    client_name
FROM
    client
WHERE
    client_id IN (
        SELECT
            client_id
        FROM
            purchase
        WHERE
            gameboard_id = 2);

-- Noms de clients ayant commandé un jeu de société pour 2 joueurs ou +

SELECT client_name FROM
    client NATURAL JOIN purchase
    NATURAL JOIN gameboard
    WHERE gameboard.nb_players >= 2;

-- Types de jeu commandés par Yvan

SELECT
    DISTINCT category
FROM
    gameboard
    NATURAL JOIN purchase
    NATURAL JOIN client
WHERE
    client_name = 'John';

SELECT
    category
FROM
    gameboard
    NATURAL JOIN purchase
    NATURAL JOIN client
WHERE
    client_name = 'John'
GROUP BY category;

SELECT category FROM gameboard WHERE gameboard_id IN (
    SELECT gameboard_id FROM purchase WHERE client_id IN (
        SELECT client_id FROM client WHERE client_name = 'John'
    )
);

WITH john_client AS (
    SELECT client_id FROM client WHERE client_name = 'John'
), john_purchase AS (
    SELECT gameboard_id FROM purchase WHERE client_id IN (SELECT client_id FROM john_client)
) SELECT category FROM gameboard WHERE gameboard_id IN (SELECT gameboard_id FROM john_purchase);


-- Noms des clients ayant commandé au moins un jeu

SELECT DISTINCT client_name FROM client NATURAL JOIN purchase;
SELECT DISTINCT client_name FROM client JOIN purchase USING(client_id);
SELECT DISTINCT client_name FROM client JOIN purchase ON client.client_id = purchase.client_id;

-- Noms des clients ayant commandé un jeu de rôle ou un puzzle

SELECT DISTINCT c.client_name FROM client c JOIN purchase p ON c.client_id = p.client_id
JOIN gameboard g ON p.gameboard_id = g.gameboard_id
WHERE g.category IN ('puzzle', 'jeu de role');

-- Clients ayant commandé au moins 2 jeux de société

SELECT client.client_id, client.client_name, SUM(purchase.quantity) total_quantity FROM client NATURAL JOIN purchase GROUP BY client.client_id, client.client_name HAVING SUM(purchase.quantity) >= 2;

-- Clients qui ont un âge > 50 et qui n’ont pas commmandé un jeu de société pour 2 joueurs ou +

SELECT * FROM client NATURAL JOIN (

SELECT client_id FROM client
EXCEPT
SELECT client_id FROM purchase NATURAL JOIN gameboard WHERE nb_players >= 2

) t WHERE EXTRACT(year from CURRENT_DATE) - EXTRACT(year from birthdate) > 50;



-- Clients qui ont commandé tous les jeux de société


WITH
purchases_not_happened AS (
SELECT client_id, gameboard_id FROM client
CROSS JOIN gameboard
EXCEPT
SELECT client_id, gameboard_id FROM purchase
),
best_clients AS (SELECT client_id FROM client EXCEPT SELECT client_id FROM purchases_not_happened)
SELECT * FROM client NATURAL JOIN best_clients 
-- Noms de client qui ont commandé tous les jeux de société de “deck building”