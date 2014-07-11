'''
****************************************************************************
Welcome to the text-based BlackJack Game written by ehsan Kabiri Rahani. 

1-BlackJack is played in different ways; The present code followa the Casino's version in which one of the dealer's cards are 'Face Down'(Hidden) untill when the player stands
and the hidden card will be revealed when the dealer hits
2-This version allows splitting only once, therefore the splitted hands may not be splittable again
3-We have only hand1 when the player does not split and hand2 will come into play when splitting takes place

****************************************************************************

'''
import random
import os

class playHand:
     __cardValues = {'Ace':11,'King':10,'Queen':10,'Jack':10,'2':2,'3':3,'4':4,
     '5':5,'6':6,'7':7,'8':8,'9':9,'10':10}
     __suitChar={'Spade':'Spade',' Diamond':'Diamond',' Heart':'Heart','Club':'Club'} #Card suit text map
     __Hands={} #Hand draws storage dictionary

     def __init__(self,BetChips):
          self.BetChips=BetChips
     def play(self):
          self.__Hands={}
          self.__dealInitialHand()
          print 50*"-"
          print "Starting A BlackJack Hand \n"
          print "Dealer's initial Hand is: "+ self.__HandToString([self.__Hands['dealer'][0]])+'-(Face Down Card)'
          print "Your initial Hand is: "+ self.__HandToString(self.__Hands['player']['hand1'])
          print 50*"-"
             
          if self.__isSplittable() and self.BetChips>1: #Split the Hand if it is splittable
             inp=raw_input("You have pairs, do you want to Split? Y / N : ")
             if inp.upper()=='Y':
                  split=True
                  self.__splitInitialHand()
          pScores={}
          for hand in self.__Hands['player']:
               IsBlackJack= self.__isBlackJack(hand)
               if IsBlackJack:
                    print "BlackJack! for "+hand
                    self.BetChips+=2
                    pScores[hand]=22
                    continue
               print 'You bet 1 chip for '+hand
               self.BetChips-=1  #bet one chip
               print str(self.BetChips)+" chips are left" 
               print 50*"-"
               print 'Playing '+hand+' :\n'  
               bust=False
               while not bust: #Hand's Hit or Stay Loop
                    dealerScore= self.__handScore(self.__Hands['dealer'])
                    print "Dealer's hand is: "+self.__HandToString([self.__Hands['dealer'][0]])+"-(Face Down Card)"
                    playerScore= self.__handScore(self.__Hands['player'][hand])
                    print "Your hand is: "+self.__HandToString(self.__Hands['player'][hand])+", Score= "+str(playerScore)
                    inp=raw_input("Hit? : (H), Stay? : (S), Surrender? : (E) ")
                    if inp.upper()=='E':
                         return 
                    elif inp.upper()=='S':
                         break
                    elif inp.upper()=='H':
                         Hands=self.__playerHit(hand)
                         playerScore= self.__handScore(self.__Hands['player'][hand])
                    if playerScore>21:
                         print "Your hand is: "+self.__HandToString(self.__Hands['player'][hand])+", Score= "+str(playerScore)
                         print 'Bust! for '+hand
                         bust=True
               pScores[hand]=playerScore   
          
          if pScores.values()[0]<=21 or pScores.values()[len(pScores)-1]<=21:
               print 50*"-"
               print "Now Dealer is playing:\n"
               self.__dealerHit()
               dealerScore= self.__handScore(self.__Hands['dealer'])
               print "Dealer's hand is: "+self.__HandToString(self.__Hands['dealer'])+", Score= "+str(dealerScore)
               print 
               for hand in pScores:
                         if dealerScore>21 and pScores[hand]<=21:
                              print 'You won for '+hand
                              self.BetChips+=2
                         elif pScores[hand]<=21 and pScores[hand]>dealerScore:
                              print 'You won! for '+hand
                              self.BetChips+=2
                         elif pScores[hand]<=21 and pScores[hand]==dealerScore:
                              print 'Push! for '+hand
                              self.BetChips+=1
                         elif pScores[hand]<=21 and pScores[hand]<dealerScore:
                              print 'Bust! for '+hand
          print str(self.BetChips)+" chips are left"  
         
          
     def __HandToString(self,Hand):    #Returns the string format of a Hand 
          HandString=''
          Symbols=dict({'Ace':'Ace','King':'King','Queen':'Queen','Jack':'Jack'}.items()+[(str(i),str(i)) for i in range(2,11)]) #Cards character map
          first=True
          for card in Hand:
               HandString+=(not first)*'...'+'('+Symbols[card[0]]+','+self.__suitChar[card[1]]+')'
               first=False
          return HandString

     def __isBlackJack(self,player): #Check for Blackjack (Player or Dealer)
          isBlackJack= self.__cardValues[self.__Hands['player'][player][0][0]]+self.__cardValues[self.__Hands['player'][player][1][0]]==21
          isBlackJack=isBlackJack and not self.__cardValues[self.__Hands['dealer'][0][0]]+self.__cardValues[self.__Hands['dealer'][1][0]]==21
          return isBlackJack

     def __handScore(self,Hand):
         score=0
         hasAce=False
         for card in Hand:
             score+=self.__cardValues[card[0]]
             if card[0]=='Ace':
                 hasAce=True
         if hasAce and score>21:
             score-=10
         return score
           
     def __splitInitialHand(self):
         #if player splits the hand 'Hand2' key will be added
         valueList=self.__cardValues.keys()
         suitList=self.__suitChar.keys()
         hand1=[self.__Hands['player']['hand1'][0],(random.choice(valueList),random.choice(suitList))]
         hand2=[self.__Hands['player']['hand1'][1],(random.choice(valueList),random.choice(suitList))]
         self.__Hands['player']={'hand1':hand1,'hand2':hand2}
      
     def __dealerHit(self): #Dealer draws cards for dealer's hand
         hasAce=False
         valueList=self.__cardValues.keys()
         suitList=self.__suitChar.keys()
         handValue=self.__cardValues[self.__Hands['dealer'][0][0]]+self.__cardValues[self.__Hands['dealer'][1][0]]
         while handValue<17:
            newCard=(random.choice(valueList),random.choice(suitList))
            self.__Hands['dealer'].append(newCard) 
            hasAce=newCard[0]=='Ace'
            handValue+=self.__cardValues[newCard[0]]
            if hasAce and handValue>21:
                handValue-=10
         
     def __playerHit(self,hand): #Dealer draws cards for player's hand
         valueList=self.__cardValues.keys()
         suitList=self.__suitChar.keys()
         newCard=(random.choice(valueList),random.choice(suitList))
         self.__Hands['player'][hand].append(newCard) 
         
     def __isSplittable(self): #can I Split the Hand? (check for pairs)
          return self.__Hands['player']['hand1'][0][0]==self.__Hands['player']['hand1'][1][0]

     def __dealInitialHand(self):
         self.__Hands={}
         valueList=self.__cardValues.keys()
         suitList=self.__suitChar.keys()
         self.__Hands['dealer']= [(random.choice(valueList),random.choice(suitList)) for i in range(2)] #two card to start for dealer
         #if player splits the hand 'hand2' key will be added
         self.__Hands['player']={'hand1':[(random.choice(valueList),random.choice(suitList)) for i in range(2)]} #two cards to start for player

def playGame():
    os.system('cls') 
    BetChips=100
    inp='Y'
    Hand=playHand(BetChips)
    while Hand.BetChips>0 and inp.upper()=='Y':
         Hand.play()
         inp=raw_input("Play another hand? Y/N") 
    
if __name__ == '__main__':
     playGame()

