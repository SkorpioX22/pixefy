import turtle
from PIL import Image
import tkinter as tk
from tkinter import filedialog

# Function to convert 24-bit RGB color to 16-bit RGB 565
def rgb_to_16bit(color):
    r, g, b = color
    r = (r >> 3) & 0x1F  # 5 bits for red
    g = (g >> 2) & 0x3F  # 6 bits for green
    b = (b >> 3) & 0x1F  # 5 bits for blue
    return (r << 11) | (g << 5) | b

# Function to convert 16-bit RGB 565 back to RGB for Turtle
def bit16_to_rgb(color_16bit):
    r = ((color_16bit >> 11) & 0x1F) << 3
    g = ((color_16bit >> 5) & 0x3F) << 2
    b = (color_16bit & 0x1F) << 3
    return (r, g, b)

# Function to draw the image using Turtle
def draw_image_with_turtle(image, resolution, pixel_size=5, hide_turtle=True):
    # Set up Turtle
    turtle.speed(0)  # Fastest Turtle speed
    turtle.colormode(255)
    turtle.penup()

    # Hide or show the Turtle based on user selection
    if hide_turtle:
        turtle.hideturtle()
    else:
        turtle.showturtle()

    width, height = resolution, resolution
    start_x, start_y = -width // 2 * pixel_size, height // 2 * pixel_size  # Center image

    total_pixels = width * height  # Total number of pixels
    pixels_drawn = 0  # Pixels drawn counter

    for y in range(height):
        for x in range(width):
            # Get pixel color
            color = image.getpixel((x, y))
            color_16bit = rgb_to_16bit(color)  # Convert to 16-bit
            turtle_color = bit16_to_rgb(color_16bit)  # Convert back to 24-bit RGB for Turtle

            # Set Turtle color and move to position
            turtle.goto(start_x + x * pixel_size, start_y - y * pixel_size)
            turtle.fillcolor(turtle_color)
            turtle.begin_fill()

            # Draw pixel (as a square)
            for _ in range(4):
                turtle.forward(pixel_size)
                turtle.right(90)
            turtle.end_fill()

            # Update the count of drawn pixels
            pixels_drawn += 1
            pixels_left = total_pixels - pixels_drawn
            
            # Update the pixel count in the main window
            update_pixel_count(pixels_left)

    # Final update after all pixels are drawn
    update_pixel_count("Drawing complete!")

    # Keep the window open after drawing is done
    turtle.done()

# Function to update the pixel count in the Tkinter window
def update_pixel_count(pixels_left):
    count_label.config(text=f"Pixels left: {pixels_left}")

# Function to load image, ask for resolution, and run Turtle drawing
def start_drawing():
    # Ask the user to browse for an image
    image_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    
    if image_path:
        # Get the chosen resolution from the slider
        resolution = resolution_slider.get()

        # Check if turtle should be hidden
        hide_turtle = hide_turtle_var.get() == 1

        # Open the image and resize it to the selected resolution
        image = Image.open(image_path)
        image = image.convert("RGB")  # Ensure image is RGB format
        image = image.resize((resolution, resolution))  # Resize to user-selected resolution

        # Start the Turtle drawing
        draw_image_with_turtle(image, resolution, hide_turtle=hide_turtle)

# Function to create the main GUI window for selecting resolution, starting drawing, and showing pixel count
def create_main_gui():
    root = tk.Tk()
    root.title("Turtle Image Drawer")
    root.geometry("400x350")

    # Add a label for the title
    label = tk.Label(root, text="Select Resolution and Image:", font=("Courier", 14))
    label.pack(pady=10)

    # Add a slider for resolution selection (from 32x32 to 256x256)
    global resolution_slider
    resolution_slider = tk.Scale(root, from_=32, to_=256, orient=tk.HORIZONTAL, label="Resolution (px)", length=300, font=("Courier", 10))
    resolution_slider.set(128)  # Set default value to 128
    resolution_slider.pack(pady=10)

    # Add a checkbutton for hiding/showing the turtle
    global hide_turtle_var
    hide_turtle_var = tk.IntVar(value=1)  # Default is to hide the turtle
    hide_turtle_checkbutton = tk.Checkbutton(root, text="Hide Turtle", variable=hide_turtle_var, font=("Courier", 12))
    hide_turtle_checkbutton.pack(pady=10)

    # Add a button to browse for an image and start drawing
    browse_button = tk.Button(root, text="Browse Image and Start Drawing", command=start_drawing, font=("Courier", 12))
    browse_button.pack(pady=20)

    # Add a label to display the pixel count
    global count_label
    count_label = tk.Label(root, text="Pixels left: 0", font=("Courier", 12), fg="black")
    count_label.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_main_gui()
