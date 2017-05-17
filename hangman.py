import random


class Hangman:

    def __init__(self, word):  
        self.display = []
        self.word = word
        self.used = []
        self.wrong = 0
        self.win = 0
        self.alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                          'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        

    #Setters
    def set_word(self, word):
        self.word = word

    def set_gallows(self, gallows):
        self.gallows = gallows
        
    def set_display(self, display):
        self.display = display

    def set_guess(self, guess):
        self.guess = guess

    def set_used(self, used):
        self.used = used
        
    def set_win(self, win):
        self.win = win
        
    def set_wrong(self, wrong):
        self.wrong = wrong

    #Getters
    def get_displaylist(self):
        return self.display

    def get_guess(self):
        return self.guess

    def get_used(self):
        return self.used
        
    def get_win(self):
        return self.win
        
    def get_wrong(self):
        return self.wrong

    #Methods
    def get_display(self):
        word_disp = ''
        for i in self.word:
           self.display.append("_ ")
        for j in self.display:
            word_disp += j

        return "Word: " + word_disp
    
    def get_gallows(self): #Returns graphic representation of gallows
        
        gall_1 = """         ------
        /    |
        |    
        |   
        |   
                     """
        gall_2 = """         ------
        /    |
        |    o
        |   
        |   
                     """
        gall_3 = """         ------
        /    |
        |    o
        |    |
        |   
                     """
        gall_4 = """         ------
        /    |
        |    o
        |   /|
        |   
                     """
        gall_5 = """         ------
        /    |
        |    o
        |   /|\\
        |   
                     """
        gall_6 = """         ------
        /    |
        |    o
        |   /|\\
        |   /
        """
        final_gall = """         ------
        /    |  GAME OVER
        |    o
        |   /|\\
        |   / \\
        
        Please type 'quit' to end game
        """
        win_gall = """
         \o/  YOU WIN!
          |
         / \\
         
         
        Please type 'quit' to end game
        """
        if self.win == len(self.word):
            return win_gall
        elif self.wrong == 6:
            return final_gall
        elif self.wrong == 5:
            return gall_6
        elif self.wrong == 4:
            return gall_5
        elif self.wrong == 3:
            return gall_4
        elif self.wrong == 2:
            return gall_3
        elif self.wrong == 1:
            return gall_2
        elif self.wrong == 0:
            return gall_1
            
    def display_letters(self):
        for i in self.alphabets:
            print(i, end = ' ')
        print('')

    def word_guess(self, guess):
        if len(guess) == len(self.word): #Allows users to guess a whole word at a time
            print("You are ambitious!")
            if guess == self.word:
                print("You guessed the word, congrats!")
                self.win = len(self.word)
                print(self.get_gallows()) 
            else:
                print("Incorrect. Guess more letters")
                self.wrong += 1
                print(self.get_gallows()) 
        pass
        
    def letter_guess(self, guess): #Processes one letter guesses 
        update = ""
        count = 0
        index = 0
        for l in range(len(self.alphabets)):
            if self.alphabets[l] == guess.lower():
                self.alphabets[l] = guess.lower() + '\u0336'
        for i in self.word:
            if i == guess:
                self.display[index] = guess + " "
                count += 1
                index += 1
                self.win += 1
            else:
                index += 1
        if count > 0:
            print("You revealed",count,"letters!")
        else:
            print("Try again!")
            self.wrong += 1
            self.add_guess(guess)
        for i in self.display:
            update += i
        return "Word:   " + update

    def add_guess(self, guess):
        guessed = ''
        if guess in self.used:
            print("You already guessed this letter!")
        else:
            self.used.append(guess)
        for i in self.used:
            guessed += str(i) + ", "
        return "Guessed Letters: " + guessed
        
    def play(self):
        print("Welcome to Hangman!")
        print("Help: Type quit to leave")
        print(self.get_display())
        print(self.get_gallows())
        
        while (len(self.used) != 27):
            self.display_letters()
            guess = str(input("Guess a letter or the word: "))
            print(self.add_guess(guess))
            if guess != "quit":
                if len(guess) == len(self.word):
                   print(self.word_guess(guess))
                elif len(guess) == 1:
                    print(self.letter_guess(guess))
                    print(self.get_gallows())                   
                else:
                    print("Invalid guess! Try again!")
                if (self.get_win() == len(self.word)):
                    break 
                if (self.get_wrong() == 6):
                    print("The word was \""+ self.word +"\"")
                    break
            else:
                print("Thanks for playing!")
                break
            
            
        
            

    
