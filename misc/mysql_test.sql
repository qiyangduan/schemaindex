/* show comments */
SELECT
    table_name, column_name, COLUMN_COMMENT
FROM
    INFORMATION_SCHEMA.COLUMNS
WHERE
    TABLE_SCHEMA = 'blog' AND
    TABLE_NAME = 'authors'  ;




/* show fks */
ALTER TABLE `blog`.`entries` 
ADD INDEX `fk_entries_1_idx` (`author_id` ASC);
ALTER TABLE `blog`.`entries` 
ADD CONSTRAINT `fk_entries_1`
  FOREIGN KEY (`author_id`)
  REFERENCES `blog`.`authors` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;



