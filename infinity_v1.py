import random
import requests
from tabulate import tabulate
from decimal import Decimal
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set your own secret key
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Define the symbols for each reel
reel1 = ['S1', 'W1', 'W4', 'W3', 'W2', 'W1', 'S3', 'W3', 'W4', 'W2',
         'S2', 'W1', 'W2', 'S4', 'W3', 'W2', 'W4', 'S1', 'W2', 'W4', 
         'W3', 'FS', 'W2', 'W1', 'S2', 'W2', 'W4', 'W3', 'S4', 'W4', 
         'W1', 'W2', 'W3', 'S1', 'W1', 'W4', 'W2', 'S3', 'W3', 'W1', 
         'FS', 'W4', 'W1', 'W3', 'W2', 'W4', 'S2', 'W4', 'W3', 'W1', 
         'S1', 'W2', 'W4', 'W3', 'S3', 'W2', 'W3', 'FS', 'W2', 'W4', 
         'W1', 'S4', 'W3', 'W2', 'W3', 'S4', 'W1', 'W4', 'S3', 'W4', 
         'W2', 'W4', 'W1', 'S2', 'W2', 'W1', 'W3', 'S4', 'W3', 'W4', 
         'W1', 'W2', 'FS', 'W4', 'W1', 'W3', 'W4', 'W1', 'S3', 'W2', 
         'W1', 'W3', 'W4', 'FS', 'W2', 'W1', 'W3', 'S4', 'W3', 'W4']

reel2 = ['S1', 'W2', 'W4', 'FS', 'W4', 'W1', 'W2', 'S4', 'W4', 'W3',
         'S2', 'W1', 'W2', 'W4', 'W3', 'W2', 'S3', 'W1', 'W3', 'W4', 
         'S4', 'W2', 'W3', 'W1', 'S4', 'W2', 'W3', 'W4', 'W2', 'FS', 
         'W3', 'W2', 'W4', 'S2', 'W1', 'W3', 'W2', 'S1', 'W1', 'W3', 
         'W2', 'W1', 'S3', 'W2', 'W4', 'W1', 'S2', 'W4', 'W3', 'S3', 
         'W4', 'W1', 'FS', 'W3', 'W1', 'W3', 'S3', 'W4', 'W2', 'S1', 
         'W1', 'W3', 'W4', 'S4', 'W3', 'W1', 'W4', 'S2', 'W1', 'W3', 
         'W2', 'W4', 'S3', 'W3', 'W1', 'FS', 'W2', 'W4', 'W3', 'W2', 
         'W1', 'W4', 'W2', 'W4', 'W1', 'W3', 'S4', 'W4', 'W2', 'S1', 
         'W1', 'W4', 'W3', 'S4', 'W2', 'W1', 'FS', 'W4', 'W2', 'W3']

reel3 = ['S1', 'W2', 'W4', 'S4', 'W3', 'W2', 'W4', 'W3', 'S4', 'W2',
         'W4', 'W1', 'S2', 'W3', 'W4', 'W2', 'S3', 'W1', 'W2', 'FS', 
         'W1', 'W4', 'W2', 'S3', 'W3', 'W2', 'W4', 'W3', 'W1', 'S1', 
         'W4', 'W2', 'S1', 'W3', 'W1', 'W4', 'S4', 'W1', 'W3', 'S3', 
         'W4', 'W1', 'W3', 'W2', 'W1', 'W3', 'S2', 'W4', 'W3', 'W1', 
         'FS', 'W2', 'W4', 'FS', 'W1', 'W2', 'W3', 'S2', 'W2', 'W3', 
         'S3', 'W4', 'W1', 'FS', 'W4', 'W1', 'W3', 'S3', 'W1', 'W3', 
         'W2', 'W4', 'S4', 'W3', 'W2', 'W1', 'W4', 'S1', 'W3', 'W2', 
         'W1', 'W4', 'S4', 'W4', 'W2', 'W3', 'W4', 'S2', 'W4', 'W2', 
         'W1', 'W4', 'S4', 'W3', 'W2', 'W1', 'FS', 'W2', 'W3', 'W1']

