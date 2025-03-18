import tinydb

db = tinydb.TinyDB("db.json")
table_papel = db.table("papeis")
table_tecidos = db.table("tecidos")
table_tintas = db.table("tintas")


def insert_papel(data: dict, tabel=table_papel) -> bool | None:
    try:
        tabel.insert(data)
    except Exception as e:
        return None
    return True


def insert_tecido(data: dict, tabel=table_tecidos) -> bool | None:
    try:
        tabel.insert(data)
    except Exception as e:
        return None
    return True


def insert_tinta(data: dict, tabel=table_tintas) -> bool | None:
    try:
        tabel.insert(data)
    except Exception as e:
        return None
    return True

# insert_papel(data={'name': 'Papel Kraft 35gr 160x500', 'quantity': 1, 'metros': 50})
# insert_tecido(data={'name': 'Papel Kraft 35gr 160x500', 'quantity': 1, 'metros': 50})
