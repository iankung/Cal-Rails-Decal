''' Blackjack by Ian Kung'''

def player_wins(myhand,dealerhand):
    '''Returns true if player wins against dealer hand'''
    if myhand.totalvalue <= 21:
        if dealerhand.totalvalue > 21:
            return True
        elif myhand.totalvalue > dealerhand.totalvalue:
            return True
        elif myhand.totalvalue < dealerhand.totalvalue:
            return False
        elif myhand.totalvalue == dealerhand.totalvalue:
            return False
        else:
            return
    else:
        return False

def insurance_play():
    '''Offers insurance. Then runs cases where dealer either has or doesn't have
       blackjack. If insurance is wanted then player is allowed to bet up to half
       of original bet.  
    '''
    global balance
    global bet
    insurancechoice = 'empty'
    while insurancechoice == 'empty':
        insurancechoice = input('Would you like insurance? ')
        
        if insurancechoice == 'no':
            if dealerhand.totalvalue == 21 and playerhand.totalvalue != 21:
                balance = balance - bet
                print('Dealer has blackjack, you lose ' + str(bet))
                continue
        elif insurancechoice == 'yes':
            
            insurancebet = 'empty'
            while insurancebet == 'empty':
                insurancebet = input('Enter insurance amount (max is: '
                                     + str(.5*bet) + '):' )
                
                if str.isdigit(insurancebet) and int(insurancebet) <= (.5*bet):
                    insurancebet = int(insurancebet)
                else:
                    insurancebet = 'empty'
                    
            if dealerhand.totalvalue == 21:
                balance = balance - (bet - 2*insurancebet)
                print('Dealer has blackjack. You lose: '
                      + str(bet - insurancebet*2))
                continue
            elif dealerhand.totalvalue != 21:
                balance = balance - insurancebet
                print('Dealer does not have blackjack.'
                      +' You lose insurance bet of: '+ str(insurancebet))
        else:
            insurancechoice = 'empty'
            print('Please enter either yes or no')


class BlackjackDeck:
    '''A standard 52 card blackjack deck.
    '''
    def _build_deck(self):
        deck = []
        for value in "23456789TJQKA":
            for suite in "CDSH":
                card = value + suite
                deck.append(card)
        return deck
    
    def __init__(self):
        '''Initialize an empty deck.'''
        self.cards = self._build_deck()

    def deal(self):
        '''Removes 1 random card from deck and returns it'''
        import random
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

class BlackjackHand:
    def __init__(self):
        '''Initialize an empty player hand.'''
        self.hand = []
        self.totalvalue = 0
        self.acecount = 0

    def _value(self, card):
        '''Takes argument card and returns its integer value '''
        if card[0] in '23456789':
            return int(card[0])
        elif card[0] in 'TJQK':
            return  int(10)
        else:
            return int(11)
        
    def deal(self, deck):
        '''Appends a new card from deck to hand. This
           adds the value of new card to total value
           and adds 1 to acecount for every drawn Ace.
        '''
        self.hand.append(deck.deal())
        self.totalvalue += self._value(self.hand[-1])
        if self.hand[-1].startswith('A'):
            self.acecount +=1
        else:
            return

    def lower_ace(self):
        '''Reduces value of Ace cards to 1 by subtrating
           10 from hand value when over 21
        '''
        while self.totalvalue > 21 and self.acecount>0:
            self.totalvalue -= 10
            self.acecount -= 1
        else:
            return self.totalvalue
        
    def blackjack_check(self):
        '''Checks if hand is a true blackjack '''
        if len(self.hand) == 2 and self.totalvalue == 21:
            return True
        else:
            return False

class PlayerHand(BlackjackHand):
    '''Player's hand of cards.
    '''
    def play(self, deck):
        ''''Allows player to hit or stand while under 21'''
        self.lower_ace()
        choice = 'hit'
        while (self.totalvalue < 21 and choice == 'hit'): 
            choice = input('Would you like to hit or stand? ')
            if choice == 'hit':
                self.deal(deck)
                self.lower_ace()
                print('You are dealt a ' + self.hand[-1])
            elif choice == 'stand':
                return
            else:
                print('Invalid input')
                choice = 'hit'
                
        else:
            if self.totalvalue == 21:
                print('You have 21')
            elif self.totalvalue > 21:
                print('You Bust')
                
    def can_and_want_split(self):
        '''Offers player split if player's first two cards are of
           equal value.  Player then chooses whether want or don't
           want to split
        '''
        if self._value(self.hand[0]) == self._value(self.hand[1]):
            choice = 'null'
            while choice == 'null':
                choice = input('Would you like to split? ')
                if choice == 'yes':
                    return True
                elif choice == 'no':
                    return False
                else:
                    choice = 'null'
                    continue
        else:
            return False

class DealerHand(BlackjackHand):
    '''Dealer's hand of cards.
    '''
    def play(self, deck):
        '''Simulates dealer playing.  Dealer hits until reaches
           value of 17 or above.
        '''
        self.lower_ace()
        while self.totalvalue < 17:
            self.deal(deck)
            print('Dealer draws a ' + self.hand[-1])
            self.lower_ace()    
        else:
            if self.totalvalue > 21:
                print('Dealer Busts.')
            else:                
                return

