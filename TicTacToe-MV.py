from random import randint

def gen_field(N):       # generovanie hracieho pola (3 x 3 uvazujem ako najmensi mozny format,  
                        # kedze beriem 3 znaky za sebou ako podmienku na ziskanie bodu)
    field = [['-','-','-'],['-','-','-'],['-','-','-']]
    for i in range(3,N):
        field.append(['-','-','-'])
        for j in range(3,i):
            field[i].extend('-')
        for j in range(0,i+1):
            field[j].extend('-')
    return field
    

def print_field(field):             ## vypis pola
    print
    print ' ',
    for i in range(0,len(field)):   #vypis X suradnic
        if i < 9:
            print '',i, '',
        else:
            print '',i,
    print '  X'
    for i in range(0,len(field)):
        print i,     #vypisovanie Y suradnice
        if i < 10:
            print '',
        for j in range(0,len(field)):   
            print field[j][i],      #vypis jednotlivych riadkov
            if j != len(field)-1:
                print '|',
        print
        print ' ',
        for j in range(0,len(field)):   #vypis oddelovaca riadkov
            print '~~~',            
        print
    print 'Y'

def gen_priority_field(N):                      #generovanie pomocneho int pola pre CP bota
    priority_field = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3,N):
        priority_field.append([0,0,0])
        for j in range(3,i):
            priority_field[i].extend('-')
        for j in range(0,i+1):
            priority_field[j].extend('-')
    return priority_field

# zvazoval som 2 moznosti pre PC bota a to:
# 1. na zaciatku tvorit pole zlozene nie z char premennych ale z objektov a kazdu poziciu v poli mat s atributom state(-/X/O),
#    a priority, nakoniec sa mi ale 2. moznost zdala menej narocna pre PC aj ked som si neni prilis isty.
# 2. vygenerovat nove pole ale s int. jednotkami a ratat prioritu jednotlivych pozicii v tomto paralelnom poli.
def check_left(field,i,j):
    if field[i-1][j] == field[i-2][j] != '-':
        return True
    return False                                        ###funkcie, ktore kontroloju jednotlive casti okolia zvoleneho
def check_left_up(field,i,j):                           ###bodu v poli pre moznost ziskat alebo zablokovat zisk bodu
    if field[i-1][j-1] == field[i-2][j-2] != '-':
        return True
    return False
def check_up(field,i,j):
    if field[i][j-1] == field[i][j-2] != '-':
        return True
    return False
def check_up_right(field,i,j):
    if field[i+1][j-1] == field[i+2][j-2] != '-':
        return True
    return False
def check_right(field,i,j):
    if field[i+1][j] == field[i+2][j] != '-':
        return True
    return False
def check_right_down(field,i,j):
    if field[i+1][j+1] == field[i+2][j+2] != '-':
        return True
    return False
def check_down(field,i,j):
    if field[i][j+1] == field[i][j+2] != '-':
        return True
    return False
def check_down_left(field,i,j):
    if field[i-1][j+1] == field[i-2][j+2] != '-':
        return True
    return False
def check_middle_horizontal(field,i,j):
    if field[i-1][j] == field[i+1][j] != '-':
        return True
    return False
def check_middle_vertical(field,i,j):
    if field[i][j-1] == field[i][j+1] != '-':
        return True
    return False
def check_middle_X1(field,i,j):
    if field[i-1][j+1] == field[i+1][j-1] != '-':
        return True
    return False
def check_middle_X2(field,i,j):
    if field[i-1][j-1] == field[i+1][j+1] != '-':
        return True
    return False
    

