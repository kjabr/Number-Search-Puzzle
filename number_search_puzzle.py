#!/usr/bin/python
import random
import sys
import time

def overlap(start1, end1, start2, end2):
    # using this routine to check if two lines overlap. Essential if they
    # intersect and are on the same row (horizontal) or column (vertical)
    # then they overlap
    return (end1 >= start2) and (end2 >= start1)

def coord():
    # auto generate random coordinates, length and function
    # function means horizontal, vertical or diagonal number search
    x = random.randint(0,16)   # row
    y = random.randint(0,16)   # column
    f = random.randint(1,3)    # function
    l = random.randint(5,9)    # length

    if f == 1: # horizontal mode
        if (y+l >= 17):
            d = 2
        elif (y-l < 0):
            d = 1
        else:
            d = random.randint(1,2)
    elif f == 2: # vertical mode
        if (x+l >= 17):
            d = 2
        elif (x-l < 0):
            d = 1
        else:
            d = random.randint(1,2)
    elif f == 3: # diagonal mode
        if (x+l >= 17) and (y-l < 0):  # need to search up-right
            d = 1
        elif (x+l >= 17) and (y+l >= 17):    # need to search up-left
            d = 2
        elif (x-l < 0) and (y-l < 0):  # need to search down-right
            d = 3
        elif (x-l < 0) and (y+l >= 17):     # need to search down-left
            d = 4
        elif (x+l <= 16 and x-l >=0) and (y-l < 0):
            d = random.choice([1,3])
        elif (x+l <= 16 and x-l >=0) and (y+l >= 17):
            d = random.choice([2,4])
        elif (x-l < 0) and (y+l <= 16 and y-l >=0):
            d = random.choice([3,4])
        elif (x+l >= 17) and (y+l <= 16 and y-l >=0):
            d = random.choice([1,2])
        else:
            d = random.randint(1,4)
    else:
        pass
    return x,y,f,l,d

def find_numb(m,x,y,f,l,d):
    # this routine finds the number search in the matrix and returns that number
    # based on d we know either horizontal, vertical, or diagonal

    # print ("%s %s %s %s %s" % (x,y,f,l,d))

    n=[]
    for i in range (l):
        if f == 1 and d == 1: # horizontal mode
            n.append(m[x][y+i])   # right

        if f == 1 and d == 2:
            n.append(m[x][y-i])   # left

        if f == 2 and d == 1: # vertical mode
            n.append(m[x+i][y])   # down

        if f == 2 and d == 2:
            n.append(m[x-i][y])   # up

        if f == 3 and d == 1: # diagonal mode
            n.append(m[x-i][y+i])  # up-right
        elif f == 3 and d == 2:
            n.append(m[x-i][y-i])  # up-left
        elif f == 3 and d == 3:
            n.append(m[x+i][y+i])  # down-right
        elif f == 3 and d == 4:
            n.append(m[x+i][y-i])  # dowb-left
        else:
            pass
    return n

# html_file is the output html file
html_file = "number_search_puzzle.html"

matrix, result, dup_list, items, numb =([] for i in range (5))
hd1,hd2,vd1,vd2,dd1,dd2,dd3,dd4=([] for i in range(8))
matrix_puzz=""
numbers_puzz=""
position_from_top = 80 # for display in the html file.
regen_coord = 1

number_of_puzzles = 1

if len(sys.argv) > 1:
    number_of_puzzles = sys.argv[1]

# the html_content string
html_content = """<HTML>
<!doctype html public "-//w3c//dtd html 3.2//en">

<head>
<style>

.container {
    width: 800px;
    position: relative;
}

.left-element {
    display: inline-block;
    position: relative;
    outline: #2eb7ed solid medium;
    padding: 10px;
    font-family: arial;
    font-weight: bold;
    font-size: 25;
    letter-spacing: 4px;
    left: 20;
    top: 40;
    margin-left: 20px;
}

.left_under {
    display: inline-block;
    position: absolute;
    font-family: arial;
    font-weight: bold;
    padding-top: 570px;
    vertical-align: middle;
    font-size: 15;
    left: 230;

}

.right-element {
    display: inline-block;
    position: absolute;
    font-family: arial;
    font-weight: bold;
    font-size: 25;
    letter-spacing: 4px;
    right: 0;
}


.pagebreak { page-break-after: always;
    position: relative; }
</style>
</head>

<body bgcolor="ffffff" text="000000" link="0000ff" vlink="800080" alink="ff0000"> """

