import random
import time
from tkinter import *

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
    "We volunteered at a local charity event.",
    "I enjoy reading books in my free time.",
    "The sun is shining brightly in the sky.",
    "He played the guitar at the concert.",
    "We had a delicious dinner at the restaurant.",
    "I love watching movies on weekends.",
    "He ran quickly to catch the bus.",
    "The clock on the wall is ticking loudly.",
    "She wrote a heartfelt letter to her best friend.",
    "They planted vegetables in their backyard.",
    "I bought a new laptop for my work.",
    "We enjoyed a picnic by the lake.",
    "They cheered loudly for their favorite team.",
    "I baked cookies for the school bake sale.",
    "We hiked up the mountain to enjoy the view.",
    "They adopted a puppy from the animal shelter.",
    "I wrote a poem about nature.",
    "She sang a song with a melodious voice.",
    "The car broke down on the way to the party.",
    "He cooked a delicious meal for his friends.",
    "She knitted a cozy scarf for the winter.",
    "The baby took its first steps.",
    "He gave a presentation to the board of directors.",
    "She baked a cake for her sister's birthday.",
    "The train arrived at the platform on time.",
    "He studied late into the night for the exam.",
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

class App:
    def __init__(self, master, matrix):
        self.matrix = matrix
        self.master = master

        frame = Frame(master, bg="lightblue")
        frame.pack(fill=BOTH, expand=1)

        rerun_button = Button(frame, text="Rerun", command=self.rerun)
        rerun_button.place(x=50, y=100)
        #rerun_button.grid(row=0, column=0)

        clear_button = Button(frame, text="Clear", command=self.clear)
        clear_button.place(x=100, y=100)
        #clear_button.grid(row=1, column=0)

        self.status = Label(frame, text="...", wraplength=950, font=("Arial", 20))
        self.status.place(x=10, y=10)

    def rerun(self):
        START_WORDS = ("I", "He", "She", "They", "The")
        startWrd = START_WORDS[int(random.random() * len(START_WORDS))]

        sent = [startWrd]

        if not startWrd in self.matrix.keys():
            print("Starting word hasn't been learnt before")
            return None

        def generateRec(prevWrd):
            if len(sent) >= MAX_SENT_LIM:
                return False
            elif prevWrd in PUNCTS:
                return True
            else:
                #print(self.matrix)
                nxtWords = self.matrix[prevWrd][0]
                nextProbs = self.matrix[prevWrd][1]

                nxtWord = nxtWords[selectValue(nextProbs)]
                sent.append(nxtWord)

                #time.sleep(0.5)

                if nxtWord in PUNCTS:
                    return True
                else:
                    generateRec(nxtWord)

        generateRec(startWrd)

        print(sent)
        #self.status.config(text=concat(sent_str))
        sent_str = []
        current_word_index = 0

        def updateTxt():
            nonlocal current_word_index, sent_str
            if current_word_index < len(sent):
                sent_str += [sent[current_word_index]]
                current_word_index += 1
                self.status.config(text=concat(sent_str))
                root.after(100, updateTxt)  # Schedule next update after 1 second
        
        updateTxt()

    
    def clear(self):
        self.status.config(text="...")
        print("clear")



root = Tk()
root.minsize(1000, 200)
root.resizable(False, False)
root.wm_title("Project Narration")

app = App(root, trainedMatrix)

root.mainloop()


#Make a random starting word
#Please make sure that the starting word is included in the training sentences



