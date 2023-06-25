// Clear data
MATCH (n)
DETACH DELETE n;

// Create indexes
CREATE RANGE INDEX text_label IF NOT EXISTS
FOR (w:Word) ON (w.text, w.label);

CREATE RANGE INDEX id IF NOT EXISTS
FOR (w:Word) ON (w.id);

// Preload vertices
// USING PERIODIC COMMIT 100000
CALL apoc.periodic.iterate('
CALL apoc.load.csv("file: ///words.csv", {sep: "|"}) yield map as line return line
',
'
CREATE (w:Word { id: line[0], lang: line[1], text: line[2] })
', { batchSize:10000, iterateList: true , parallel: true })
// RETURN COUNT(w) AS `Inserted words:`;

// Load relationships
// USING PERIODIC COMMIT 100000
LOAD CSV FROM 'file: ///relationships.csv' AS line
FIELDTERMINATOR '|'

MATCH (a:Word { id: line[0] })
MATCH (b:Word { id: line[2] })
CALL apoc.create.relationship(a, line[1], { }, b) YIELD rel
RETURN COUNT(rel) AS `Inserted relationships:`;
