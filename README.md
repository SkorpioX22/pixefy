# pixefy
an image redraw system to make it blurry. powered by Python.

# How does pixefy work?
- Load and Resize the Image:

After the user selects an image, the program loads it using Pillow (PIL.Image) and resizes it to the user-selected resolution (e.g., 128x128 pixels).
Pixel Color Extraction:

- The program loops over each pixel of the resized image.
It gets the color of each pixel using image.getpixel() and converts the 24-bit RGB color to 16-bit (RGB 565) to reduce color complexity.
Position Turtle:

- Turtle is positioned to draw each "pixel" as a small square.
The top-left corner of the image is calculated, and Turtle moves to each pixel position by adjusting its x and y coordinates.
Set Color and Draw:

- For each pixel, the color is converted back from 16-bit to 24-bit (so Turtle can use it), and Turtle fills a small square with that color.
The size of the square is determined by a pixel_size variable, which remains constant.
Repeat for Each Pixel:

The process repeats for all pixels in the image, creating a grid of colored squares, which recreates the image using Turtle's drawing capabilities.
Pixel Count:

As Turtle draws each pixel, the program updates the pixel count, showing how many pixels are left to draw.
