#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import os
from tkinter import Tk, Label
from PIL import ImageTk, Image, ImageOps
from tkinter import ttk
import time

# Function to convert numeric countdown to words
def number_to_words(number):
    if number == 0:
        return "zero"
    elif number == 1:
        return "one"
    elif number == 2:
        return "two"
    elif number == 3:
        return "three"
    elif number == 4:
        return "four"
    elif number == 5:
        return "five"
    elif number == 6:
        return "six"
    elif number == 7:
        return "seven"
    elif number == 8:
        return "eight"
    elif number == 9:
        return "nine"
    else:
        return str(number)

# Set the API endpoint and parameters; All are optional
# https://wallhaven.cc/help/api For information on each parameter
# Including any that I didn't include
api_url = 'https://wallhaven.cc/api/v1/search'
params = {
    #'categories': '100',  # 100 corresponds to general wallpapers
    #'sorting': 'random',  # You can change the sorting method if desired
    #'apikey': '[YOUR_API]',  # Replace with your Wallhaven API key - Only really needed for NSFW results
    #'page': '1',  # Page number of the results
    #'seed': '[RANDOM STRING]', #Seed to ensure pseudo-random results
    #'atleast': '1920x1080', #Make sure the images are at least this size.
    #'resolutions': '1920x1080', #Strictly enforce the resolution
    #'ratios': '16x9', #16x10 is the other option
    #'q': 'nature',  # Search query (e.g., 'nature', 'space', etc.)
    #'purity': '100' #100/110/111/etc (sfw/sketchy/nsfw)
}

# Send a GET request to the Wallhaven API
response = requests.get(api_url, params=params)
data = response.json()

# Create a directory to store the downloaded images
directory = 'wallpapers'
if not os.path.exists(directory):
    os.makedirs(directory)

# Retrieve the list of existing images and delete the last 20.
#This is a variable incase someone, myself, decides death by a thousand cuts is a good idea.
existing_images = os.listdir(directory)
existing_images.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)))
num_existing_images = len(existing_images)
if num_existing_images >= 20:
    oldest_images = existing_images[:20]
    for image in oldest_images:
        image_path = os.path.join(directory, image)
        os.remove(image_path)

# Download images from the API response
num_images_to_download = min(20, len(data['data']))
window = Tk()
window.title('Image Downloader')
window.attributes('-fullscreen', True)
window.config(cursor="none")

# Define style for the progress bar
style = ttk.Style()
style.configure("TProgressbar",
                thickness=20,
                troughcolor='#D9D9D9',
                bordercolor='#D9D9D9',
                background='#69A8BB',
                troughrelief='flat',
                relief='flat')

# Create the progress bar
progress_bar = ttk.Progressbar(window, style="TProgressbar", orient='horizontal', mode='determinate')
progress_bar.place(x=50, y=window.winfo_screenheight() - 50, width=window.winfo_screenwidth() - 100, height=30)

# Initialize the first image dimensions
image_width, image_height = window.winfo_screenwidth(), window.winfo_screenheight()

for i in range(num_images_to_download):
    wallpaper = data['data'][i]
    image_url = wallpaper['path']
    image_name = wallpaper['id'] + '.' + wallpaper['file_type'].split('/')[-1]
    image_path = os.path.join(directory, image_name)

    progress_label = Label(window, text='Downloading image ' + str(i + 1) + ' of ' + str(num_images_to_download) + '...',
                           font=('Arial', 14))
    progress_label.place(x=50, y=window.winfo_screenheight() - 100, width=window.winfo_screenwidth() - 100, height=30)
    window.update()

    image_response = requests.get(image_url)
    with open(image_path, 'wb') as image_file:
        image_file.write(image_response.content)

    # Display the downloaded image in a full-screen window
    image = Image.open(image_path)
    image = image.resize((image_width, image_height))  # Resize the image to match the screen size
    image.thumbnail((window.winfo_screenwidth(), window.winfo_screenheight()), Image.LANCZOS)

    # Create a blank image with the same size and mode as the screen
    blank_image = Image.new('RGB', (window.winfo_screenwidth(), window.winfo_screenheight()), (255, 255, 255))

    # Create a blended image with a smooth transition
    blended_image = Image.alpha_composite(blank_image.convert('RGBA'), image.convert('RGBA'))

    photo = ImageTk.PhotoImage(blended_image)
    label = Label(window, image=photo)
    label.image = photo
    label.place(x=0, y=0, relwidth=1, relheight=1)
    window.update()

    # Update the dimensions for the next image
    image_width, image_height = image.size



    # Update the progress bar
    progress_value = (i + 1) / num_images_to_download * 100
    progress_bar["value"] = progress_value
    window.update()


# 6-second countdown
for countdown in range(6, 0, -1):
    countdown_label = Label(window, text=f'All set! Closing automatically in {number_to_words(countdown)}...',
                            font=('Arial', 14))
    countdown_label.place(x=50, y=window.winfo_screenheight() - 100, width=window.winfo_screenwidth() - 100, height=30)
    window.update()
    time.sleep(1)
    countdown_label.destroy()
window.destroy()
window.quit()
