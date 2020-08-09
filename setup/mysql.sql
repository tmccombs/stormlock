CREATE TABLE stormlock (
    resource VARCHAR(128) PRIMARY KEY,
    lease BINARY(16) NOT NULL,
    principal VARCHAR(128) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT NOW(),
    expires TIMESTAMP NOT NULL
);
