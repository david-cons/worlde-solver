import math

TRIES = 6
FILE = 'words'

secret = 'lamps'
all_words = []

def wordle():
    global all_words
    all_words = get_word_db()
    guesses_so_far = []
    highlights_so_far = []
    
    for i in range(TRIES):
        guesses_so_far.append(guess(guesses_so_far))

        if guesses_so_far[i] == secret:
            return 1
        
        highlights_so_far.append(get_highlight(guesses_so_far[-1],secret=secret))
        print(highlights_so_far[-1])
        print('calculating')

        print(suggestion(guesses_so_far, highlights_so_far))
        print('done calculating')

    return -1


def guess(guesses_so_far):
    guessed_word = input().lower()
    if len(guessed_word) == 5 and guessed_word not in guesses_so_far and guessed_word in all_words: #additional check for dictionary here
        return guessed_word
    else:
        return guess(guesses_so_far)
    
def get_highlight(guess,secret):
    highlight = ['','','','','']

    for i in range(len(guess)):
        if guess[i] == secret[i]:
            highlight[i] = 'G'

        elif guess[i] in secret and highlight[i] != 'G':
            for j in range(len(secret)):
                if guess[i] == secret[j]:
                    if highlight[j] != 'G':
                       highlight[i] = 'Y'

        elif highlight[i] == '':
            highlight[i] = '_'    

    return highlight
        

def get_word_db():
    with open(FILE) as f:
        all_words = f.read().splitlines()
    return all_words

def calculate_entropy(guess):
    probabilities = {}

    for i in all_words:
        highlight = str(get_highlight(guess,i))
        if highlight not in probabilities:
            probabilities[highlight] = 1
        else: 
            probabilities[highlight] += 1

    for i in probabilities:
        p = probabilities[i]/len(all_words)
        info = -math.log2(p)
        probabilities[i] = (p,info)

    entropy = 0
    for i in probabilities:
        entropy += probabilities[i][0] * probabilities[i][1]

    return entropy

def alt_matched_cases(guesses_so_far, highlights_so_far):
    matched_words = []
    alphabet = 'a b c d e f g h i j k l m n o p q r s t u v w x y z'
    match_shape  = [alphabet.split().copy() for i in range(5)]
    letters_in = []

    for j in range(len(guesses_so_far)):
        for k in range(len(guesses_so_far[j])):
            letter = guesses_so_far[j][k]
            letter_highlight = highlights_so_far[j][k]

            if letter_highlight == 'G':
                match_shape[k] = letter
                letters_in.append(letter)

            elif letter_highlight == 'Y':
                while letter in match_shape[k]:
                    match_shape[k].remove(letter)

                letters_in.append(letter)

                for t in range(len(match_shape)):
                    if t != k:
                        if letter != match_shape[t] and letter in match_shape[t]:
                            if not isinstance(match_shape[t],str):
                                match_shape[t].append(letter)
            
            elif letter_highlight == '_':
                for t in range(len(match_shape)):
                    if not isinstance(match_shape[t],str) and letter in match_shape[t]:
                        match_shape[t].remove(letter)
    
    for i in match_shape:
        print(i)

    for i in all_words:
        cond = True
        for j in range(len(match_shape)):
            if i[j] not in match_shape[j] and i[j] != match_shape[j]:
                cond = False
        
        for j in letters_in:
            if j not in i:
                cond = False

        if cond == True:
            matched_words.append(i)

    print(len(matched_words))

    return matched_words

def suggestion(guesses_so_far, highlights_so_far):
    word_entropy = {}

    matched_words = alt_matched_cases(guesses_so_far, highlights_so_far)
    for i in matched_words:

        if i in guesses_so_far:
            matched_words.remove(i)
            continue

        word_entropy[i] = calculate_entropy(i)

    sorted_entropy = sorted(word_entropy.items(), key=lambda x: x[1])
    sorted_entropy.reverse()

    return sorted_entropy[:10] #if len(sorted_entropy)>=10 else len(sorted_entropy)])    
    
    
def alt_wordle():
    global all_words
    all_words = get_word_db()
    guesses_so_far = []
    highlights_so_far = []

    while True:
        guesses_so_far.append(input('guess: ').lower())
        highlights_so_far.append(input('highlight: ').split())
        if input('more? ') == 'y':
            continue
        else:
            print(suggestion(guesses_so_far, highlights_so_far))
        

if __name__ == '__main__':
    print(wordle())