def PC_strategy(field,priority_field):                  # samotna strategia pre PC, v ktorej ratam prioritu do priority_field pre kazdy zatial nezaradeny
    for i in range(0,len(field)):                       # bod v poli field. velkosti zmeny hodnot som viac menej urcil na zaklade pokusov z hrania.   
        for j in range(0,len(field)):
            priority_field[i][j] = 0
            if i == 0 or j == 0 or i == len(field)-1 or j == len(field)-1:      ## -3 body ak je dana pozicia na kraji pola
                priority_field[i][j] -= 3
            elif i > 0 and j > 0 and i < len(field)-1 and j < len(field)-1 and field[i][j] == '-':
                priority_field[i][j] -= 2                                       ## -2 body ak je dana pozicia mimo okraju
            if field[i][j] == '-':  
                if i > 0 and i < len(field)-1 and check_middle_horizontal(field,i,j) == True:   ## +5 bodov ak na danom poli viem ziskat bod 
                    priority_field[i][j] += 5                                                   ## alebo zabranit superovi aby ho ziskal on
                if j > 0 and j < len(field)-1 and check_middle_vertical(field,i,j) == True:
                    priority_field[i][j] += 5
                if j > 0 and j < len(field)-1 and i > 0 and i < len(field)-1:
                    if check_middle_X1(field,i,j) == True:
                        priority_field[i][j] += 5
                    if check_middle_X2(field,i,j) == True:
                        priority_field[i][j] += 5
                if j > 1 and check_up(field,i,j) == True:
                    priority_field[i][j] += 5
                if j < len(field)-2 and check_down(field,i,j) == True:
                    priority_field[i][j] += 5
                if i > 1 and check_left(field,i,j) == True:
                    priority_field[i][j] += 5
                if i < len(field)-2 and check_right(field,i,j) == True:
                    priority_field[i][j] += 5
                if i < len(field)-2 and j > 1 and check_up_right(field,i,j) == True:
                    priority_field[i][j] += 5
                if i < len(field)-2 and j < len(field)-2 and check_right_down(field,i,j) == True:
                    priority_field[i][j] += 5
                if i > 1 and j < len(field)-2 and check_down_left(field,i,j) == True:
                    priority_field[i][j] += 5
                if i > 1 and j > 1 and check_left_up(field,i,j) == True:
                    priority_field[i][j] += 5
                count_three = 0 
                if i > 0 and j > 0 and field[i-1][j-1] != '-' and count_three < 4:          ## +1 bod za kazdy znak v okoli.(do 3 znakov)
                    priority_field[i][j] += 1
                if j > 0 and field[i][j-1] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if i < len(field)-1 and j > 0 and field[i+1][j-1] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if i < len(field)-1 and field[i+1][j] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if i < len(field)-1 and j < len(field)-1 and field[i+1][j+1] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if j < len(field)-1 and field[i][j+1] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if i > 0 and j < len(field)-1 and field[i-1][j+1] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                if i > 0 and field[i-1][j] != '-' and count_three < 4:
                    priority_field[i][j] += 1
                    
    value = -10                         # vyber volnej pozicie s najvecsou prioritou. 
    for i in range(0,len(field)):                 
        for j in range(0,len(field)):
            if field[i][j] == '-' and priority_field[i][j] > value:
                value = priority_field[i][j]
                pozitions = [[i,j]]
            if field[i][j] == '-' and priority_field[i][j] == value:    # pri viacerich bodoch s najvyssou prioritou vyberam nahodne jeden z nich.
                pozitions.append([i,j])
    #print print_field(priority_field) #    (VYPIS PRIORITNEHO POLA PRED CPU TAHOM NA LADENIE BOTA)
    random_poz = randint(0,len(pozitions)-1)
    return pozitions[random_poz]
            
                
                        
    
    
