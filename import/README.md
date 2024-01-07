
## Preperation

```cypherl
// Clear data
MATCH (n)
DELETE n;
```

Then

```cypherl
STORAGE MODE IN_MEMORY_ANALYTICAL;
```

Load words
```

LOAD CSV FROM "/import/words.csv" NO HEADER DELIMITER "|" AS line
CREATE (w:Word { id: line[0], lang: line[1], name: line[2] })
RETURN COUNT(w) AS `Inserted`;

```

Create indexes
```
CREATE INDEX ON :Word(id);
CREATE INDEX ON :Word(label);
CREATE INDEX ON :Word(name);
```

Load edges
```

LOAD CSV FROM "/import/is_derived_from.csv" NO HEADER DELIMITER "|" AS line
MATCH (a:Word { id: line[0] }), (b:Word { id: line[2] })
CREATE (a)-[r:is_derived_from]->(b)
RETURN COUNT(r) AS `Inserted is_derived_from`;

LOAD CSV FROM "/import/etymological_origin_of.csv" NO HEADER DELIMITER "|" AS line
MATCH (a:Word { id: line[0] }), (b:Word { id: line[2] })
CREATE (a)-[r:etymological_origin_of]->(b)
RETURN COUNT(r) AS `Inserted etymological_origin_of`;

LOAD CSV FROM "/import/variant_orthography.csv" NO HEADER DELIMITER "|" AS line
MATCH (a:Word { id: line[0] }), (b:Word { id: line[2] })
CREATE (a)-[r:variant_orthography]->(b)
RETURN COUNT(r) AS `Inserted variant_orthography`;

LOAD CSV FROM "/import/etymologically_related.csv" NO HEADER DELIMITER "|" AS line
MATCH (a:Word { id: line[0] }), (b:Word { id: line[2] })
CREATE (a)-[r:etymologically_related]->(b)
RETURN COUNT(r) AS `Inserted etymologically_related`;
```
Example query

```
MATCH (w:Word {name: "television"})
RETURN w;
```
