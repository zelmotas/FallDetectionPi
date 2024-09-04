import time
import csv
import smtplib
from sense_hat import SenseHat

sense = SenseHat()

# Set up CSV file to log data
with open('fall_data.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'Acceleration X', 'Acceleration Y', 'Acceleration Z', 'Total Acceleration'])

# Function to calculate the total acceleration vector magnitude
def calculate_magnitude(x, y, z):
    return (x**2 + y**2 + z**2)**0.5

# Email configuration
def send_email():
    smtp_user = 'zelmotas@hotmail.com'
    smtp_pass = 'lwijmzfdixokjehr'
    to_email = 'telmotas@gmail.com'
    
    subject = 'Fall Detected'
    body = 'A fall was detected by your Raspberry Pi.'
    
    email_text = f"Subject: {subject}\n\n{body}"
    
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to_email, email_text)
        server.close()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Threshold for detecting a fall
FALL_THRESHOLD = 1.6  # Adjust based on testing

try:
    while True:
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']
        
        total_acceleration = calculate_magnitude(x, y, z)
        
        with open('fall_data.csv', mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([time.time(), x, y, z, total_acceleration])
        
        if total_acceleration > FALL_THRESHOLD:
            print("Fall Detected!!!")
            send_email()
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Program stopped by the user.")
