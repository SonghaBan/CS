# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
from hangman import *
class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.word = ''
        self.game = Hangman(self.word)

    def set_state(self, state):
        self.state = state
        
    def get_state(self):
        return self.state
    
    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me
    
    def game_to(self, peer):
        msg = M_HANGMAN + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_HANGMAN+'ok'):
            self.peer = peer
            return True
        elif response == (M_HANGMAN + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_HANGMAN + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False) 
    
    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT+'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_code, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:
                
                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE
                    
                elif my_msg[0] == 'h':
                    peer = my_msg[1:].strip()                    
                    if self.game_to(peer) == True:
                        self.out_msg += "Invite sent. Waiting for the other player's response..."                        
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        
                elif my_msg[0] == 'Y':
                    self.peer = my_msg[1:].strip()
                    msg = M_RESPONSE + 'Y' + self.peer
                    mysend(self.s, msg)
                    
                elif my_msg[0] == 'N':
                    self.peer = my_msg[1:].strip()
                    msg = M_DECLINE + 'N' + self.peer
                    mysend(self.s, msg)
                        
                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in
                            
                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in
                            
                elif my_msg[0] == 'c':
                    peer = my_msg[1:].strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                        
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'
                        
                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem = myrecv(self.s)[1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'
                        
                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer 
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                
                elif peer_code == M_REQUEST:
                    self.peer = peer_msg
                    self.out_msg += "Invite from " + self.peer + " to play Hangman!\n "
                    self.out_msg += "Type 'Y " + self.peer + "' to accept\n"
                    self.out_msg += "Type 'N " + self.peer + "' to  decline"
                    peer_code = M_RESPONSE
                
                elif peer_code == M_WORDPICKER:
                    self.peer = peer_msg
                    self.out_msg += self.peer + " has accepted the invite\n"
                    self.out_msg += "What is the word: "
                    
                    self.state = S_GAMING
                    
                
                elif peer_code == M_GUESSER:
                    #self.peer = peer_msg
                    self.out_msg += 'You are now playing hangman'
                    self.state = S_GAMING
                    self.word = peer_msg[1:].strip()
                    self.game = Hangman(self.word)
                    self.out_msg += self.game.get_display()
                    
                elif peer_code == M_DECLINE:
                    if peer_msg == self.me:
                        self.out_msg += peer + 'You have left the game with ' + peer_msg
                    else:
                        self.out_msg += peer_msg + " has left the game"
                
                elif peer_code == M_QUIT:
                    self.out_msg += peer + ' has refused the invtive'
            
#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # My stuff, going out
                mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_GAMING
                    self.peer = ''
            if len(peer_msg) > 0:   # Peer's stuff, coming in
                # New peer joins
                if peer_code == M_CONNECT:
                    self.out_msg += "(" + peer_msg + " joined)\n"
                else:
                    self.out_msg += peer_msg

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_GAMING

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu
        
        elif self.state == S_GAMING:                        
            if len(my_msg) == 1:
                mysend(self.s, M_GUESSING + my_msg)
                self.game.letter_guess(my_msg)
                self.out_msg += self.game.get_gallows()
                self.game.display_letters()
                self.out_msg += self.game.get_display()[:len(self.word)*2+6]
                mysend(self.s, M_DISPLAY + my_msg + self.game.get_gallows()\
                + self.game.get_display()[:len(self.word)*2+6])
                

            elif len(my_msg) > 0:     # my stuff going out
                mysend(self.s, M_GUESSING + my_msg)
                if len(my_msg) == len(self.word):
                    self.game.word_guess(my_msg)
                    self.out_msg += self.game.get_gallows()
                    self.game.display_letters()
                    self.out_msg += self.game.get_display()[:len(self.word)*2+6]
                    mysend(self.s, M_DISPLAY + my_msg + self.game.get_gallows()\
                    + self.game.get_display()[:len(self.word)*2+6])
                if my_msg == 'quit':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
                if my_msg == 'hint':
                    mysend(self.s, M_CONNECT)
                    self.connect_to(self.peer)
                    self.state = S_CHATTING
                    
            if peer_code == M_DISPLAY:
                self.out_msg += peer_msg
                
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN
            
            if peer_code == M_CONNECT:
                self.state = S_CHATTING

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

            
           
#==============================================================================
# invalid state                       
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)
            
        return self.out_msg
