

-- SPECIES INFO
CREATE TABLE species (
    gcf STRING PRIMARY KEY,
    genus STRING,
    species STRING
);

-- rrna info from RIBDIF
CREATE TABLE ribdif_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gcf INT REFERENCES species (gcf),
    number_16s INTEGER DEFAULT NULL, 
    mean REAL DEFAULT NULL,
    sd REAL DEFAULT NULL,
    min REAL DEFAULT NULL,
    max REAL DEFAULT NULL,
    total_div REAL DEFAULT NULL
);


----16S rRNA SEQUENCES
-- SEQUENCE (FULL 16s rRNA)
CREATE TABLE s16full_sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence STRING UNIQUE);
-- SPECIES TO FULL SEQUENCE
CREATE TABLE species2s16full_sequence (
    sequence_id INT REFERENCES s16full_sequence (id),
    gcf STRING REFERENCES species (gcf)
);


----V1V9 CLUSTER
-- V1V9 cluster sequence
CREATE TABLE v1v9sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence STRING UNIQUE
);
-- SPECIES TO V1V9 CLUSTER
CREATE TABLE species2V1V9sequence (
    sequence_id INT REFERENCES v1v9sequence (id),
    gcf STRING REFERENCES species (gcf)
);


-----V3V4 cluster
-- V3V4 cluster sequence
CREATE TABLE v3v4sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence STRING UNIQUE
    );
-- SPECIES TO V1V9 CLUSTER
CREATE TABLE species2V3V4sequence (
    sequence_id INT REFERENCES v3v4sequence (id),
    gcf STRING REFERENCES species (gcf)
);

.exit