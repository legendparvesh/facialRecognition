# import mysql.connector
# mydb=mysql.connector.connect(
#     host=""
#     user
# )
# from datetime import datetime
# from datetime import date
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# x=now.hour
# y=now.minute
# print(y)
#
#  if((x>10 && y>25)||(x<11&&y<25)):
#      slot=1;
#  elif((x>11 && y>15)||(x<12&&y<05))
#      slot=2;
#  elif((x>12 && y>45)||(x<13&&y<30))
#      slot=3;
#"select slot from slots where start<="
from datetime import datetime as d
import mysql.connector

db = mysql.connector.connect(
        host="10.147.18.177",
        user="user",
        password="user@mysql",
        database="erp"
)
try:
        t = d.now()
        cur = db.cursor()
        hi = ''.join([str(t.hour),str(t.minute),"00"])
        cmd = "SELECT slot FROM `slots` WHERE start <= %s and end >= %s LIMIT 1;" % (hi,hi)
        cur.execute(cmd)
        print(cur.fetchone()[0])
except Exception:
        print("none")




