# This are the various packages that are used throughout the program
import csv
import random
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
import sys


# This is the beginning of function called populate_csv. Its run to update the contents of the data stored in the csv
# files
def populate_csv():
    # We create an empty list
    main_lit = []
    # Open the users.csv file in read mode
    with open('users.csv', 'r') as read_obj:
        # Create a csv reader object and pass the open file to it
        csv_reader = csv.reader(read_obj)
        # Iterate through the rows of the csv file
        for ite in csv_reader:
            # We create an empty list

            memory_use_list = []
            # Iterate 3600 times to create contents of the resource usage
            for time in range(3600):
                # Create a random integer between 0 and 5000 and add that value to the memory_use_list
                memory_use_list.append(random.randint(0, 5000))
            # Print the contents of memory_use_list to console window
            print(memory_use_list)
            # Add momory_use_list to list main_lit
            main_lit.append(memory_use_list)
    # Print contents of main_lit
    print(main_lit)
    # Create a writer object in write mode
    writer = csv.writer(open('users_memory.csv', 'w', newline=''))
    # Add the contents of main_lit to the open file
    writer.writerows(main_lit)


# The main function to draw the graph adn do everything else. Takes 2 arguments: num and username
def draw_graph(num, username):

    user_id = 0
    y_values = []
    # Open the user.csv file and get the user that matches the username value
    with open('users.csv', 'r') as user_data_obj:
        user_data_reader = csv.reader(user_data_obj)
        for id, row in enumerate(user_data_reader):
            try:
                if row[0] == username:
                    user_id = id
            except Exception:
                return 'Could not find user'

    with open('users.csv', 'r') as user_read_obj:
        user_reader = csv.reader(user_read_obj)
        for t, user in enumerate(user_reader):
            if t == num:
                user_data = user
    # Open the user_memory.csv and find the data the matches the id of the user
    with open('users_memory.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        for num, item in enumerate(csv_reader):
            if num == user_id:
                y_values = item
    # Loop through y values and convert them to integers
    for i in range(0, len(y_values)):
        y_values[i] = int(y_values[i])
    print(y_values)
    # Assign the value of num to variable lini
    lini = num
    total_memory_usage = 0
    total_time = 0
    # Loop through y_values upto the value of num passed as an argument and get and get the sum
    for value in y_values[:lini]:
        total_memory_usage += value
    # Get the sum of of total time
    for time in range(lini):
        total_time += 1
    # Create a numpy array object for y axsi
    y = np.array(y_values[:lini])
    # Create a numpy array object for x axsi

    x = np.arange(0, lini)
    print(x)
    print(y)
    # Ploting the graph
    plt.title("Line graph")
    plt.xlabel("Seconds")
    plt.ylabel("Memory Usage")
    plt.plot(x, y, color="green")
    plt.show()
    plt.savefig('saved_figure.png')

    output_data = (['Username', user_data[0]], ['Total PIDs ', user_data[1]], ['Total CPU Time', total_time],
                   ['Total Real Memory Usage', total_memory_usage])

    row = 0
    col = 0
    # Writtign user data to userdata.xlsx
    workbook = xlsxwriter.Workbook('UserData.xlsx')
    worksheet = workbook.add_worksheet()

    for item, cost in (output_data):
        worksheet.write(row, col, item)
        worksheet.write(row, col + 1, cost)
        row += 1

    # Write a total using a formula.
    worksheet.write(row, 0, 'Total')
    worksheet.write(row, 1, '=SUM(B1:B4)')

    workbook.close()
# Beegginig of the program

try:
    username = sys.argv[1]
    if username == 'populate':
        populate_csv()
    else:
        try:
            time = int(sys.argv[2])
            draw_graph(time, username)
        except:
            print('You did not provide the time argument')
except:
    print('You did not provide any arguments')
