import sys; args = sys.argv[1:]
import math, time, re
# sort dictionary words --> 53%
startTime = time.process_time()
height = 0
WIDTH = 0
board = ""
TOTALBLOCKS = 0
OGBLOCKS = 0
BLOCKCHAR = "#"
OPENCHAR = "-"
DICTIONARY = {} #len wrd: word
LETTERDCT = {}
POSTOLEN = ""
SEENWRDS = {}
alpha = "ABCDEFGHIJKLMNOP"
NOTPOSS = set()
#0  #1  #2  #3  #4  #5  #6  #7  #8
#9  #10 #11 #12 #13 #14 #15 #16 #17
#18 #19 #20 #21 #22 #23 #24 #25 #26
#27 #28 #29 #30 #31 #32 #33 #34 #35
#36 #37 #38 #39 #40 #41 #42 #43 #44
#45 #46 #47 #48 #49 #50 #51 #52 #53
#54 #55 #56 #57 #58 #59 #60 #61 #62
#63 #64 #65 #66 #67 #68 #69 #70 #71
#72 #73 #74 #75 #76 #77 #78 #79 #80

def positionToSet(n):
    return
 
def constraint1(pz, n): # n is len of one side, gen diagonals, rows, and cols
    return 
 

#-----------------------------------------------------------------------------------#
 
def bruteForce(board, bsq):
    ct = board.count(BLOCKCHAR)
    if isInvalid(board, ct):
        return ""
    if isSolved(board, ct): #see if it is solved
        #display2D(board)
        return board
    listofChoices = collectivelyExhausted(board) #where you can put the next blocking square
    for nextboard in listofChoices:
        bF = bruteForce(nextboard, bsq -2) #lookup table - letter, block
        if bF:
            return bF
    return ""
   
def calculatelen2(brd): #cut time in half by mirroring lengths
   posandlen = {}
   for i, pc in enumerate(brd):
      if i < WIDTH+3:
         continue
      if i> len(brd)-WIDTH-3:
         continue
      if pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR and brd[i-1] == BLOCKCHAR:
         posandlen[i] = [hlen(brd, i, 2), vlen(brd, i, 2)]
      elif  pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR:
         posandlen[i] = [0, vlen(brd, i, 2)]
      elif pc != BLOCKCHAR and brd[i-1] == BLOCKCHAR:
         posandlen[i] = [hlen(brd, i, 2), 0]
   return posandlen
 
