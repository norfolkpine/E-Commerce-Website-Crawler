import mysql.connector
import random
r = random.randint(0, 5)

mydb = mysql.connector.connect(host="localhost",user="USER",passwd="PASSWORD",database="DATABASE")
mycursor = mydb.cursor(buffered=True)

sql = "INSERT INTO stage_website(SKU, Title, Brand, Availability, PriceCurrency, Price, URL, ImageURL, Description, Category) VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s,%s ) ON DUPLICATE KEY UPDATE Title=%s,Brand=%s,Availability=%s,PriceCurrency=%s,Price=%s,URL= %s,ImageURL=%s,Description = %s,Category = %s"
    
val = (1,1,1,1,1,r,1,1,1,1,1,1,1,r,1,1,1,1,1)
print("Status Updated")
mycursor.execute(sql,val)

mydb.commit()

