# python --version
# Python 3.11.5
from WPP_Whatsapp import Create
import PySimpleGUI as sg
import filetype
import time, os, re

APP_ICON = b"iVBORw0KGgoAAAANSUhEUgAAABsAAAAcCAMAAACnDzTfAAAAAXNSR0IB2cksfwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAcJQTFRFAAAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAawAAcBQAhm0Aqv8Aqv8AeDMAl7EAqv8AAAAAAAAAAAAAPQAAYwAAe0AAe0AAh3AAns8Aqv8Aqv8Aqv8AAAAAAAAAIQAAVgAAmr8Amr8Apu8Aqv8Aqv8AAAAAAAAAEBAQMDAwQEBAFAAAPAAAUAAAUAAAAAAAj4+Pv7+/BwAAGwAAGwAAAAAAAAAAAAgPAA0YAA4aNkFLoqit4uTm9fb3z8/PcHBwNjc3IyUmFxkcDhARAAAAAAAAAAAAASE/ASlPI0RiaHiHp62z7+/voqSmaG5zO0JIAAAAAAEAAAECBzpqE0FsLE9wUWR1gImRu8DEZ25zIiUmAAAAAAECAAIFOFZxXWt3bXeAAAECAAMFAA0aGkVtS2B0Y254AAMGAA0aAAECAAQGAAAAAAMFAAAAAAECAAoUAR87EzdYOFNrSmB0OEhXExgdAAAAAAABAAMHBxwvGUVtEzRSBhEbAAAAAS1VATRiATdpABguAAAApZsojQAAAJZ0Uk5TAAECBAYHBQMPKTlAPzgiC0K03+HpthAwcM/vv4/PcDAQ78+PEDBAcM9Av///z3BAj7/P70C//++/cM///////79A7////79AAQRwz////////////89wAxq87//////////vBTTo//////////8HQd3///9C1f/////P/kPSBts95f////////8r9P//////Dv//////JtyrQAAAAYhJREFUeJxjYEABjEzMLKwsbOyMDJiAiYOTi5uHl48fixyDgKCQkLCIKA+mjJi4hKSUpKSUNDemnLgMUEpCQhKbHLe0lKSMOLe0rJy8AqacpIS4GLe0opKyPExMRVUNDNQ1QKZpamnr6OrpQ+VUDQzBwMgYJGdiqmNmrmsB1WVpZW1ja2tjbWfv4MjAIK+saw6TUzWwcrJxdnFxtnG1c3NnYFCQ19MFm+nhqebl7ePj6+cfEBgUHBIapqoC0gl2S3hEpHdUdHRMbJx/fGBCYlKogSpIJ9gPySmpPtFp6RmZWdn+Af5xObmGanAv5eUX+ESnF2YWFWfFASUTgpHlSkrLossrKoEApNPFFkWuqhoqB9KJKldT6wOVA+lEMbOuph4hV5yF4pa6hsam5pbWNiho70CSC+/s6m7qaemFgr5+JDmPCYZWTk3N0dETJ02ePGlilDfI73BJNUur7iYfnykTJ0+eOMXbCxRmCAAK66lTQXpRdcHiaOpUkF50XSCgZjgVDJDcQQEAAHU1e0ler6JPAAAAAElFTkSuQmCC"
COOLDOWN_MOD = 10
COOLDOWN_AMMOUNT = 5
COUNTRY_CODE = 62

sg.theme('BlueMono')
main_layout = [
            [sg.Image(APP_ICON),sg.Text('Whatsapp Blaster', font='Any 18')],
            [sg.Text("Phone Numbers (one per line)")],
            [sg.Multiline(size=(45,3),)],
            [sg.Text("Message to Send")],
            [sg.Multiline(size=(45,15),)],
            [sg.Text("Message Cheatsheet:\n_Italic_ *Bold* ~Strikethrough~ ```Monospace```\nMax Message Length: 65536 Chars", text_color='white')],
            [sg.Text("Image to attach (if any)")],
            [sg.Input(size=(45),), sg.FileBrowse()],
            [sg.Button('SEND IT!')],
        ]
window = sg.Window('Whatsapp Blaster',main_layout,icon=APP_ICON)
event, values = window.read()

def format_and_sanitize_phone_number(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
    if phone_number.startswith('0'):
        phone_number = str(COUNTRY_CODE) + phone_number[1:]
    return phone_number

print(values)

phone_number_list = values[1].split("\n")
message_to_send = values[2]
image_to_attach = values[3]

print(values)
print(event)
print(phone_number_list)
sanitized_phone_number_list = [format_and_sanitize_phone_number(number) for number in phone_number_list]
print(sanitized_phone_number_list)
print(message_to_send)
print(image_to_attach)

def is_image_file(file_path):
    kind = filetype.guess(file_path)
    if kind is None:
        return False
    return kind.mime.startswith('image/')

def send_messages(client, phone_numbers, message_type, message, image_path=None):
    for idx, number in enumerate(phone_numbers, start=1):
        if message_type == 'image':
            client.sendImage(to=number, filePath=image_path, filename="image", caption=message)
            print(f"Sent image to {number}")
        else:
            client.sendText(to=number, content=message)
            print(f"Sent text to {number}")
        if idx % COOLDOWN_MOD == 0:
            print("Cooling Down")
            time.sleep(COOLDOWN_AMMOUNT)

def blast(phone_numbers, image_path=None, message=""):
    creator = Create(session="prods")
    client = creator.start()
    try:
        if creator.state != 'CONNECTED':
            raise Exception(creator.state)
        message_type = 'image' if image_path and is_image_file(image_path) else 'text'
        send_messages(client, phone_numbers, message_type, message, image_path)
        print("Done")
    except Exception as e:
        print(f"An error occurred: {e}")

window.disable()

sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, keep_on_top=True)
blast(sanitized_phone_number_list,image_to_attach,message_to_send)
sg.popup_animated(None)
sg.popup('Done', keep_on_top=True)
window.close()
os._exit(0)