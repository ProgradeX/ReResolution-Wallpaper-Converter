from PIL import Image

class monitor():
    def __init__(self, width_cm, height_cm, width_px, height_px):
        self.above = None
        self.below = None
        self.left = None
        self.right = None

        self.width = width_cm
        self.height = height_cm
        self.res_x = width_px
        self.res_y = height_px
        return


class monitor_config():
    def __init__(self) -> None:
        self.anchor = None
        # self.direction = {'up': 0, 'down': 1, 'left': 2, 'right': 3}
        pass

        # wow this is some really bad code but dw ill totally not forget and fix this
    def show_config(self):
        print('ANCR->', self.anchor.res_x, self.anchor.res_y)
        if self.anchor.above:
            print('ABOV->', self.anchor.above.res_x, self.anchor.above.res_y)
        if self.anchor.below:
            print('BELW->', self.anchor.below.res_x, self.anchor.below.res_y)
        if self.anchor.left:
            print('LEFT->', self.anchor.left.res_x, self.anchor.left.res_y)
        if self.anchor.right:
            print('RIGT->', self.anchor.right.res_x, self.anchor.right.res_y)
        


    def add_panel(self, panel, direction = None):
        if self.anchor is None:
            print('is anchor')
            # set monitor to anchor
            self.anchor = panel

        elif direction is not None:
            print('has a direction')
            # set monitor next to anchor
            if direction == 'above':
                self.anchor.above = panel
            elif direction == 'below':
                self.anchor.below = panel
            elif direction == 'left':
                self.anchor.left = panel
            elif direction == 'right':
                self.anchor.right = panel
            else:
                print('wat')

        else:
            print('bruh')

        return


def calculate_scale():
    num_monitors = 2 # 2 by default
    sizes = []
    resolutions = []
    density = []
    scaling = []
    for x in range(num_monitors):
        print('monitor ', x)
        cm_width = float(input('Enter width of monitor (in cm): '))
        cm_height = float(input('Enter height of monitor (in cm): '))
        sizes.append((cm_width, cm_height))

        width = int(input('Enter width of monitor (in pixels): '))
        height = int(input('Enter height of monitor (in pixels): '))
        resolutions.append((width, height))

        density_x = round(width/cm_width, 3)
        density_y = round(height/cm_height, 3)

        if density_x != density_y:
            print('WARNING: monitor ', x, ' does not have 1:1 pixels, transformation may be biased')

        density.append(density_y)
    

    # bubble sorting all the arrays by highest density to lowest density
    n = num_monitors
    for i in range(n):
        for j in range(0, n - i - 1):
            if density[j] < density[j + 1]:
                density[j], density[j + 1] = density[j + 1], density[j]
                sizes[j], sizes[j + 1] = sizes[j + 1], sizes[j]
                resolutions[j], resolutions[j + 1] = resolutions[j + 1], resolutions[j]


    scaled_resolutions = []
    for x in range(num_monitors):
        scaling.append(density[0] / density[x])     # highest density display
        scale = (int(resolutions[x][0] * scaling[x]), int(resolutions[x][1] * scaling[x]))
        scaled_resolutions.append(scale)

    print(scaled_resolutions)
    return resolutions, scaled_resolutions
    

def main():
    input_image = Image.open("input.png")
    size = input_image.size

    res, scaled_res = calculate_scale()

    #Crop the input image to 3425x1200 pixels
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
    return


# CODE STARTS HERE

m1 = monitor(51, 30, 1920, 1200)
m2 = monitor(51, 30, 1920, 1650)
config = monitor_config()

config.add_panel(m1)
config.add_panel(m2, 'above')

config.show_config()