reel4 = ['S1', 'W3', 'W2', 'W4', 'W1', 'W3', 'W4', 'S4', 'W4', 'W2',
         'S2', 'W1', 'W3', 'W4', 'S2', 'W2', 'W4', 'W1', 'W2', 'S4', 
         'W1', 'W3', 'W2', 'S3', 'W4', 'W2', 'W3', 'S3', 'W2', 'W4', 
         'W3', 'W2', 'S1', 'W3', 'W1', 'W4', 'W2', 'S2', 'W1', 'W2', 
         'W4', 'W1', 'W4', 'W2', 'S1', 'W3', 'W2', 'W4', 'W3', 'W1', 
         'W4', 'W2', 'S4', 'W3', 'W1', 'W3', 'S3', 'W4', 'W2', 'W3', 
         'S3', 'W1', 'W4', 'S4', 'W3', 'W1', 'W2', 'W3', 'W1', 'W4', 
         'S3', 'W2', 'W1', 'W4', 'W3', 'W1', 'S2', 'W4', 'W3', 'W2', 
         'W1', 'W4', 'S4', 'W4', 'W1', 'S1', 'W3', 'W4', 'W2', 'W3', 
         'W1', 'W4', 'W3', 'S4', 'W2', 'W1', 'W3', 'W4', 'W3', 'W2']


# Change the number of spins in the range below
def spin_reel(reel):
    starting_index = random.randint(0, len(reel) - 1)  # Select a random starting index for the given reel
    result = []
    for i in range(4):
        index = (starting_index + i) % len(reel)
        result.append(reel[index])
    return result

def display_results(results):
    table = []
    for i in range(4):
        row = []
        for result in results:
            row.append(result[i])
        table.append(row)
    return table

#def display_results_freespin(results_freespin):
#    table = []
#    for i in range(3):
#        row = []
#        for result in results_freespin:
#            row.append(result[i])
#        table.append(row)
#    return table

# Make it equals zero:
#results_freespin = display_results_freespin([['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
#                                             ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
#                                             ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
#                                             ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
#                                             ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']])

