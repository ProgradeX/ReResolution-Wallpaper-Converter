from PIL import Image


input_image = Image.open("input.png")
size = input_image.size

# Crop the input image to 3425x1200 pixels
if (size[0] < 3425) and (size[1] < 1200):
    exit

else:
    xStart = (size[0] - 3425) / 2
    yStart = (size[1] - 1200) / 2
    
    xOffset , yOffset = 0, -100

    cropped_image = input_image.crop((xStart + xOffset, yStart + yOffset, xStart + 3425 + xOffset, yStart + 1200 + yOffset))


# Select the area (2035, 0) to (3325, 1111) and scale it to 1283x1024 pixels
selected_area = cropped_image.crop((2035, 0, 3425, 1111))

monitorOne = cropped_image.crop((0, 0, 1920, 1200))
monitorTwo = selected_area.resize((1280, 1024))

# Move the scaled image after 1920 pixels
new_image = Image.new('RGB', (3200, 1200))
new_image.paste(monitorOne, (0, 0))
new_image.paste(monitorTwo, (1920, 0))

new_image.save("output.png")