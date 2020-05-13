CREATE TABLE stormlock (
  resource text PRIMARY KEY USING HASH,
  lease uuid NOT NULL,
  principal text NOT NULL,
  created timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expires timestamp without time zone NOT NULL
);