@app.route('/')
def index_infinity_v1():
    #if 'countegg' not in session:
    #    session['countegg'] = 0
    #countegg = session['countegg']

    # Spin the reels
    result1 = spin_reel(reel1)
    result2 = spin_reel(reel2)
    result3 = spin_reel(reel3)
    result4 = spin_reel(reel4)

    # print("quinta coluna=", result5)

    # Reels for the V Feature
    #result6 = [""] * 5
    #result7 = [""] * 5
    #result8 = [""] * 5
    #result9 = [""] * 5
    #result10 = [""] * 5
    #result11 = [""] * 3
    #result12 = [""] * 3
    #result13 = [""] * 3
    #result14 = [""] * 3
    #result15 = [""] * 3
    #result16 = [""] * 3
    #result17 = [""] * 3
    #result18 = [""] * 3
    #result19 = [""] * 3
    #result20 = [""] * 3
    #result21 = [""] * 3
    #result22 = [""] * 3
    #result23 = [""] * 3
    #result24 = [""] * 3
    #result25 = [""] * 3
    #result26 = [""] * 3
    #result27 = [""] * 3
    #result28 = [""] * 3
    #result29 = [""] * 3
    #result30 = [""] * 3
    #result31 = [""] * 3
    #result32 = [""] * 3
    #result33 = [""] * 3
    #result34 = [""] * 3
    #result35 = [""] * 3
    #result36 = [""] * 3
    #result37 = [""] * 3
    #result38 = [""] * 3
    #result39 = [""] * 3
    #result40 = [""] * 3
    #result41 = [""] * 3
    #result42 = [""] * 3
    #result43 = [""] * 3
    #result44 = [""] * 3
    #result45 = [""] * 3
    #result46 = [""] * 3
    #result47 = [""] * 3
    #result48 = [""] * 3
    #result49 = [""] * 3
    #result50 = [""] * 3
    #result51 = [""] * 3
    #result52 = [""] * 3
    #result53 = [""] * 3
    #result54 = [""] * 3
    #result55 = [""] * 3
    #result56 = [""] * 3
    #result57 = [""] * 3
    #result58 = [""] * 3
    #result59 = [""] * 3
    #result60 = [""] * 3


    ## Evaluating the number D1+D2+D3+D4 in the Main Game
    #numofdinitial = 0
    #for i in range(3):
    #    if result1[i] == 'D1' or result1[i] == 'D2' or result1[i] == 'D3' or result1[i] == 'D4':
    #        numofdinitial += 1
    #    if result2[i] == 'D1' or result2[i] == 'D2' or result2[i] == 'D3' or result2[i] == 'D4':
    #        numofdinitial += 1
    #    if result3[i] == 'D1' or result3[i] == 'D2' or result3[i] == 'D3' or result3[i] == 'D4':
    #        numofdinitial += 1
    #    if result4[i] == 'D1' or result4[i] == 'D2' or result4[i] == 'D3' or result4[i] == 'D4':
    #        numofdinitial += 1
    #    if result5[i] == 'D1' or result5[i] == 'D2' or result5[i] == 'D3' or result5[i] == 'D4':
    #        numofdinitial += 1

    # print("Number of D1+D2+D3+D4: ", numofdinitial)

    #numofd = numofdinitial

    # Line wins counter

    W1_4 = 0
    W1_3 = 0

    W2_4 = 0
    W2_3 = 0

    W3_4 = 0
    W3_3 = 0

    W4_4 = 0
    W4_3 = 0

    S1_4 = 0
    S1_3 = 0
    S1_2 = 0

    S2_4 = 0
    S2_3 = 0
    S2_2 = 0

    S3_4 = 0
    S3_3 = 0
    S3_2 = 0

    S4_4 = 0
    S4_3 = 0
    S4_2 = 0

    # Infinity main game paytable
    # Line win payments
    S1_4pay = 30
    S2_4pay = 30
    S3_4pay = 30
    S4_4pay = 30
    W1_4pay = 5  
    W2_4pay = 5  
    W3_4pay = 5
    W4_4pay = 5

    S1_3pay = 8
    S2_3pay = 8
    S3_3pay = 8
    S4_3pay = 8
    W1_3pay = 2
    W2_3pay = 2
    W3_3pay = 2
    W4_3pay = 2

    S1_2pay = 2
    S2_2pay = 2
    S3_2pay = 2
    S4_2pay = 2

    payment = 0

    #for n in range(0,3):
    #    exec(f'winline{n} = 0')

    # Check for line winning condition
    # W1 Beggining in 0
    if 'W1' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 W1")
        W1_4 += 1

    elif 'W1' == result1[0] == result2[0] == result3[0] or 'W1' == result2[0] == result3[0] == result4[0]:
        print("000 W1")
        W1_3 += 1

    # W1 Beggining in 1
    if 'W1' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 W1")
        W1_4 += 1

    elif 'W1' == result1[1] == result2[1] == result3[1] or 'W1' == result2[1] == result3[1] == result4[1]:
        print("111 W1")
        W1_3 += 1

    # W1 Beggining in 2
    if 'W1' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 W1")
        W1_4 += 1

    elif 'W1' == result1[2] == result2[2] == result3[2] or 'W1' == result2[2] == result3[2] == result4[2]:
        print("222 W1")
        W1_3 += 1

    # W1 Beggining in 3
    if 'W1' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 W1")
        W1_4 += 1

    elif 'W1' == result1[3] == result2[3] == result3[3] or 'W1' == result2[3] == result3[3] == result4[3]:
        print("333 W1")
        W1_3 += 1

    # W2 Beggining in 0
    if 'W2' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 W2")
        W2_4 += 1

    elif 'W2' == result1[0] == result2[0] == result3[0] or 'W2' == result2[0] == result3[0] == result4[0]:
        print("000 W2")
        W2_3 += 1

    # W2 Beggining in 1
    if 'W2' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 W2")
        W2_4 += 1

    elif 'W2' == result1[1] == result2[1] == result3[1] or 'W2' == result2[1] == result3[1] == result4[1]:
        print("111 W2")
        W2_3 += 1

    # W2 Beggining in 2
    if 'W2' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 W2")
        W2_4 += 1

    elif 'W2' == result1[2] == result2[2] == result3[2] or 'W2' == result2[2] == result3[2] == result4[2]:
        print("222 W2")
        W2_3 += 1

    # W2 Beggining in 3
    if 'W2' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 W2")
        W2_4 += 1

    elif 'W2' == result1[3] == result2[3] == result3[3] or 'W2' == result2[3] == result3[3] == result4[3]:
        print("333 W2")
        W2_3 += 1

    # W3 Beggining in 0
    if 'W3' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 W3")
        W3_4 += 1

    elif 'W3' == result1[0] == result2[0] == result3[0] or 'W3' == result2[0] == result3[0] == result4[0]:
        print("000 W3")
        W3_3 += 1

    # W3 Beggining in 1
    if 'W3' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 W3")
        W3_4 += 1

    elif 'W3' == result1[1] == result2[1] == result3[1] or 'W3' == result2[1] == result3[1] == result4[1]:
        print("111 W3")
        W3_3 += 1

    # W3 Beggining in 2
    if 'W3' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 W3")
        W3_4 += 1

    elif 'W3' == result1[2] == result2[2] == result3[2] or 'W3' == result2[2] == result3[2] == result4[2]:
        print("222 W3")
        W3_3 += 1

    # W3 Beggining in 3
    if 'W3' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 W3")
        W3_4 += 1

    elif 'W3' == result1[3] == result2[3] == result3[3] or 'W3' == result2[3] == result3[3] == result4[3]:
        print("333 W3")
        W3_3 += 1

    # W4 Beggining in 0
    if 'W4' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 W4")
        W4_4 += 1

    elif 'W4' == result1[0] == result2[0] == result3[0] or 'W4' == result2[0] == result3[0] == result4[0]:
        print("000 W4")
        W4_3 += 1

    # W4 Beggining in 1
    if 'W4' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 W4")
        W4_4 += 1

    elif 'W4' == result1[1] == result2[1] == result3[1] or 'W4' == result2[1] == result3[1] == result4[1]:
        print("111 W4")
        W4_3 += 1

    # W4 Beggining in 2
    if 'W4' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 W4")
        W4_4 += 1

    elif 'W4' == result1[2] == result2[2] == result3[2] or 'W4' == result2[2] == result3[2] == result4[2]:
        print("222 W4")
        W4_3 += 1

    # W4 Beggining in 3
    if 'W4' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 W4")
        W4_4 += 1

    elif 'W4' == result1[3] == result2[3] == result3[3] or 'W4' == result2[3] == result3[3] == result4[3]:
        print("333 W4")
        W4_3 += 1

    # S1 Beggining in 0
    if 'S1' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 S1")
        S1_4 += 1

    elif 'S1' == result1[0] == result2[0] == result3[0] or 'S1' == result2[0] == result3[0] == result4[0]:
        print("000 S1")
        S1_3 += 1

    elif 'S1' == result1[0] == result2[0] or 'S1' == result3[0] == result4[0]:
        print("00 S1")
        S1_2 += 1       

    # S1 Beggining in 1
    if 'S1' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 S1")
        S1_4 += 1

    elif 'S1' == result1[1] == result2[1] == result3[1] or 'S1' == result2[1] == result3[1] == result4[1]:
        print("111 S1")
        S1_3 += 1

    elif 'S1' == result1[1] == result2[1] or 'S1' == result3[1] == result4[1]:
        print("11 S1")
        S1_2 += 1  

    # S1 Beggining in 2
    if 'S1' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 S1")
        S1_4 += 1

    elif 'S1' == result1[2] == result2[2] == result3[2] or 'S1' == result2[2] == result3[2] == result4[2]:
        print("222 S1")
        S1_3 += 1

    elif 'S1' == result1[2] == result2[2] or 'S1' == result3[2] == result4[2]:
        print("22 S1")
        S1_2 += 1  

    # S1 Beggining in 3
    if 'S1' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 S1")
        S1_4 += 1

    elif 'S1' == result1[3] == result2[3] == result3[3] or 'S1' == result2[3] == result3[3] == result4[3]:
        print("333 S1")
        S1_3 += 1

    elif 'S1' == result1[3] == result2[3] or 'S1' == result3[3] == result4[3]:
        print("33 S1")
        S1_2 += 1  

    # S2 Beggining in 0
    if 'S2' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 S2")
        S2_4 += 1

    elif 'S2' == result1[0] == result2[0] == result3[0] or 'S2' == result2[0] == result3[0] == result4[0]:
        print("000 S2")
        S2_3 += 1

    elif 'S2' == result1[0] == result2[0] or 'S2' == result3[0] == result4[0]:
        print("00 S2")
        S2_2 += 1  

    # S2 Beggining in 1
    if 'S2' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 S2")
        S2_4 += 1

    elif 'S2' == result1[1] == result2[1] == result3[1] or 'S2' == result2[1] == result3[1] == result4[1]:
        print("111 S2")
        S2_3 += 1

    elif 'S2' == result1[1] == result2[1] or 'S2' == result3[1] == result4[1]:
        print("11 S2")
        S2_2 += 1

    # S2 Beggining in 2
    if 'S2' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 S2")
        S2_4 += 1

    elif 'S2' == result1[2] == result2[2] == result3[2] or 'S2' == result2[2] == result3[2] == result4[2]:
        print("222 S2")
        S2_3 += 1

    elif 'S2' == result1[2] == result2[2] or 'S2' == result3[2] == result4[2]:
        print("22 S2")
        S2_2 += 1

    # S2 Beggining in 3
    if 'S2' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 S2")
        S2_4 += 1

    elif 'S2' == result1[3] == result2[3] == result3[3] or 'S2' == result2[3] == result3[3] == result4[3]:
        print("333 S2")
        S2_3 += 1

    elif 'S2' == result1[3] == result2[3] or 'S2' == result3[3] == result4[3]:
        print("33 S2")
        S2_2 += 1

    # S3 Beggining in 0
    if 'S3' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 S3")
        S3_4 += 1

    elif 'S3' == result1[0] == result2[0] == result3[0] or 'S3' == result2[0] == result3[0] == result4[0]:
        print("000 S3")
        S3_3 += 1

    elif 'S3' == result1[0] == result2[0] or 'S3' == result3[0] == result4[0]:
        print("00 S3")
        S3_2 += 1

    # S3 Beggining in 1
    if 'S3' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 S3")
        S3_4 += 1

    elif 'S3' == result1[1] == result2[1] == result3[1] or 'S3' == result2[1] == result3[1] == result4[1]:
        print("111 S3")
        S3_3 += 1

    elif 'S3' == result1[1] == result2[1] or 'S3' == result3[1] == result4[1]:
        print("11 S3")
        S3_2 += 1

    # S3 Beggining in 2
    if 'S3' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 S3")
        S3_4 += 1

    elif 'S3' == result1[2] == result2[2] == result3[2] or 'S3' == result2[2] == result3[2] == result4[2]:
        print("222 S3")
        S3_3 += 1

    elif 'S3' == result1[2] == result2[2] or 'S3' == result3[2] == result4[2]:
        print("22 S3")
        S3_2 += 1

    # S3 Beggining in 3
    if 'S3' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 S3")
        S3_4 += 1

    elif 'S3' == result1[3] == result2[3] == result3[3] or 'S3' == result2[3] == result3[3] == result4[3]:
        print("333 S3")
        S3_3 += 1

    elif 'S3' == result1[3] == result2[3] or 'S3' == result3[3] == result4[3]:
        print("33 S3")
        S3_2 += 1

    # S4 Beggining in 0
    if 'S4' == result1[0] == result2[0] == result3[0] == result4[0]:
        print("0000 S4")
        S4_4 += 1

    elif 'S4' == result1[0] == result2[0] == result3[0] or 'S4' == result2[0] == result3[0] == result4[0]:
        print("000 S4")
        S4_3 += 1

    elif 'S4' == result1[0] == result2[0] or 'S4' == result3[0] == result4[0]:
        print("00 S4")
        S4_2 += 1

    # S4 Beggining in 1
    if 'S4' == result1[1] == result2[1] == result3[1] == result4[1]:
        print("1111 S4")
        S4_4 += 1

    elif 'S4' == result1[1] == result2[1] == result3[1] or 'S4' == result2[1] == result3[1] == result4[1]:
        print("111 S4")
        S4_3 += 1

    elif 'S4' == result1[1] == result2[1] or 'S4' == result3[1] == result4[1]:
        print("11 S4")
        S4_2 += 1

    # S4 Beggining in 2
    if 'S4' == result1[2] == result2[2] == result3[2] == result4[2]:
        print("2222 S4")
        S4_4 += 1

    elif 'S4' == result1[2] == result2[2] == result3[2] or 'S4' == result2[2] == result3[2] == result4[2]:
        print("222 S4")
        S4_3 += 1

    elif 'S4' == result1[2] == result2[2] or 'S4' == result3[2] == result4[2]:
        print("22 S4")
        S4_2 += 1

    # S4 Beggining in 3
    if 'S4' == result1[3] == result2[3] == result3[3] == result4[3]:
        print("3333 S4")
        S4_4 += 1

    elif 'S4' == result1[3] == result2[3] == result3[3] or 'S4' == result2[3] == result3[3] == result4[3]:
        print("333 S4")
        S4_3 += 1

    elif 'S4' == result1[3] == result2[3] or 'S4' == result3[3] == result4[3]:
        print("33 S4")
        S4_2 += 1

    payment_main = (W1_4pay*W1_4 + W1_3pay*W1_3 + 
                    W2_4pay*W2_4 + W2_3pay*W2_3 + 
                    W3_4pay*W3_4 + W3_3pay*W3_3 + 
                    W4_4pay*W4_4 + W4_3pay*W4_3 + 
                    S1_4pay*S1_4 + S1_3pay*S1_3 + S1_2pay*S1_2 +
                    S2_4pay*S2_4 + S2_3pay*S2_3 + S2_2pay*S2_2 +
                    S3_4pay*S3_4 + S3_3pay*S3_3 + S3_2pay*S3_2 +
                    S4_4pay*S4_4 + S4_3pay*S4_3 + S4_2pay*S4_2)
    # payment_main = Decimal(payment_main).quantize(Decimal('0.1'))
    #print("payment_main=", payment_main)

    # Display the winning region
    results = display_results([result1, result2, result3, result4])

    payment = payment_main #+ payment_vfeature + payment_freespin
    payment = Decimal(payment).quantize(Decimal('0.01'))
    print("payment=", payment)

    #print(results)
    #print(results_vfeature)

    #result6 = ["F", "F2", "F3", "F4", "D1"]
    #result6[2]="V"
    #print(result7)
    #print(result6[2])

    ####### API request do jogo #######
    #informacoes = {"payment main game": payment_main , "freespin mode": freespin , "Number of dinos": numofd, "Number of Eggs": countegg}
    #requisicao = requests.post('https://testeapi-14f17-default-rtdb.firebaseio.com/.json', json=informacoes)
    #print(requisicao)
    #print(requisicao.json())

    return render_template('index_infinity_v1.html', 
                           results=results, 
                           result1=result1, 
                           result2=result2, 
                           result3=result3, 
                           result4=result4, 
                           W1_3=W1_3, W1_4=W1_4,
                           W2_3=W2_3, W2_4=W2_4,
                           W3_3=W3_3, W3_4=W3_4,
                           W4_3=W4_3, W4_4=W4_4,
                           S1_2=S1_2, S1_3=S1_3, S1_4=S1_4,
                           S2_2=S2_2, S2_3=S2_3, S2_4=S2_4,
                           S3_2=S3_2, S3_3=S3_3, S3_4=S3_4,
                           S4_2=S4_2, S4_3=S4_3, S4_4=S4_4,
                           W1_3pay=W1_3pay, W1_4pay=W1_4pay,
                           W2_3pay=W2_3pay, W2_4pay=W2_4pay,
                           W3_3pay=W3_3pay, W3_4pay=W3_4pay,
                           W4_3pay=W4_3pay, W4_4pay=W4_4pay,
                           S1_2pay = S1_2pay, S1_3pay=S1_3pay, S1_4pay=S1_4pay,
                           S2_2pay = S2_2pay, S2_3pay=S2_3pay, S2_4pay=S2_4pay,
                           S3_2pay = S3_2pay, S3_3pay=S3_3pay, S3_4pay=S3_4pay,
                           S4_2pay = S4_2pay, S4_3pay=S4_3pay, S4_4pay=S4_4pay,
                           payment=payment)


if __name__ == '__main__':
    app.run(debug=True, port=8000)


