// Clear data
MATCH (n)
DETACH DELETE n;

// Preload vertices
USING PERIODIC COMMIT LOAD CSV FROM 'file:///etymwn.csv' AS line
WITH split(line[0], ': ') as origin, split(line[2], ': ') as dest
MERGE (w1:Word {text: origin[1], lang: origin[0]})
MERGE (w2:Word {text: dest[1], lang: dest[0]});

// Load relationships
USING PERIODIC COMMIT LOAD CSV FROM 'file:///etymwn.csv' AS line
WITH split(line[0], ': ') as origin, split(line[2], ': ') as dest, split(line[1], ':')[1] as rel
MATCH (o:Word {text: origin[1], lang: origin[0]})
MATCH (d:Word {text: dest[1], lang: dest[0]})
MERGE (o)-[r:REL {type: rel}]->(d);