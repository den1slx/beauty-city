import sqlite3
from datetime import timedelta
from django.utils import timezone

from order_bot.models import Master, Salon, Appointment, Procedure, Promo, WorkTime


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


con = sqlite3.connect("db.sqlite3", check_same_thread=False)
con.row_factory = dict_factory


def get_salons():
    cur: sqlite3.Cursor = con.execute(
        f'select title, address from order_bot_salon'
    )
    row = cur.fetchone()
    cur.close()
    return row


def get_masters():
    cur: sqlite3.Cursor = con.execute(
        f'select name from order_bot_master'
    )
    row = cur.fetchone()
    cur.close()
    return row


def get_procedure(id_procedure):
    cur: sqlite3.Cursor = con.execute(
        f'select title, price from order_bot_procedure where id like {id_procedure}'
    )
    row = cur.fetchone()
    cur.close()
    return row


def get_salon_procedure(salon):
    salon_id = Salon.objects.get(address=salon).id
    cur: sqlite3.Cursor = con.execute(
        f'select procedure_id from order_bot_salon_procedures where salon_id like {salon_id}'
    )
    rows = cur.fetchall()
    cur.close()
    rows = [get_procedure(row['procedure_id']) for row in rows]
    return rows


def get_master_procedure(master):
    master_id = Master.objects.get(name=master).id
    cur: sqlite3.Cursor = con.execute(
        f'select procedure_id from order_bot_master_service where master_id like {master_id}'
    )
    rows = cur.fetchall()
    cur.close()
    rows = [get_procedure(row['procedure_id']) for row in rows]
    return rows


def get_days():
    from_table = ''  # TODO table name
    select_colon = '*'  # TODO colon names
    cur: sqlite3.Cursor = con.execute(f'select {select_colon} from {from_table}')
    rows = cur.fetchall()
    cur.close()
    # ожидается список из 30 словарей
    # День = [{'смена': [{'начало': '', 'конец': '', 'мастер': ''}, ]},]
    # как лучше хранить это в db ?
    return rows


def create_client(date, salon_id, name, phone, master_id, service_id, prepay):
    if not master_id:
        master_id = WorkTime.objects.filter(workplace_id=salon_id).first().worker_id
    if not salon_id:
        salon_id = WorkTime.objects.filter(worker_id=master_id).first().workplace_id
    data = (date, salon_id, name, phone, master_id, service_id, prepay)
    cur = con.execute(
        'insert into order_bot_appointment '
        '(date, salon_id, name, phone_number, master_id, service_id, payment)'
        'values( ?, ?, ?, ?, ?, ?, ?)', data)
    con.commit()
    cur.close()
    return cur.lastrowid


def update_prepay_status(name, phone, date, status):
    client_id = Appointment.objects.get(
        name=name,
        phone_number=phone,
        date=date
    ).id
    from_table = 'order_bot_appointment'
    cur = con.execute(f'UPDATE {from_table} SET payment = {status} where id like {client_id}')
    con.commit()
    cur.close()
    return


def get_ids(salon, master, service):
    salon_id = Salon.objects.get(title=salon).id
    master_id = Master.objects.get(name=master).id
    service_id = Procedure.objects.get(title=service)
    return salon_id, master_id, service_id


def get_promo(code):
    cur: sqlite3.Cursor = con.execute(
        f'select promo from order_bot_promo where status like True'
    )
    rows = cur.fetchall()
    cur.close()
    for row in rows:
        if code == row.get('promo'):
            return True
    return False


def get_decades():
    today = timezone.now()
    first_decade = today + timedelta(days=10)
    second_decade = first_decade + timedelta(days=10)
    third_decade = today + timedelta(days=10)
    decades = [
        {'decade': f'{today.date()}:{first_decade.date()}'},
        {'decade': f'{first_decade.date()}:{second_decade.date()}'},
        {'decade': f'{second_decade.date()}:{third_decade.date()}'},
    ]
    return decades

