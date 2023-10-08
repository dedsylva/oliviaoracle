tables = ['appointments']

create_table = '''
CREATE TABLE IF NOT EXISTS appointments(
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  start_date TEXT,
  start_time TEXT,
  end_date TEXT,
  end_time TEXT,
  description TEXT
);
'''

insert_value = '''
INSERT INTO appointments VALUES
  (1, "Test", "2023-10-08", "2-49", "2023-10-09", "2-40", null)
'''

select_value = '''
SELECT * FROM appointments WHERE id == 1
'''

select_values = '''
SELECT * FROM appointments 
'''

delete_value = '''
DELETE FROM appointments WHERE id == 1
'''

delete_table = '''
DROP TABLE IF EXISTS appointments
'''

