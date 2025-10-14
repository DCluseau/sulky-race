#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import randint

# Une course de trot attelé rassemble 12 à 20 chevaux, chacun tractant un sulky, et étant mené par un driver. Elle peut faire l’objet d’un tiercé, d’un quarté, ou d’un quinté. La course est supposée se dérouler sur un hippodrome rectiligne (chaque cheval disposant de son propre couloir), d’une longueur de 2 400 m. Il est à noter que chaque cheval doit respecter l’allure du trot de bout en bout, le passage au galop entrainant sa disqualification. L’utilisateur saisit au démarrage le nombre de chevaux et le type de la course.
# La course se déroule à la manière d’un « jeu de plateau » : à chaque tour de jeu, chaque cheval fait l’objet d’un jet de dé (à 6 faces), qui décide d’une altération possible de sa vitesse (augmentation, stabilisation, diminution). La nouvelle vitesse détermine alors la distance dont il avance. Chaque tour de jeu représente 10 secondes du déroulement de la course, mais le temps ne sera pas rendu dans le programme. C’est l’utilisateur qui fera avancer la course de tour en tour, à la suite d’un message du programme l’y invitant.

RACE_TYPE = [3, 4, 5]
MIN_NB_HORSES = 12
MAX_NB_HORSES = 20
RACETRACK_LENGTH = 2400
MIN_DICE = 1
MAX_DICE = 6
race_choice = 0
nb_horses = 0
horse_list = []
total_distance = 0
ranking = []

# Type of race choice
def choose_race():
    """

    :return:
    """
    nb = 0
    while nb not in RACE_TYPE:
        try:
            nb = int(input("Choose the type of race : \n 3 - Tiercé\n 4 - Quarté\n 5 - Quinté\n"))
        except ValueError:
            print("Error : must choose a number between 3 and 5.")
            nb = 0
    return nb

# Number of horses
def choose_horses_number():
    """
    Usage : choose a number of horses
    :return:
    """
    nb = 0
    while nb not in range(MIN_NB_HORSES, MAX_NB_HORSES + 1):
        try:
            nb = int(input("Choose how much horses will do the race : \n"))
        except ValueError:
            print("Error : must choose a number between 12 and 20.")
            nb = 0
    return nb

# Throw dice
def throw_dice():
    """

    :return:
    """
    result = randint(MIN_DICE,MAX_DICE + 1)
    return result

# Add horse to list
def add_horse(arr_horses, num):
    """
    Usage : add horse to horses list
    :param arr_horses:
    :return:
    """
    horse = {"number" : num, "speed" : 0, "distance" : 0, "dq" : False}
    arr_horses.append(horse)
    return arr_horses

# Calculate speed
def calculate_speed(dice_result, current_speed):
    """

    :param current_speed:
    :param dice_result:
    :return:
    """
    speed_modifier = 0
    match dice_result:
        case 1:
            match current_speed:
                case 0, 1, 2 :
                    speed_modifier = 0
                case 3, 4 :
                    speed_modifier = -1
                case 5, 6 :
                    speed_modifier = -2
        case 2:
            match current_speed:
                case 0 :
                    speed_modifier = 1
                case 1, 2, 3, 4:
                    speed_modifier = 0
                case 5, 6:
                    speed_modifier = -1
        case 3:
            match current_speed:
                case 0, 1, 2:
                    speed_modifier = 1
                case 3, 4, 5, 6:
                    speed_modifier = 0
        case 4:
            match current_speed:
                case 0, 1, 2, 3, 4:
                    speed_modifier = 1
                case 5, 6:
                    speed_modifier = 0
        case 5:
            match current_speed:
                case 0:
                    speed_modifier = 2
                case 1, 2, 3, 4:
                    speed_modifier = 1
                case 5, 6:
                    speed_modifier = 0
        case 6:
            match current_speed:
                case 0, 1, 2:
                    speed_modifier = 2
                case 3, 4, 5:
                    speed_modifier = 1
                case 6:
                    speed_modifier = 3
    return speed_modifier

# Update horse speed
def update_horse_speed(speed_init, speed_updater):
    """

    :param speed_init:
    :param speed_updater:
    :return:
    """
    new_speed = speed_init + speed_updater
    return new_speed

# Update distance
def update_horse_distance(init_distance, updated_speed):
    """

    :param init_distance:
    :param updated_speed:
    :return:
    """
    new_distance = init_distance + (3 * updated_speed)
    return new_distance

# Calculate the total distance the horses ran
def calculate_total_distance(horses_list):
    """

    :param horses_list:
    :return:
    """
    max_distance = 0
    for k in range(len(horses_list)):
        if horses_list[k]["distance"] > max_distance and horses_list[k]["dq"] == False:
            max_distance = horses_list[k]["distance"]
    return max_distance

# Rank horses
def rank_horses(horse_rank):
    """

    :param horse_rank:
    :return:
    """
    return horse_rank["distance"]

# Choose race
race_choice = choose_race()

# Choose number of horses
nb_horses = choose_horses_number()

# Fill the horses list
for i in range(nb_horses):
    horse_list = add_horse(horse_list, i)

# Begin race
while total_distance < RACETRACK_LENGTH:
    # For each horse, throw dice
    for j in range(nb_horses):
        if not horse_list[j]["dq"]:
            dice_res = throw_dice()
            # Search speed modifier
            modifier_speed = calculate_speed(dice_res, horse_list[j]["speed"])
            if modifier_speed < 3:
                # Update horse speed
                horse_list[j]["speed"] = update_horse_speed(horse_list[j]["speed"], modifier_speed)
                # Update distance
                horse_list[j]["distance"] = update_horse_distance(horse_list[j]["distance"], horse_list[j]["speed"])
            else:
                horse_list[j]["dq"] = True
    # Add distance to total
    total_distance = calculate_total_distance(horse_list)
print("Terminé !")
print("Classement :")

# Find race_choice ranking
horse_list.sort(reverse=True, key=rank_horses(horse_list))
for i in range(race_choice):
    print(f"Horse number : {horse_list[i]["num"]}\n Distance : {horse_list[i]["distance"]}")