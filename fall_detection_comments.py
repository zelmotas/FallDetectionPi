import time  # Import time module to add delays in the code
import csv  # Import CSV module to handle data logging in CSV format
import smtplib  # Import smtplib to send email notifications
from sense_hat import SenseHat  # Import SenseHat module to interact with the Sense HAT

sense = SenseHat()  # Initialize the Sense HAT

# Set up a CSV file to log data
with open('fall_data.csv', mode='w') as file:  # Open a new CSV file in write mode
    writer = csv.writer(file)  # Create a CSV writer object
    writer.writerow(['Time', 'Acceleration X', 'Acceleration Y', 'Acceleration Z', 'Total Acceleration'])  # Write the header row

# Function to calculate the total acceleration vector magnitude
def calculate_magnitude(x, y, z):
    return (x**2 + y**2 + z**2)**0.5  # Return the magnitude using the formula sqrt(x^2 + y^2 + z^2)

# Email configuration function
def send_email():
    smtp_user = 'your_email@example.com'  # Your email address
    smtp_pass = 'your_password'  # Your email password
    to_email = 'recipient_email@example.com'  # The recipient's email address
    
    subject = 'Fall Detected'  # Subject of the email
    body = 'A fall was detected by your Raspberry Pi.'  # Body of the email
    
    email_text = f"Subject: {subject}\n\n{body}"  # Format the email
    
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)  # Connect to the SMTP server
        server.ehlo()  # Identify ourselves to the server
        server.starttls()  # Secure the connection
        server.ehlo()  # Re-identify ourselves after securing the connection
        server.login(smtp_user, smtp_pass)  # Log in to the email account
        server.sendmail(smtp_user, to_email, email_text)  # Send the email
        server.close()  # Close the connection
    except Exception as e:
        print(f"Failed to send email: {e}")  # Print an error message if sending fails

# Main loop to detect falls
while True:
    acceleration = sense.get_accelerometer_raw()  # Get raw accelerometer data
    x = acceleration['x']  # Extract the x component
    y = acceleration['y']  # Extract the y component
    z = acceleration['z']  # Extract the z component
    
    magnitude = calculate_magnitude(x, y, z)  # Calculate the total acceleration magnitude
    
    with open('fall_data.csv', mode='a') as file:  # Open the CSV file in append mode
        writer = csv.writer(file)  # Create a CSV writer object
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), x, y, z, magnitude])  # Log the time and acceleration data
    
    if magnitude > 2.5:  # Check if the magnitude exceeds a threshold (indicating a fall)
        print("Fall detected!")  # Print a message to the console
        send_email()  # Send an email notification
    
    time.sleep(1)  # Wait for 1 second before the next measurement