for repeat in range (int(number_of_puzzles)):

    # Need to produce the number matrix. Below implemented as 17x17
    for y in range (17):
        row=[]
        for x in range (17):
            row.append(random.randint(0,9))
        matrix.append(row)

    # Next part takes each line from them matrix, saves to a variable and then adds to the html
    # file using the variable html_content. This probably can be combined with the loop that produced
    # the matrix list. But decided to keep it separate to keep it easier to understand

    html_content += """<div class="container">
        <div class="left-element">

    """

    for n in range (17):
        matrix_puzz = " ".join([str(x) for x in matrix[n]])
        #html_content += """<div1>"""
        html_content += matrix_puzz
        html_content += """<br>"""

    html_content += """</div>"""

    html_content += """<div class="left_under">"""
    html_content += """Puzzle Number: """
    html_content += str(repeat+1)
    html_content += """</div>"""

        #position_from_top += 29

    # Next part creates multiple random coordinates to look for the numbers in the puzzle

    html_content += """<div class="right-element">
    """

    # pos_from_top_numbers = 80  # need to reinit the position from top for the numbers
                            # displayed on the right side of the puzzle

    # The next part is generating 21 numbers. ie numbers to search.
    for p in range (21):
        row, column, func, length, direction = coord()
        while (regen_coord):

    # Need to look for overlapping numbers in the puzzle. Lists hd1, hd2,
    # vd1, vd2, and dd1-4 act as history buffer to compare against

            if (func == 1 and direction == 1):  #right
                if hd1 and not dup_list:
                    dup_list = [items for items in hd1 if
                        ((overlap (items[1], (items[1]+items[2]), column,
                        (column+length)) and (items[0] == row)))]

                if hd2 and not dup_list:
                    dup_list = [items for items in hd2 if
                        ((overlap ((items[1]-items[2]), items[1], column,
                            (column+length)) and (items[0] == row)))]

            elif (func == 1 and direction == 2):  # left
                if hd2 and not dup_list:
                    dup_list = [items for items in hd2 if
                        ((overlap ((items[1]-items[2]), items[1], (column-length),
                            column) and (items[0] == row)))]
                if hd1 and not dup_list:
                    dup_list = [items for items in hd1 if
                        ((overlap (items[1], (items[1]+items[2]), (column-length),
                        column) and (items[0] == row)))]

            elif (func == 2 and direction == 1):   # down
                if vd1 and not dup_list:
                    dup_list = [items for items in vd1 if
                        ((overlap (items[0], (items[0]+items[2]), row, (row+length))
                            and (items[1] == column)))]
                if vd2 and not dup_list:
                    dup_list = [items for items in vd2 if
                        ((overlap ((items[0]-items[2]), items[0], row,
                            (row+length)) and (items[1] == column)))]

            elif (func == 2 and direction == 2):  # up
                if vd2 and not dup_list:
                    dup_list = [items for items in vd2 if
                        ((overlap ((items[0]-items[2]), items[0], (row-length), row)
                            and (items[1] == column)))]
                if vd1 and not dup_list:
                    dup_list = [items for items in vd1 if
                        ((overlap (items[0], (items[0]+items[2]), (row-length),
                            row) and (items[1] == column)))]

            elif (func == 3 and (direction == 1 or direction == 4)):  # up-right or
                dup_list = [items for items in dd1 if                 # down-left
                    (((items[0]+items[1]) == (row+column)) and dd1)]
                if not dup_list:
                    dup_list = [items for items in dd4 if
                        (((items[0]+items[1]) == (row+column)) and dd4)]

            elif (func == 3 and (direction == 2 or direction == 3)):  # up-left or
                dup_list = [items for items in dd2 if                 # down-right
                    (((items[0]-items[1]) == (row-column)) and dd2)]
                if not dup_list:
                    dup_list = [items for items in dd3 if
                        (((items[0]-items[1]) == (row-column)) and dd3)]

            if not dup_list:
                result = [row, column, length]

                if (func == 1 and direction == 1):
                    hd1.append(result)
                elif (func == 1 and direction == 2):
                    hd2.append(result)
                elif (func == 2 and direction == 1):
                    vd1.append(result)
                elif (func == 2 and direction == 2):
                    vd2.append(result)
                elif (func == 3 and direction == 1):
                    dd1.append(result)
                elif (func == 3 and direction == 2):
                    dd2.append(result)
                elif (func == 3 and direction == 3):
                    dd3.append(result)
                elif (func == 3 and direction == 4):
                    dd4.append(result)

                regen_coord = 0

            elif dup_list:
                # print dup_list
                row, column, func, length, direction = coord()
                #print "dedup"
                del dup_list[:]

        regen_coord = 1

    # Now that we have the random coordinates we pass that to the routine to generate
    # the actual number

        numb=find_numb(matrix,row,column,func,length,direction)

    # option to print the coordinates of each number in the matrix...

        #print ("row=%s, column=%s, func=%s, length=%s, direction=%s" % (row+1, column+1,
        #    func, length, direction))

        numbers_puzz = "".join([str(x) for x in numb])

    # we get the number back from the routine then append to the html file we will write
    # at the end

        #html_content += """<DIV style="display:inline-block Right; font-family: arial; font-style: italic;
        #    font-variant:small-caps; font-weight:bold;letter-spacing: 4px; font-size:25;
        #    width: 250px; left: 650px; height: 25px">"""
        html_content += """<span>"""
        html_content += numbers_puzz
        html_content += """</span>"""
        html_content += """<br>"""
    html_content += """</div>"""
        #position_from_top += 29

    if number_of_puzzles > 1:
        html_content += """

        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <br>
        <div class="pagebreak"> </div>

        """

        y = 0
        matrix = []
        #time.sleep(0.5)
        hd1,hd2,vd1,vd2,dd1,dd2,dd3,dd4=([] for i in range(8))


# Now complete the trailing part of the html file
html_content += """
</body>
</html>
"""

# write to the html and properly close it
out_file = open(html_file, "w")
out_file.write(html_content)
out_file.close()
