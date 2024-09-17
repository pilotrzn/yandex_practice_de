counter = 0

while True:
    counter += 1
    if counter % 3 == 0 and counter % 5 == 0 and counter % 7 == 0:
        print(counter)
        break