def hlen(brd, i, num):
   for ind in range(i+3, (i//(WIDTH+2)+1)*(WIDTH+2), ):
      if brd[ind] == BLOCKCHAR: #horz len; first occurent of #
         if num == 1: return ind-i if OPENCHAR in brd[i: ind:] else 0
         if num == 2: return ind-i
   return 0
 
def vlen(brd, i, num):
   for ind in range(i+3*(WIDTH+2), len(brd), WIDTH+2):
      if brd[ind] == "#": #VERT len; first occurent of #
         if num == 1: return (ind-i)//(WIDTH+2) if OPENCHAR in brd[i: ind: WIDTH+2] else 0
         if num == 2: return (ind-i)//(WIDTH+2)
   return 0
    

def calculatelen(brd): #cut time in half by mirroring lengths
   posandlen = {}
   for i, pc in enumerate(brd):
      hLen = hlen(brd, i, 1)
      vLen = vlen(brd, i, 1)
      if i < WIDTH+3:
         continue
      if i> len(brd)-WIDTH-3:
         continue
      if pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR and brd[i-1] == BLOCKCHAR:
         if hLen or vLen: posandlen[i] = [hLen, vLen]
      elif  pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR:
         if vLen: posandlen[i] = [0, vLen]
      elif pc != BLOCKCHAR and brd[i-1] == BLOCKCHAR:
         if hLen: posandlen[i] = [hLen, 0]
   return posandlen
   
def validword(board, ind, word, ori, check):
   global NOTPOSS
   if ori == "h":
      for i, letter in enumerate(check):
         if letter == BLOCKCHAR:
            return False
         if letter not in "*"+OPENCHAR and letter != word[i]:
            return False
      board = putword(board, ind, word, ori) #input the word if OK
      vertpos = -1 #position of vert word
      for i in range(ind, ind+len(word),): #start at ind, go to lastind
         for vind in range(i, 0, -(WIDTH+2)): 
            if board[vind] == BLOCKCHAR: 
               vertpos = vind+WIDTH+2
               break
         vword = board[vertpos: vertpos + (2+WIDTH)*POSTOLEN[vertpos][1]: 2+WIDTH]
         if OPENCHAR not in vword: #vertical len, does not make a full word
            if not vword in DICTIONARY[POSTOLEN[vertpos][1]]: #checks to see if the vertical
               #print(vword)
               return False
         else:
            LOS = []
            for ind, letter in enumerate(vword):
               if letter == OPENCHAR:
                  continue
               tupkey = (len(vword), letter, ind)
               if tupkey in NOTPOSS: return False
               if not tupkey in LETTERDCT:
                  return False
               LOS.append(LETTERDCT[tupkey])
            SOS = set.intersection(*LOS)
            if not SOS: 
               NOTPOSS.add(vword)
               return False
 
   if ori == "v":
      check = board[ind: ind+len(word)*(WIDTH+2):WIDTH+2]
      for i, letter in enumerate(check):
         if letter == BLOCKCHAR:
            return False
         if letter not in "*"+OPENCHAR and letter != word[i]:
            return False
      board = putword(board, ind, word, ori) #input the word if OK
      horzpos = -1 #position of vert word
      for i in range(ind, ind+len(word)*(WIDTH+2), WIDTH+2): #start at ind, go to lastind
         for hind in range(i, 0, -1): 
            if board[hind] == BLOCKCHAR: 
               horzpos = hind+1
               break
         hword = board[horzpos: horzpos + POSTOLEN[horzpos][0]]
         if OPENCHAR not in hword: #vertical len, does not make a full word
            if hword not in DICTIONARY[POSTOLEN[horzpos][0]]: #checks to see if the vertical
               return False
         else:
            LOS = []
            for ind, letter in enumerate(hword):
               if letter == OPENCHAR:
                  continue
               tupkey = (len(hword), letter, ind)
               if tupkey in NOTPOSS:
                  return False
               if not tupkey in LETTERDCT:
                  return False
               LOS.append(LETTERDCT[tupkey])
            SOS = set.intersection(*LOS)
            if not SOS: 
               NOTPOSS.add(hword)
               return False
   return True      




   
def solved(board):
   return not OPENCHAR in board   


def solve(board):
   global POSTOLEN
   board = border(board) #for easier processing
   POSTOLEN = calculatelen2(board)
   postolen = calculatelen(board) 
   toremove = {board:set()} #used words
   board = solvehelper(board, postolen, toremove)
   board = removeborder(board)
   return board
 
def invalidplace(board, toremove, postolen):
   toremove[board] = set()
   for pos in POSTOLEN:
      hLen = POSTOLEN[pos][0]
      vLen = POSTOLEN[pos][1]
      if not hLen and not vLen:
         continue
      if hLen:
            hstr = board[pos: pos + POSTOLEN[pos][0]].lower()
            if not "-" in hstr:
               if not hstr in DICTIONARY[POSTOLEN[pos][0]]: 
                  return True
               if hstr in DICTIONARY[POSTOLEN[pos][0]]:
                  toremove[board].add(hstr)
            if hLen and vLen: 
               postolen[pos][0] = hlen(board, pos, 1) 
               postolen[pos][1] = vlen(board, pos, 1)
            elif not vLen: 
               postolen[pos][0] = hlen(board, pos, 1) 
               postolen[pos][1] = 0
      if vLen:
            vstr = board[pos: pos + POSTOLEN[pos][1]*(WIDTH+2): WIDTH+2].lower()
            if not "-" in vstr and not vstr in DICTIONARY[POSTOLEN[pos][1]]:
               return True
            if vstr in DICTIONARY[POSTOLEN[pos][1]]:
               toremove[board].add(vstr)
            if hLen and vLen: 
               postolen[pos][0] = hlen(board, pos, 1) 
               postolen[pos][1] = vlen(board, pos, 1)
            elif not hLen: 
               postolen[pos][0] = 0 
               postolen[pos][1] = vlen(board, pos, 1)
   return False 
   
def solvehelper(board, postolen, toremove):
    if solved(board):
      return board
    #postolen = calculatelen(board)
#     print(postolen)
    dctChoices = possbrds(board, postolen, toremove)
    for brd in dctChoices: # brd: (tofill but certain ind is removed, toremoved + word)
      #display2Dw(brd, WIDTH+2)
      bF = solvehelper(brd, postolen, toremove)
      if bF:
          return bF
    return ""


def possbrds(board, tofill, toremove):
   global SEENWRDS
   postochoices = {}
   toreturn = set()
   for ind in tofill:
         hLen = hlen(board, ind, 1) if tofill[ind][0] else 0
         if hLen:
            constr = board[ind: ind+hLen]
            if constr in SEENWRDS:
               postochoices[str(ind)+"h"] = len(SEENWRDS[constr])
            else:
               for word in DICTIONARY[hLen]:
                  if word not in toremove[board]:
                     if validword(board, ind, word, "h", constr):
                        if not constr in SEENWRDS: SEENWRDS[constr] = {word}
                        if constr in SEENWRDS: SEENWRDS[constr].add(word)
                        if str(ind)+"h" in postochoices: postochoices[str(ind)+"h"] += 1
                        if str(ind)+"h" not in postochoices: postochoices[str(ind)+"h"] = 1
         vLen = vlen(board, ind, 1) if tofill[ind][1] else 0
         if vLen:
            constr = board[ind: ind+vLen*(WIDTH+2): WIDTH+2]
            if constr in SEENWRDS:
               postochoices[str(ind)+"v"] = len(SEENWRDS[constr])
            else:
               for word in DICTIONARY[vLen]:
                  if word not in toremove[board]:
                     if validword(board, ind, word, "v", constr):
                        if not constr in SEENWRDS: SEENWRDS[constr] = {word}
                        if constr in SEENWRDS: SEENWRDS[constr].add(word)
                        if str(ind)+"v" in postochoices: postochoices[str(ind)+"v"] += 1
                        if str(ind)+"v" not in postochoices: postochoices[str(ind)+"v"] = 1
   if not postochoices: return postochoices
   minposs = min(postochoices.values())
   poskey = -1
   for pos in postochoices:
      if postochoices[pos] == minposs:
         poskey = pos
         break
   for word in DICTIONARY[tofill[int(poskey[:len(poskey)-1])][poskey[-1]=="v"]]:
      if word not in toremove[board]:
         if validword(board, int(poskey[:len(poskey)-1]), word, poskey[-1], constr):
            newbrd = putword(board, int(poskey[:len(poskey)-1]), word, poskey[-1])
            toremove[newbrd] = {word}
            toreturn.add(newbrd)
   return toreturn

def removeborder(brd):
   brd = brd[WIDTH+2:len(brd)-WIDTH-2]
   brd = "".join([brd[ind+1: ind+WIDTH+1] for ind in range(0, len(brd), WIDTH+2)])
   return brd
 
def isSolved(board, ct):
    return ct == TOTALBLOCKS
 
def display2D(board):
    for rowPos in range(0, len(board), WIDTH):
        print(board[rowPos: rowPos+WIDTH])
 
def display2Dw(board, WIDTH):
    for rowPos in range(0, len(board), WIDTH):
        print(board[rowPos: rowPos+WIDTH])

def mirror(brd, ind, wrd):
   if brd[len(brd)-ind-1] == OPENCHAR:
      brd = brd[:len(brd)-ind-1] + wrd + brd[len(brd)-ind:]
   return brd
        
def collectivelyExhausted(board): # pz, len of 1 side, returns all puzzles that can fit in a dot
    toreturn = []
    for i in range(len(board)//2+1):
       if board[i] == OPENCHAR and board[len(board)-i-1] == OPENCHAR:
         newbrd = fillHV(board[:i] + "#" + board[i+1: len(board)-i-1] + BLOCKCHAR + board[len(board)-i:]) 
         if newbrd not in toreturn:
            toreturn.append(newbrd)
    return toreturn 
 
def display2D(pz):
    print("\n".join(pz[i:i + WIDTH] for i in range(0, len(pz), WIDTH)))
    print()
 
def isInvalid(brd, ct): #set of pairs of blocks
    if ct > TOTALBLOCKS:
       return True
    if not horizvert(brd):
       return True
    if not isconnected(brd):
       return True
    return False

def border(brd):
   return "#"*(WIDTH+2) + "".join(["#" + brd[i:i+WIDTH:1] + "#" for i in range(0, len(brd), WIDTH)]) + "#"*(WIDTH+2)
 
def isconnected(brd):
   brd = border(brd)
   if "-" in brd:
      ind = 0
      for i, c in enumerate(brd):
         if c != BLOCKCHAR:
            ind = i
            break
      c = connected(brd, ind)
      return not "-" in c
   return True
      
def connected(brd, ind, sym = ""): #! is the locations already viewed
   if not sym: sym = "!"
   if ind not in range(0,len(brd), 1):
      return ""
   if brd[ind] == BLOCKCHAR or brd[ind] == sym:
      return ""
   if brd[ind] != sym and brd[ind+1] in BLOCKCHAR+sym and brd[ind-1] in BLOCKCHAR+sym and brd[ind-WIDTH-2] in BLOCKCHAR+sym and brd[ind+WIDTH+2] in BLOCKCHAR+sym:
      return brd[:ind] + sym + brd[ind+1:]
   brd = brd[:ind] + sym + brd[ind+1:]
   if ind+1 in range(0, len(brd), 1) and brd[ind+1] != BLOCKCHAR and brd[ind+1] != sym:
      brd = connected(brd, ind+1, sym)
   if ind-1 in range(0, len(brd), 1) and brd[ind-1] != BLOCKCHAR and brd[ind-1] != sym:
      brd = connected(brd, ind-1, sym)
   if ind+WIDTH+2 in range(0, len(brd), 1) and brd[ind+WIDTH+2] != BLOCKCHAR and brd[ind+WIDTH+2] != sym:   
      brd =  connected(brd, ind+WIDTH+2, sym)
   if ind-WIDTH-2 in range(0, len(brd), 1) and brd[ind-WIDTH-2] != BLOCKCHAR and brd[ind-WIDTH-2] != sym:      
      brd = connected(brd, ind-2-WIDTH, sym)
   return brd
   
# WIDTH = 12
# d = "-----g*-#--------o*-#--------d*-#--------f*-####-----a*-----####-t*--------#-h*--------#-e*--------#-r*-----"
# print(isconnected(d))

def horizvert(brd):
   for ind, ch in enumerate(brd):
      if ch != BLOCKCHAR and (not vertcheck(brd, ind) or not horizcheck(brd, ind)):
         return False
   return True

def vertcheck(brd, ind):
   startpos, endpos = max(ind%WIDTH, ind-2*WIDTH), min(len(brd), ind+2*WIDTH+1)
   vertstr = "".join(["#-"[letter != BLOCKCHAR] for letter in brd[startpos:endpos:WIDTH]])
   return "---" in vertstr

def horizcheck(brd, ind):
   startpos, endpos = max((ind//WIDTH)*WIDTH, ind-2), min((ind//WIDTH+1)*WIDTH, ind+3)
   horzstr = "".join(["#-"[letter != BLOCKCHAR] for letter in brd[startpos: endpos]])
   return "---" in horzstr

#0  #1  #2  #3  #4  #5
#6  #7  #8  #9  #10 #11
#12 #13 #14 #15 #16 #17



def makeBoard():
    return OPENCHAR*int(WIDTH)*int(height)

def readfile(fi):
   dct = {}
   for word in fi.read().splitlines():
      if len(word) in dct and len(word)>2 and word.isalpha():
         dct[len(word)].add(word.lower())
      else:
         dct[len(word)] = {word.lower()}
   return dct
   
def letterdct():
   toret = {}
   for wordlen in DICTIONARY:   
      for word in DICTIONARY[wordlen]:
         for ind, letter in enumerate(word):
            if not (wordlen, letter, ind) in toret: toret[(wordlen, letter, ind)] = {word}
            else: toret[(wordlen, letter, ind)].add(word)
   return toret
   
   
def readInput(s):
    global height, WIDTH, TOTALBLOCKS, DICTIONARY, LETTERDCT
    s = s.lower().split(" ")
    if ".txt" in s[0]:
        file = open(args[0])
        DICTIONARY = readfile(file)
        LETTERDCT = letterdct()
        s = s[1:]
    hxw = s[0] #1: xw size
    height = h = int(hxw[:hxw.index("x")])
    WIDTH = w = int(hxw[hxw.index("x")+1:])
    TOTALBLOCKS = numblock = int(s[1]) #total blocks
    blocklist = [block for block in s if "h" in block or "v" in block]
    inputList = [h, w, numblock, blocklist]
    #print(inputList)
    return inputList #(area, s1, s2)
    
    
def mirrorbrd(brd):
    for i in range(len(brd)): #mirrors the board after putting in all the blocks
       if brd[i] != OPENCHAR and brd[i] != BLOCKCHAR:
          brd = mirror(brd, i, "*")
       if brd[i] == BLOCKCHAR:
          brd = mirror(brd, i, BLOCKCHAR)
    return brd

    
def centralsq(brd, blocknum):
   global OGBLOCKS
   if len(brd)%2 == 1: #inputs a block at the center if odd length with odd num blocking squares
       if blocknum%2 ==1:
            brd = brd[:len(brd)//2] + "#" + brd[len(brd)//2+1:]
       else:
         if brd[len(brd)//2] == OPENCHAR:
            brd = brd[:len(brd)//2] + "*" + brd[len(brd)//2+1:]
   return brd


def fillHV(brd): #check blocking squares --> fill horz and vert
   i = 0
   while i < len(brd):
      if brd[i] == BLOCKCHAR: 
        #  print(brd)
         brd = hsquares(brd, i) #fill in 
         brd = vsquares(brd, i)
      i+=1
   return brd

def itoxy(ind):
   return ind//WIDTH, ind%WIDTH

def vsquares(brd, ind):
   startpos, endpos = max(ind%WIDTH, ind-3*WIDTH), min(len(brd), ind+3*WIDTH+1)
   topstr = "".join([letter for letter in brd[startpos:ind:WIDTH]][::-1])
   botstr = "".join([letter for letter in brd[ind+WIDTH:endpos:WIDTH]])
   if "#" in topstr:
      i = topstr.find("#")
      x, y = itoxy(ind)
      brd = inputvert(brd, x-i, y, "#"*i)
   if len(topstr)<3:
      i = len(topstr)
      x, y = itoxy(ind)
      brd = inputvert(brd, x-i, y, "#"*i)
   if "#" in botstr:
      i = botstr.find("#")
      x, y = itoxy(ind)
      brd = inputvert(brd, x, y, "#"*i)
   if len(botstr)<3:
      i = len(botstr)
      x, y = itoxy(ind)
      brd = inputvert(brd, x+1, y, "#"*i)
   return brd 

def hsquares(brd, ind):
   startpos, endpos = max((ind//WIDTH)*WIDTH, ind-3), min((ind//WIDTH+1)*WIDTH, ind+4)
   leftstr = "".join([letter for letter in brd[startpos: ind]][::-1])
   rightstr = "".join([letter for letter in brd[ind+1: endpos]])
   if "#" in leftstr:
      i = leftstr.find("#")
      x, y = itoxy(ind)
      brd = inputhorz(brd, x, y-i, "#"*i)
   if len(leftstr)<3:
      i = len(leftstr)
      x, y = itoxy(ind)
      brd = inputhorz(brd, x, y-i, "#"*i)
   if "#" in rightstr:
      i = rightstr.find("#")
      x, y = itoxy(ind)
      brd = inputhorz(brd, x, y, "#"*i)
   if len(rightstr)<3:
      i = len(rightstr)
      x, y = itoxy(ind)
      brd = inputhorz(brd, x, y+1, "#"*i)
   return brd 
   
def fillchunks(brd):
   oldbrd = brd
   strsyms = "!$?^%"
   brd = border(brd)
   i = 0
   while OPENCHAR in brd: #fills each - in the board until there is no more
      brd = connected(brd, brd.index(OPENCHAR), strsyms[i])
      i += 1
   brd = brd[WIDTH+2:len(brd)-WIDTH-2]
   brd = "".join([brd[ind+1: ind+WIDTH+1] for ind in range(0, len(brd), WIDTH+2)])
   theSym = ""
   for ind, ch in enumerate(brd): #if it is symetrival across the axis, get rid of other parts of brd
      if ind > len(brd)//2+1:
         break
      if ch != BLOCKCHAR:
         if ch == brd[len(brd)-ind-1]:
            theSym = ch
            break
   returnbrd = ""
   for ind, letter in enumerate(brd):
      if letter != theSym:
         returnbrd += BLOCKCHAR
      else:
         returnbrd += oldbrd[ind]
   return returnbrd
          
    
def autofill(brd, blocknum, blocklist):
    global OGBLOCKS
    if blocknum == WIDTH*height:
       OGBLOCKS = blocknum
       return brd.replace(OPENCHAR, BLOCKCHAR)
    for block in blocklist: #put the blocks into the board
       brd = inputvals(brd, block)
    if len(brd) - blocknum == 9:
       OGBLOCKS = blocknum
       return inputsq(brd, height//2-1, WIDTH//2-1, 3).replace("-", "#").replace("*", "-")
    if len(brd) - blocknum == 16:
       OGBLOCKS = blocknum
       return inputsq(brd, height//2-2, WIDTH//2-2, 4).replace("-", "#").replace("*", "-")
    if len(brd) - blocknum == 14:
       OGBLOCKS = blocknum
       return inputsq(inputsq(brd, height//2-2, WIDTH//2-2, 3), height//2-1, WIDTH//2-1, 3).replace("-", "#").replace("*", "-")
    brd = mirrorbrd(brd)
    brd = centralsq(brd, blocknum)
    brd = fillHV(brd)
    if not isconnected(brd): brd = fillchunks(brd)
    OGBLOCKS = brd.count(BLOCKCHAR)
    return brd

def inputvals(brd, block):
    global OGBLOCKS
    indw2 = block.index("x")+1 #starting ind of second work
    endw2 = indw2+2 if (len(block)>indw2+1 and block[indw2+1] in "0123456789") else indw2+1
    x, y, word = int(block[1:indw2-1]), int(block[indw2:endw2]), block[endw2:]
    if not word:
       brd = inputhorz(brd, x, y, "#")
       return brd
    if block[0] == "h":
       brd = inputhorz(brd, x, y, word)
    if block[0] == "v":
       brd = inputvert(brd, x, y, word)
    return brd

def inputsq(brd, x, y, sL):
    for ind in range(sL):
       brd = inputhorz(brd, ind+x, y, "*"*sL)
    return brd

def inputvert(brd, x, y, word):
    startpos = x*WIDTH + y
    lbrd = [*brd]
    for ind, chr in enumerate(word):
       if lbrd[startpos + ind*WIDTH] in "*"+OPENCHAR:
          lbrd[startpos + ind*WIDTH] = chr
    return "".join(lbrd)
   
def inputhorz(brd, x, y, word):
    startpos = x*WIDTH + y
    newbrd = brd[:startpos] 
    for i in range(len(word)):
       if brd[startpos+i] in "*"+OPENCHAR:
          newbrd += word[i]
       else:
          newbrd += brd[startpos+i]
    newbrd += brd[startpos+len(word):]
    return newbrd
  
def putword(brd, startpos, word, ori):
   if ori == "h":
      return puthorzword(brd, startpos, word)
   if ori == "v":
      return putvertword(brd, startpos, word, WIDTH +2)
   return ""   
              
def puthorzword(brd, startpos, word):
    newbrd = brd[:startpos] 
    for i in range(len(word)):
       if brd[startpos+i] in "*"+OPENCHAR:
          newbrd += word[i]
       else:
          newbrd += brd[startpos+i]
    newbrd += brd[startpos+len(word):]
    return newbrd        

def putvertword(brd, startpos, word, width):
    lbrd = [*brd]
    for ind, chr in enumerate(word):
       if lbrd[startpos + ind*width] in "*"+OPENCHAR:
          lbrd[startpos + ind*width] = chr
    return "".join(lbrd)
        
def main():
    global startPzTime
    if args:
        inputs = " ".join(args)
        startPzTime = time.process_time()
        inputList = readInput(inputs)
        brd, numblocks, blockList = makeBoard(), inputList[2], inputList[3]
        brd = autofill(brd, numblocks, blockList)
        if not isSolved(brd, OGBLOCKS):
            brd = bruteForce(brd, numblocks-OGBLOCKS).replace("*", "-")
            display2D(brd)#print("New board: ")
        brd = brd.replace("*", "-")
      #   display2D(brd)
        brd = solve(brd)
        display2D(brd)        
        #print(startPzTime-time.process_time())

    else: 
        inputList = readInput("dct20k.txt 3x3 9") #reads input, sets WH global
        brd, numblocks, blockList = makeBoard(), inputList[2], inputList[3]
        brd = autofill(brd, numblocks, blockList)
        fillchunks(brd)
        print("Old board: ")
        display2D(brd.replace("*", "-"))
        print(brd +" \n")
        if not isSolved(brd, OGBLOCKS):
            brd = bruteForce(brd, numblocks-OGBLOCKS).replace("*", "-")
            print("New board: ")
            display2D(brd)
        
 
if __name__ == "__main__":main()
 
print(f'\nTime: {float(time.process_time()- startTime):.3g}s')

#0 #1  #2
#2 #0 #1
#1 #2 #0
 
#0  #   #   #3
#   #5  #6  #
#   #9  #10 #
#12 #   #   #15
 
#0  #   #   #  #4
#   #6  #   #8  #
#   #   #12 #   #
#   #16 #   #18 #
#20 #   #   #   #24
 
#Stephanie Song, P6, 2024
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# if tofill[thepos][0] == thelen: # horz length
#       for wrd in DICTIONARY[thelen]:
#          if validword(board, thepos, wrd, "h") and wrd not in toremove:
#             toremove.add(wrd)
#             board = puthorzword(board, thepos, wrd, WIDTH+2)
#             break
#    if tofill[thepos][1] == thelen: # vert length
#       for wrd in DICTIONARY[thelen]:
#          if validword(board, thepos, wrd, "v") and wrd not in toremove:
#             toremove.add(wrd)
#             board = putvertword(board, thepos, wrd, WIDTH+2)
#             break

# def lentofill(brd): #finds length, orientation of word and and pos of word
#    posandlen = {}
#    for i, pc in enumerate(brd):
#       if i < WIDTH+3:
#          continue
#       if i> len(brd)-WIDTH-3:
#          continue
#       if pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR and brd[i-1] == BLOCKCHAR:
#          h = hlen(brd, i)
#          if OPENCHAR in brd[i: i+h]:
#             if h and h in posandlen: posandlen[h].add((i, "h"))
#             if h and h not in posandlen: posandlen[h] = {(i, "h")}
#          v = vlen(brd, i)
#          if OPENCHAR in brd[i: i+(WIDTH+2)*v: WIDTH+2]:
#             if v and v in posandlen: posandlen[v].add((i, "v"))
#             if v and v not in posandlen: posandlen[v] = {(i, "v")}
#       elif  pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR:
#          v = vlen(brd, i)
#          if OPENCHAR in brd[i: i+(WIDTH+2)*v: WIDTH+2]:
#             if v and v in posandlen: posandlen[v].add((i, "v"))
#             if v and v not in posandlen: posandlen[v] = {(i, "v")}
#       elif pc != BLOCKCHAR and brd[i-1] == BLOCKCHAR:
#          h = hlen(brd, i)
#          if OPENCHAR in brd[i: i+h]:
#             if h and h in posandlen: posandlen[h].add((i, "h"))
#             if h and h not in posandlen: posandlen[h] = {(i, "h")}
#    return posandlen


# def lentopos(brd): #finds length, orientation of word and and pos of word
#    posandlen = {}
#    for i, pc in enumerate(brd):
#       if i < WIDTH+3:
#          continue
#       if i> len(brd)-WIDTH-3:
#          continue
#       if pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR and brd[i-1] == BLOCKCHAR:
#          h = hlen(brd, i, 1)
#          if h and h in posandlen: posandlen[h].add((i, "h"))
#          if h and h not in posandlen: posandlen[h] = {(i, "h")}
#          v = vlen(brd, i)
#          if v and v in posandlen: posandlen[v].add((i, "v"))
#          if v and v not in posandlen: posandlen[v] = {(i, "v")}
#       elif  pc != BLOCKCHAR and brd[i-WIDTH-2] == BLOCKCHAR:
#          v = vlen(brd, i)
#          if v and v in posandlen: posandlen[v].add((i, "v"))
#          if v and v not in posandlen: posandlen[v] = {(i, "v")}
#       elif pc != BLOCKCHAR and brd[i-1] == BLOCKCHAR:
#          h = hlen(brd, i)
#          if h and h in posandlen: posandlen[h].add((i, "h"))
#          if h and h not in posandlen: posandlen[h] = {(i, "h")}
#    return posandlen


# def generatewrd(board, pos, wrdlen, ori, toremove):
#    wrd = ""
#    if ori == "h": 
#       for wrd in DICTIONARY[wrdlen]:
#          if validword(board, pos, wrd, "h") and wrd not in toremove[board]:
#             return wrd
#    if ori == "v": 
#       for wrd in DICTIONARY[wrdlen]:
#          if validword(board, pos, wrd, "v") and wrd not in toremove[board]:
#             return wrd
#    return 11

#Stephanie Song, P6, 2024