from PIL import Image


class monitor():
    def __init__(self, width_cm, height_cm, width_px, height_px, total_id):
        self.links = {
            'top': None,
            'bottom': None,
            'left': None,
            'right': None
        }
        self.id = total_id

        self.width = width_cm
        self.height = height_cm
        self.res_x = width_px
        self.res_y = height_px

        print("new monitor created with id:", self.id)

    def link_monitor(self, monitor, direction):
        self.links[direction] = monitor

    def get_linked(self, direction):
        return self.links[direction]


class monitor_config():
    def __init__(self) -> None:
        self.monitors = {}
        pass

    def add_monitor(self, monitor):
        self.monitors[monitor.id] = monitor

    def get_monitor(self, id):
        return self.monitors.get(id)

    def connect_monitors(self, id1, direction1, id2, direction2):
        node1 = self.get_monitor(id1)
        node2 = self.get_monitor(id2)
        if node1 and node2:
            node1.link_monitor(node2, direction1)
            node2.link_monitor(node1, direction2)
        else:
            raise ValueError("One or both nodes do not exist")

    def get_connected_monitor(self, id, direction):
        node = self.get_monitor(id)
        if node:
            return node.get_linked(direction)
        else:
            raise ValueError("Node does not exist in the graph.")
    
    def show_configuration(self):
        for id, monitor in self.monitors.items():
            print("\nmonitor: ", id, end=", \n")
            for direction, connected_monitor in monitor.links.items():
                if connected_monitor:
                    print(direction, " : ", connected_monitor.id, end='     \n')



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

m1 = monitor(51, 30, 1920, 1200, 0)
m2 = monitor(51, 30, 1920, 1650, 1)

config = monitor_config()

config.add_monitor(m1)
config.add_monitor(m2)

config.connect_monitors(0, 'right', 1, 'left')

config.show_configuration()
