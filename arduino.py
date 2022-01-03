import serial
import math


class Food:
    def __init__(self, weight, position):
        self.weight = weight
        self.position = position


def adjust_list(array):  # a function to adjust arduino data, because arduino data is obtained as string
    for i in range(0, 5):
        array[i] = float(array[i])
    position = array[-1].split(",")
    try:
        position[-1] = float(position[-1])
        position[-2] = float(position[-2])
    except:  # pass if the position info is 'nan' or 'inf'
        pass
    array[-1] = position
    return array


def check_for_changes(list1, list2):
    if not math.isclose(list1[4], list2[4], rel_tol=1e-1):  # check if TOTAL weight has changed considerably
        if list1[4] > list2[4]:
            return 1  # total has weight increased, a new food has placed
        else:
            return -1  # total has weigh decreased, a food has removed

    for i in [0, 1, 2, 3]:  # toplam ağırlıkta değişim yoksa buraya gelir
        if not math.isclose(list1[i], list2[i], rel_tol=0.5):  # köşelerde değişim olmuş mu diye bakar
            return 2  # toplam ağırlıkta değişim olmamış fakat konum değişikliği olmuş

    else:
        return 0  # nothing changed


def calc_center_of_gravity(new_data, prev_data):
    x_max = 69.0
    y_max = 50.0
    f2 = new_data[1] - prev_data[1]
    f3 = new_data[2] - prev_data[2]
    f4 = new_data[3] - prev_data[3]
    f_max = new_data[4] - prev_data[4]  # total weight of the object
    x_coordinate = (f2 + f3) * x_max / f_max
    y_coordinate = (f3 + f4) * y_max / f_max
    return f_max, [x_coordinate, y_coordinate]


def match_weight(search_weight, search_coordinate):
    for name, food in holder.items():
        if search_coordinate == food.position:
            food.weight = search_weight


food_count = 0

counter = 0
instanceNames = ['food_1', 'food_2', 'food_3', 'food_4', 'food_5', 'food_6', 'food_7', 'food_8', 'food_9', 'food_10']
holder = {name: Food(0.0, (0.0, 0.0)) for name in instanceNames}


def add_new_food(new_data, prev_data):
    global counter
    counter += 1
    weight, position = calc_center_of_gravity(new_data, prev_data)
    holder[instanceNames[counter - 1]].weight = weight
    holder[instanceNames[counter - 1]].position = position


def remove_food(new_data, prev_data):
    if type(new_data[-1][0]) or type(new_data[-1][1]) != float:
        new_data[-1][0] = 0.0
        new_data[-1][1] = 0.0
    prev_data[-1][0] = float(prev_data[-1][1])
    prev_data[-1][1] = float(prev_data[-1][2])
    weight, coordinates = calc_center_of_gravity(prev_data, new_data)
    for name, food in holder.items():
        if math.isclose(coordinates[0], food.position[0], rel_tol=0.4) and math.isclose(coordinates[1],
                                                                                        food.position[1], rel_tol=0.4):
            food.weight = 0.0
            food.position = (0.0, 0.0)


def update_food(new_data, prev_data):
    weight, coordinates = calc_center_of_gravity(new_data, prev_data)
    for name, food in holder.items():
        if weight == food.weight:
            food.position = coordinates


arduino = serial.Serial('COM4', timeout=1, baudrate=9600)
# str = "HX711 readings: 0	0	0	0	Total weight: 0	|	Position as (x,y): nan,nan"
# values = ['0', '0', '0', '0', '0', '(nan,nan)']

# Read and record the data
data = [[0.0, 0.0, 0.0, 0.0, 0.0, ['nan', 'nan']],
        [0.0, 0.0, 0.0, 0.0, 0.0, ['nan', 'nan']]]  # empty list to store the data


while food_count <= 2:
    b = arduino.readline()  # read a byte string
    string_n = b.decode()  # decode byte string into Unicode
    string = string_n.rstrip().split()  # remove \n and \r
    try:
        values = [string[i] for i in [2, 3, 4, 5, 8, 13]]  # extract necessary values from the string
        values = adjust_list(values)
        data.append(values)  # add to the end of data list
        print(data[-1])
        check = check_for_changes(data[-1], data[-2])
        if check == 1:
            print("artis var")
            food_count += 1
            add_new_food(data[-1], data[-2])
        elif check == 2:
            print("biseyin yeri degisti")
            update_food(data[-1], data[-2])
        elif check == 0:
            print("degisiklik yok")
        else:
            print("azalma var")
            food_count -= 1
        for name, food in holder.items():
            if food.weight != 0.0:
                print(food.weight, food.position)
    except:
        print(string_n.rstrip())
    # time.sleep(3)

arduino.close()
