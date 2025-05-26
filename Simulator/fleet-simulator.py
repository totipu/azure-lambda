import os
import random
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
# import pymssql
import psycopg2 # Use psycopg2 for PostgreSQL instead of pymssql
from dotenv import load_dotenv

def get_car_plate():

    town_list = ["M", "B", "F", "D", "A", "H", "K"]
    letters = "ABCDEFGHIJKLMNOPQRSTUVZ"
    plate = random.choice(town_list) + "-" + ''.join(random.choice(letters) for i in range(2)) + "-"  + str(random.randint(100, 9999)) 

    return plate

def get_current_speed():
    
    current_speed = random.randint(1000, 18000) / 100
    
    return current_speed

def get_current_fuel_consumption():
    
    current_fuel_consumption = random.randint(2000, 18000) / 1000

    return current_fuel_consumption

async def main():

    # Load environment variables from .env file
    load_dotenv()

    # Fetch the database connection string from an environment variable
    dbhost = os.getenv("DBHOST")
    dbuser = os.getenv("DBUSER")
    dbpassword = os.getenv("DBPASSWORD")
    dbname = os.getenv("DBNAME")
    dbport = os.getenv("DBPORT")

    device_available = False
    device_connection_string = None
    device_name = None

    # conn = pymssql.connect(server=dbhost, user=dbuser, password=dbpassword, database=dbname)
    conn = psycopg2.connect(host=dbhost, port=dbport, user=dbuser, password=dbpassword, dbname=dbname)   
    cursor = conn.cursor() 
    cursor.execute("SELECT connectionstring, name FROM devices WHERE InUse = FALSE LIMIT 1")
    row = cursor.fetchone()
    if row:
        device_available = True
        device_connection_string = row[0]
        device_name = row[1]
        cursor = conn.cursor()
        cursor.execute("UPDATE Devices SET InUse = TRUE WHERE Name = '" + device_name + "'")
        conn.commit()
        conn.close()
    else:
        print ("No devices available")

    if device_available:

        print("Device available: " + device_name)
        print("Device connection string: " + device_connection_string)

        # choose the car plate
        car_plate = get_car_plate()
        print("Car plate: " + car_plate)

        # Create instance of the device client using the connection string
        device_client = IoTHubDeviceClient.create_from_connection_string(device_connection_string)

        # Connect the device client.
        await device_client.connect()

        while True:

            # get the current speed
            current_speed = get_current_speed()

            # get the current fuel consumption
            current_fuel_consumption = get_current_fuel_consumption()

            # build the message
            message = '{{"carPlate": "{0}", "speed": {1}, "fuelConsumption": {2}}}'.format(
                car_plate, current_speed, current_fuel_consumption)

            # Send a single message
            print("Sending message...")
            print(message)
            await device_client.send_message(message)
            print("Message successfully sent!")

            # Sleep for 2 seconds
            await asyncio.sleep(2)

        # Finally, shut down the client
        await device_client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())