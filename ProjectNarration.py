import random

MAX_SENT_LIM = 50
PUNCTS = (".", "?", "!")

TEST_TRAIN_SENT = (
    "a b.",
    "b c.",
    "a c."
)

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

def train():
    for sen in TRAIN_SENT:
        procSen = processSentence(sen)

        for i in range(len(procSen)):
            chk = procSen[i]
            prevChk = procSen[i-1] if i > 0 else None


            if not chk in PUNCTS and not chk in trainedMatrix.keys():
                trainedMatrix[chk] = [[], []]
            
            if prevChk is not None:
                #targetIndex = [trainedMatrix.keys].index(prevChk)

                if chk in trainedMatrix[prevChk][0]:
                    updatedWrdList = trainedMatrix[prevChk][0]
                    updatedProbList = trainedMatrix[prevChk][1]

                    chkIndex = updatedWrdList.index(chk)
                    updatedProbList[chkIndex] += 1

                    trainedMatrix.update({prevChk : [updatedWrdList, updatedProbList]})
                else:
                    updatedWrdList = trainedMatrix[prevChk][0]
                    updatedProbList = trainedMatrix[prevChk][1]

                    updatedWrdList.append(chk)
                    updatedProbList.append(1)

                    trainedMatrix.update({prevChk : [updatedWrdList, updatedProbList]})

def selectValue(probs):
    gradient = probabilityGradient(probs)
    target = random.random()
    total = 0
    result = 0

    for bound in gradient:
        total += bound

        if target < total:
            return result
        result += 1

    print("technically shouldn't be seeing this but ok")
    return len(gradient) - 1


def generate(startWrd):
    sent = [startWrd]

    if not startWrd in trainedMatrix.keys():
        print("Starting word hasn't been learnt before")

    def generateRec(prevWrd):
        if len(sent) >= MAX_SENT_LIM:
            return False
        else:
            nxtWords = trainedMatrix[prevWrd][0]
            nextProbs = trainedMatrix[prevWrd][1]

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
    



train()

START_WORD = "She"

print(generate(START_WORD))



