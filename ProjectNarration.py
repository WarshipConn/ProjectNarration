import random

#Constants
MAX_SENT_LIM = 50 #Maximum allowed words in one generation to prevent possible infinite recursion
PUNCTS = (".", "?", "!") #Currently accepted punctuations

TEST_TRAIN_SENT = (
    "a b.",
    "b c.",
    "a c."
)

#Training sentences requirements:
#Each entry should be exactly one full sentence
#Single independant clause only, no commas. Examples included the provided simple sentences below.
#There are a limit to currently accepted ending punctuation, which include '.', '?', and '!'. See the PUNCTS constant tuple above.
#Please double check for typos or weird syntax.
#(Optional: Try to make the sentences share common words, which introduces more possible paths for the program to take, thereby improving "creativity")
TRAIN_SENT = (
    "The cat is sleeping on the mat.",
    "I enjoy reading books in my free time.",
    "She greeted me with a warm smile.",
    "The students are studying for their exams.",
    "They went for a walk in the park.",
    "The flowers in the garden are blooming beautifully.",
    "She is wearing a red dress to the party.",
    "They built a sandcastle on the beach.",
    "We visited the museum to see the art exhibition.",
    "The baby giggled at the funny sounds.",
    "He fixed the broken chair with a hammer.",
    "The birds are chirping in the trees.",
    "She danced gracefully on the stage.",
    "He painted a beautiful landscape on the canvas.",
    "The rain is pouring heavily outside.",
    "She gave a speech at the conference.",
    "He won a gold medal in the swimming competition.",
    "The children played happily in the playground.",
    "They built a snowman in the backyard.",
    "We took a family photo during the vacation.",
    "I solved the puzzle in record time.",
    "They went on a road trip across the country.",
    "We attended a music concert in the city.",
    "I practiced playing the piano every day.",
    "They enjoyed a sunset cruise on the lake.",
    "We volunteered at a local charity event."
)


trainedMatrix = {
    #"SampleWord" : [[NextWords], [NextProbs]]

}

#Helpers

def processSentence(sentence):
    chunks = []
    nextChunk = ""

    for i in sentence:
        if i in PUNCTS:
            chunks.append(nextChunk)
            nextChunk = ""

            chunks.append(i)
        elif i == " ":
            if len(nextChunk) > 0:
                chunks.append(nextChunk)
                nextChunk = ""
        else:
            nextChunk += i
    
    return chunks

def probabilityGradient(probs):
    total = sum(probs)
    return [i/total for i in probs]

def concat(chkLst):
    result = ""

    for chk in chkLst:
        if chk in PUNCTS:
            result += chk
        else:
            result += " " + chk 

    return result

#Main functions

def train(trainingSentences, targetMatrix):
    for sen in trainingSentences:
        procSen = processSentence(sen)

        for i in range(len(procSen)):
            chk = procSen[i]
            prevChk = procSen[i-1] if i > 0 else None


            if not chk in PUNCTS and not chk in targetMatrix.keys():
                targetMatrix[chk] = [[], []]
            
            if prevChk is not None:

                if chk in targetMatrix[prevChk][0]:
                    updatedWrdList = targetMatrix[prevChk][0]
                    updatedProbList = targetMatrix[prevChk][1]

                    chkIndex = updatedWrdList.index(chk)
                    updatedProbList[chkIndex] += 1

                    targetMatrix.update({prevChk : [updatedWrdList, updatedProbList]})
                else:
                    updatedWrdList = targetMatrix[prevChk][0]
                    updatedProbList = targetMatrix[prevChk][1]

                    updatedWrdList.append(chk)
                    updatedProbList.append(1)

                    targetMatrix.update({prevChk : [updatedWrdList, updatedProbList]})

def selectValue(probs):
    gradient = probabilityGradient(probs)
    target = random.random()
    total = 0
    result = 0

    for bound in gradient:
        total += bound

        if target <= total:
            return result
        result += 1

    print("technically shouldn't be seeing this but ok")
    return len(gradient) - 1


def generate(startWrd, matrix):
    sent = [startWrd]

    if not startWrd in matrix.keys():
        print("Starting word hasn't been learnt before")
        return None

    def generateRec(prevWrd):
        if len(sent) >= MAX_SENT_LIM:
            return False
        else:
            nxtWords = matrix[prevWrd][0]
            nextProbs = matrix[prevWrd][1]

            nxtWord = nxtWords[selectValue(nextProbs)]
            sent.append(nxtWord)

            if nxtWord in PUNCTS:
                return True
            else:
                return generateRec(nxtWord)

    outcome = generateRec(startWrd)

    if outcome:
        print("Success, returning current result")
        return(concat(sent))
    else:
        print("Exceeded maximum word limit, returning current result")
        return(sent)
    

#Actual process

train(TRAIN_SENT, trainedMatrix)


#Make a random starting word
#Please make sure that the starting word is included in the training sentences
START_WORDS = ("I", "He", "She", "They", "The")
startWrd = START_WORDS[int(random.random() * len(START_WORDS))]

print(generate(startWrd, trainedMatrix))



