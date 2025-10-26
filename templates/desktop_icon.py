import datetime
import webbrowser
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

# The website you want to be reminded about
URL = "https://example.com"

# Track last visit date
last_visit = None

# Create a simple cartoon-style icon (yellow smiley face)
def create_icon():
    img = Image.new("RGB", (64, 64), color=(255, 255, 0))
    d = ImageDraw.Draw(img)
    d.ellipse((8, 8, 56, 56), fill=(255, 230, 0), outline=(0, 0, 0))
    d.ellipse((20, 25, 28, 33), fill=(0, 0, 0))
    d.ellipse((36, 25, 44, 33), fill=(0, 0, 0))
    d.arc((20, 30, 44, 50), 0, 180, fill=(0, 0, 0), width=2)
    return img

def open_website(icon, item):
    global last_visit
    webbrowser.open(URL)
    last_visit = datetime.date.today()
    icon.notify("✅ You are already staying healthy today!")

def check_reminder(icon):
    global last_visit
    today = datetime.date.today()
    if last_visit != today:
        icon.notify("Don't forget to take care of your health today!")

def quit_app(icon, item):
    icon.stop()

# Create the tray icon menu
menu = Menu(
    MenuItem("Open Website", open_website),
    MenuItem("Check Reminder", lambda icon, item: check_reminder(icon)),
    MenuItem("Quit", quit_app)
)

# Initialize the icon
icon = Icon("daily_reminder", create_icon(), menu=menu)

# Run the tray icon
icon.run()

