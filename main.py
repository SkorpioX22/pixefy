import turtle
from PIL import Image, ImageOps, EpsImagePlugin
import tkinter as tk
from tkinter import filedialog, messagebox
import io

EpsImagePlugin.gs_windows_binary = r'C:\Program Files\gs\gs9.53.3\bin\gswin64c'  # Change path to your Ghostscript installation if necessary

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
def draw_image_with_turtle(image, resolution, pixel_size=5, hide_turtle=True, fast_mode=False):
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

    # Variables to handle fast mode (split image into 4 phases)
    fast_mode_thresholds = [total_pixels // 4, total_pixels // 2, 3 * total_pixels // 4, total_pixels]
    fast_mode_step = 0

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

            if not fast_mode or pixels_drawn >= fast_mode_thresholds[fast_mode_step]:
                update_pixel_count(pixels_left)
                if fast_mode_step < len(fast_mode_thresholds) - 1:
                    fast_mode_step += 1
                if fast_mode:
                    turtle.update()  # Manually update screen in fast mode

    # Final update after all pixels are drawn
    update_pixel_count("Drawing complete!")
    save_button.config(state=tk.NORMAL)  # Enable the Save button after drawing is complete
    if not fast_mode:
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

        # Check if fast mode is enabled
        fast_mode = fast_mode_var.get() == 1

        # Open the image and resize it to the selected resolution
        image = Image.open(image_path)
        image = image.convert("RGB")  # Ensure image is RGB format
        image = image.resize((resolution, resolution))  # Resize to user-selected resolution

        if fast_mode:
            turtle.tracer(0, 0)  # Disable real-time updates for fast mode
        else:
            turtle.tracer(1, 0)  # Restore default tracer settings

        # Start the Turtle drawing
        draw_image_with_turtle(image, resolution, hide_turtle=hide_turtle, fast_mode=fast_mode)

# Function to save the Turtle window as an image
def save_image():
    try:
        # Ask user where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png")])
        if file_path:
            # Save the Turtle drawing as EPS
            canvas = turtle.getcanvas()
            ps = canvas.postscript(colormode='color')
            
            # Convert EPS to PNG using PIL
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img.save(file_path, 'png')
            messagebox.showinfo("Success", f"Image saved successfully as {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save the image: {str(e)}")

# Function to create the main GUI window for selecting resolution, starting drawing, and showing pixel count
def create_main_gui():
    root = tk.Tk()
    root.title("Pixefy")
    root.geometry("500x600")

    # Add a label for the title
    label = tk.Label(root, text="Select Resolution and Image:", font=("Helvetica", 14))  # DM Sans-like clean font
    label.pack(pady=10)

    # Add a slider for resolution selection (from 32x32 to 256x256)
    global resolution_slider
    resolution_slider = tk.Scale(root, from_=32, to_=256, orient=tk.HORIZONTAL, label="Resolution (px)", length=300, font=("Helvetica", 10))
    resolution_slider.set(128)  # Set default value to 128
    resolution_slider.pack(pady=10)

    # Add a checkbutton for hiding/showing the turtle
    global hide_turtle_var
    hide_turtle_var = tk.IntVar(value=1)  # Default is to hide the turtle
    hide_turtle_checkbutton = tk.Checkbutton(root, text="Hide Turtle (Quickens Render)", variable=hide_turtle_var, font=("Helvetica", 12))
    hide_turtle_checkbutton.pack(pady=10)

    # Add a checkbutton for fast mode
    global fast_mode_var
    fast_mode_var = tk.IntVar(value=0)  # Default is not to use fast mode
    fast_mode_checkbutton = tk.Checkbutton(root, text="RapidRender (Nearly instant rendering)", variable=fast_mode_var, font=("Helvetica", 12))
    fast_mode_checkbutton.pack(pady=10)

    # Add a button to browse for an image and start drawing
    browse_button = tk.Button(root, text="Browse Image and Start Drawing", command=start_drawing, font=("Helvetica", 12))
    browse_button.pack(pady=20)

    # Add a label to display the pixel count
    global count_label
    count_label = tk.Label(root, text="Pixels left: 0", font=("Helvetica", 12), fg="black")
    count_label.pack(pady=10)

    # Add a button to save the final Turtle drawing as an image
    global save_button
    save_button = tk.Button(root, text="Save Image", command=save_image, font=("Helvetica", 12), state=tk.DISABLED)
    save_button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_main_gui()