## GAME CODE BEGINS HERE --------------------------------------------------


print('Welcome to Blackjack, by Ian Kung')
balance = 100
while balance > 0:
    
    deck = BlackjackDeck()
    playerhand = PlayerHand()
    dealerhand = DealerHand()

    bet = input('Balance: ' + str(balance) + '. Enter Bet (0 bet to quit): ')
    if str.isdigit(bet) and (int(bet) <= balance and int(bet) > 0):
        bet = int(bet)
        
        playerhand.deal(deck)
        playerhand.deal(deck)
        dealerhand.deal(deck)
        dealerhand.deal(deck)
        
        print('You have a ' + playerhand.hand[0] + ' and ' + playerhand.hand[1] + '. '
              + 'Dealer is showing ' + dealerhand.hand[0])
        insurance = False
        if dealerhand.hand[0].startswith('A'):
            insurance_play()
            insurance = True
            
##Below checks for initial blackjack for the player and dealer, round ends if either one have blackjack
        
        if insurance == False and playerhand.blackjack_check() and dealerhand.blackjack_check():
            print('Draw. Dealer has ' + str(dealerhand.hand))
            continue
        elif insurance == False and playerhand.blackjack_check():
            print('You have blackjack and win ' + str(2.5*bet))
            balance += (2.5*bet)
            continue
        elif insurance == False and dealerhand.hand[0].startswith('A') and dealerhand.blackjack_check():
            print('Dealer has blackjack and you lose ' + str(bet))
            balance -= bet
            continue
        
##The code in the below ELSE statment handles the case when player wishes to split
        
        elif playerhand.blackjack_check()==False and dealerhand.blackjack_check() == False:
            if playerhand.can_and_want_split():
                playerhand1 = PlayerHand()
                playerhand2 = PlayerHand()
                playerhand1.hand.append(playerhand.hand[0])
                playerhand2.hand.append(playerhand.hand[1])
                
                if playerhand1.hand[0].startswith('A'):
                    playerhand1.acecount = 1
                    playerhand2.acecount = 1
                playerhand1.deal(deck)
                playerhand2.deal(deck)
                print('Hand 1: ' + str(playerhand1.hand))
                playerhand1.play(deck)
                print('Hand 2: ' + str(playerhand2.hand))
                playerhand2.play(deck)

                if playerhand1.totalvalue <= 21 or playerhand2.totalvalue <= 21:
                    dealerhand.play(deck)
                    if player_wins(playerhand1,dealerhand) and player_wins(playerhand2,dealerhand):
                        print('You won both hands. Dealer has ' + str(dealerhand.hand))
                        balance += 2*bet
                        print('You gained: '+ str(2*bet))
                        continue 
                    elif player_wins(playerhand1,dealerhand):
                        print('You won Hand 1 but lost Hand 2. Dealer has ' + str(dealerhand.hand))
                        print('You gained: 0')
                        continue
                    elif player_wins(playerhand2,dealerhand):
                        print('You won Hand 2 but lost Hand 1. Dealer has ' + str(dealerhand.hand))
                        print('You gained: 0')
                        continue
                    elif playerhand1.totalvalue == dealerhand.totalvalue and playerhand2.totalvalue == dealerhand.totalvalue:
                        print('Both hands draw. Dealer has ' + str(dealerhand.hand))
                        continue
                    else:
                        print('Both Hands Lose. Dealer has ' + str(dealerhand.hand))
                        print('You lose: ' + str(2*bet))
                        balance -= 2*bet
                        continue
                else:
                    print('Both Hands Busted. You lose: ' + str(2*bet))
                    balance -= 2*bet
                    continue
                
##The below else statment has code for regular play without splitting

            else:
                playerhand.play(deck)
                if playerhand.totalvalue <= 21:
                    dealerhand.play(deck)
                    if dealerhand.totalvalue <= 21:
                        if player_wins(playerhand, dealerhand):
                            print('You win. Dealer Cards: ' + str(dealerhand.hand))
                            print('You receive ' + str(bet))
                            balance += bet
                        else:
                            if playerhand.totalvalue == dealerhand.totalvalue:
                                print('Draw. Dealer Cards: ' + str(dealerhand.hand))
                                continue
                            elif playerhand.totalvalue < dealerhand.totalvalue:
                                print('You lose. Dealer Cards: ' + str(dealerhand.hand))
                                print('You lose ' + str(bet))
                                balance -= bet
                    else:
                        print('You win. Dealer Cards: ' + str(dealerhand.hand))
                        print('You win ' + str(bet))
                        balance += bet
                else:
                    print('Dealer Cards: ' + str(dealerhand.hand))
                    print('You lose ' + str(bet))
                    balance -= bet
    elif bet == '0':
        print('Game Over, Final Score: ' + str(balance))
        break
    else:
        print('Invalid input. You have ' + str(balance))
        continue
else:
    print('You are out of money')
