import random
import numpy as np
#changes
f = open("words.txt","r")
wordList = []
for i in f:
    wordList = np.append(wordList, i[:-1])
wordList[-1] = 'pupal'
wordList.sort()

valid = list(wordList.copy())
toRemove = []
bannedLetters = []
wrongPlace = [[],[],[],[],[]]
correctPlace = ['','','','','']
found = False

def repeatFree(word):
    for i in word:
        if word.count(i)>1:
            return False
    return True

def pickWord(validList):
    random.shuffle(validList)
    for i in validList:
        if repeatFree(i):
            return i
    
    return random.choice(validList)

counter = 0
while not found:
    if counter == 0: #first guess always crane
        guess = "crane"
        print("Use:", guess)
        counter += 1
    else:
        guess = pickWord(valid)
        print("Use:", guess)
    outcome = input('Input Outcome(0,1,2, no, yes): ') #0 = wrong, 1 = wrong place, 2 = correct place, no = reroll word
    if outcome == "no":
        toRemove.append(guess)
    elif outcome == "22222" or outcome == "yes":
        break

    else:
        for i in range(len(outcome)):
            if outcome[i] == "2":
                correctPlace[i] = guess[i]
            elif outcome[i] == "1":
                wrongPlace[i].append(guess[i])
            else:
                if guess[i] not in correctPlace:
                    bannedLetters.append(guess[i])
    
        #sometimes repeated letters need to be cleaned up
        bannedLetters = [i for i in bannedLetters if i not in correctPlace]
        for i in wrongPlace:
            bannedLetters = [j for j in bannedLetters if j not in i]

        for i in valid:
            contFlag = False
            for j in bannedLetters:
                if j in i:
                    toRemove.append(i)
                    contFlag = True
                    break
            if contFlag == True:
                continue

            for j in range(len(correctPlace)):
                if i[j] != correctPlace[j] and correctPlace[j] != '':
                    toRemove.append(i)
                    contFlag = True
                    break
            if contFlag == True:
                continue

            for j in range(len(wrongPlace)):
                if i[j] in wrongPlace[j]:
                    toRemove.append(i)
                    contFlag = True
                    break
                for k in wrongPlace[j]:
                    if k not in i:
                        toRemove.append(i)
                        contFlag = True
                        break
            if contFlag == True:
                continue

        print(bannedLetters)
        print(wrongPlace)
        print(correctPlace)
    valid = [i for i in valid if i not in toRemove]
    if len(valid) < 10:
        print(valid)

    if(len(valid) == 1):
        break

input("got it :)")

            
        
