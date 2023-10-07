create_table = '''
CREATE TABLE IF NOT EXISTS appointments(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  start_date DATE,
  start_time TEXT,
  end_date DATE,
  end_time TEXT
);
'''

insert_value = '''
INSERT INTO appointments VALUES
  (1, "Test", null, "2023-10-07", "12", "2023-10-07", "13")
'''

select_value = '''
SELECT * FROM appointments where id == 1
'''

select_values = '''
SELECT * FROM appointments 
'''



delete_value = '''
DELETE FROM appointments where id == 1
'''

delete_table = '''
DROP TABLE IF EXISTS appointments
'''