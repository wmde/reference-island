CREATE TABLE refs (
  ref_id int unsigned NOT NULL PRIMARY KEY AUTO_INCREMENT,
  ref_data mediumblob NOT NULL,
  -- 0 for unknown, 1 for good, 2 for bad
  ref_flag tinyint NOT NULL DEFAULT 0
);
CREATE UNIQUE INDEX ref_data ON references (ref_data);
-- Covering index
CREATE INDEX ref_flag ON references (ref_flag, ref_data, ref_id);