LOCK TABLES users WRITE;
DROP TRIGGER users_bu;

delimiter |

CREATE TRIGGER users_bu
  BEFORE UPDATE ON users
    FOR EACH ROW BEGIN
      SET NEW.updated_at=NOW();
      SET NEW.updated_by=CURRENT_USER();
    END;
|

delimiter ;

UNLOCK TABLES;