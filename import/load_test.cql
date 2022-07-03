// Clear data
MATCH (n)
DETACH DELETE n;

// Create indexes
CREATE BTREE INDEX text_label IF NOT EXISTS
FOR (w:Word) ON (w.text, w.label);

CREATE BTREE INDEX id IF NOT EXISTS
FOR (w:Word) ON (w.id);

// Preload vertices
USING PERIODIC COMMIT 100000
LOAD CSV FROM 'file:///words.csv' AS line
FIELDTERMINATOR '|'

CREATE (:Word {id: line[0], lang: line[1], text: line[2]});

// Load relationships
USING PERIODIC COMMIT 100000
LOAD CSV FROM 'file:///relationships.csv' AS line 
FIELDTERMINATOR '|'

MATCH (a:Word {id: line[0]})
MATCH (b:Word {id: line[2]})
CALL apoc.create.relationship(a, line[1], {}, b) YIELD rel
return count(rel);


// cat /import/load.cql | cypher-shell -u neo4j -p hello
// Import words.csv
// Import relationships.csv
// Add indexes
// Restart docker