def check_points(field):        # zaverecne zratanie bodov
    points_X = 0
    points_O = 0

    for i in range(0,len(field)):   ## body v stlpcoch
        previous = ''
        count = 0
        for j in range(0,len(field)):
            if previous == field[i][j]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else:     
                count = 1
                previous = field[i][j]

    for i in range(0,len(field)):   ## body v riadkoch
        previous = ''
        count = 0
        for j in range(0,len(field)):
            if previous == field[j][i]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else:  
                count = 1
                previous = field[j][i]
           
    for i in range(2,len(field)):   # body sikmo
        previous = ''               ## prva polovica pola
        count = 0
        for j in range(0,i+1):
            if previous == field[j][i-j]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else: 
                count = 1
                previous = field[j][i-j]

    for i in range(1,len(field)-2): ## druha polovica pola
        previous = ''
        count = 0
        for j in range(i,len(field)):
            if previous == field[j][len(field)-1-j+i]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else:  
                count = 1
                previous = field[j][len(field)-1-j+i]

    for i in range(len(field)-3,-1,-1):     # body sikmo (opacny smer)
        previous = ''                       ## prva polovica pola
        count = 0
        for j in range(0,len(field)-i):
            if previous == field[i+j][j]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else:  
                count = 1
                previous = field[i+j][j]
    
    for i in range(1,len(field)-2):         ## druha polovica pola
        previous = ''
        count = 0
        for j in range(i,len(field)):
            if previous == field[j-i][j]:
                count += 1
                if count > 2:
                    if previous == 'X':
                        points_X += 1
                    elif previous == 'O':
                        points_O += 1
            else: 
                count = 1
                previous = field[j-i][j]
    return [points_X, points_O]
    



def TicTacToe(N):
    print("PC uses character X")        
    print("Player uses character O")
    print 
    print "(1) - Player begins"
    print "(2) - Computer begins"
    move = input()  
    while move != 1 and move != 2:      
        print "oops there was a mistake, try again: "
        move = input()
    field = gen_field(N)        ## generovanie hracieho planu a pomocneho planu pre bota
    priority_field = gen_priority_field(N)
    print_field(field)
    turn = 0            ## rozpoznavanie, kto je na rade
    while turn != N*N:  
        turn += 1
        if move == 1:
            valid_move = False
            move += 1
            print '~~~~~~~~~~~~~~Your move~~~~~~~~~~~~~~'## nacitanie a kontrola hrcovho tahu
            while valid_move == False:
                x = raw_input('enter x:')
                y = raw_input('enter y:')
                if x != '' and y != '':  # kontrola zadanej hodnoty, aby sa program neukoncoval po slabom zmagnuti klavesy
                    x = int(float(x))
                    y = int(float(y))
                    if -1 < x < len(field) and -1 < y < len(field): # kontrola zadanej hodnoty, aby sa program neukoncoval pri zadani cisla mimo pola
                        if field[x][y] == '-':
                            field[x][y] = 'O'
                            valid_move = True
                        else:
                            print('Wrong move.')
                    else:
                        print('Wrong move.')
                else:
                    print('Wrong move.')
            print_field(field)
        elif move == 2:     ## PC tah
            move -= 1
            PC_move = PC_strategy(field,priority_field)
            
            print '~~~~~~~~~~~~~~Comp. move~~~~~~~~~~~~~~'
            print 'x - ', PC_move[0]
            print 'y - ', PC_move[1]
            if field[PC_move[0]][PC_move[1]] == '-':
                field[PC_move[0]][PC_move[1]] = 'X'
            else:                                       #LADENIE
                print '!!!!!!!!!!!!!!!CMP BOT JE CHYBNY ..... PLS OPRAVIT!!!!!!!!!!!!!!'
            print_field(field)
    points = check_points(field)    ## vypis vysledkov hry
    print('Points PC: '), points[0]                   
    print('Points player: '), points[1]
    print
    if points[0] > points[1]:
        print('##### PC won #####')
    elif points[0] == points[1]:
        print('##### Draw #####')
    else:
        print('##### User won #####')
    



repeat = True               ## Samotny program + volba jeho opakovania
print 'Welcome to NxN TicTacToe. In this version you play against PC and your goal is'
print 'to earn more points than him before the whole field is filled. The score is'
print 'assigned as follows: 3 in a row = 1 point, 4 in a row = 2 poits,'
print '5 in a row = 3 points and so forth. Enjoy ;)'
print
while repeat == True:
    field_size = input('Size of the field (3-40): ')    # 3 - 40 pretoze viac ako 40 sa uz na obrazovku moc nechce
    if 2 < field_size < 41:                             # zmestit a 3 je minimalna podmienka na ziskanie bodu
        TicTacToe(field_size)                               
        repeat = raw_input('next game? (y/n): ')
        if repeat == 'y' or repeat == 'Y':
            repeat = True
        else:
            repeat = False
    else:
        print('Wrong size.')
