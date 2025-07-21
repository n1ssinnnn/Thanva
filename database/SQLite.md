# SQLite

## Connect
``` sqlite3.connect("db_name") ```

## Cursor
``` cursor = connect.cursor() ```

## Execute
``` cursor.execute() ```

## Create table

```
cursor.execute('''CREATE TABLE IF NOT EXISTS table_name (
column_name_1 column_type,
column_name_2 column_type,
column_name_3 column_type)''')
```

## Insert
```
cursor.execute("INSERT INTO table_name (x1, x2) values (?,?)", (value, value))
```

## Record
```
connect.commit()
```


