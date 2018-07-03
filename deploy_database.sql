--
-- File generated with SQLiteStudio v3.1.1 on Tue Jul 3 15:43:12 2018
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Status_sheet
DROP TABLE IF EXISTS Status_sheet;

CREATE TABLE Status_sheet (
    [Job Group]             TEXT,
    Workflow                TEXT    NOT NULL
                                    UNIQUE,
    Type                    TEXT,
    [Custom SP]             TEXT,
    [Database]              TEXT,
    DEV                     TEXT    DEFAULT 'Chenny',
    [Actual complete date]  NUMERIC,
    [Target Complete Date]  NUMERIC,
    [Code change Status]    TEXT,
    [Unit test status]      TEXT,
    Description             TEXT,
    [Lastest Modified Date] TEXT
);


-- View: daily_work
DROP VIEW IF EXISTS daily_work;
CREATE VIEW daily_work AS
    SELECT [Job Group],
           Workflow,
           Type,
           [Custom SP],
           [Database],
           DEV,
           [Code change Status],
           [Unit test status],
           Description
      FROM Status_sheet
     WHERE ([Code change Status] = 'Completed' OR
            [Code change Status] = 'Code changed' OR
            [Code change Status] = 'Onhold') AND
           [Lastest Modified Date] LIKE '%' || strftime('%Y-%m-%d', 'now') || '%';


-- View: test_todo
DROP VIEW IF EXISTS test_todo;
CREATE VIEW test_todo AS
    SELECT *
      FROM Status_sheet
     WHERE [Code change Status] = 'Completed' AND
           [Unit test Status] <> 'Completed' AND
           [Unit test Status] <> 'no data' AND
           [Unit test Status] <> 'Pending';


-- View: work_todo
DROP VIEW IF EXISTS work_todo;
CREATE VIEW work_todo AS
    SELECT *
      FROM Status_sheet
     WHERE [Code change Status] <> 'Completed';


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
