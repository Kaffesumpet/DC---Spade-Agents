# DC---Spade-Agents



Agenten genererar?/tar från en lista?/ matematiska tal
Agenten ger talen till spelaren, tio i taget
Spelaren får ge svaren på ekvationen
    Vid Rätt så får spelaren gå vidare till nästa fråga
    Vid Fel så får spelaren gissa igen 
        Vid tre fel så skippas frågan
    Vid första rätt svar får spelaren 1 poäng, andra försöket 0.5 poäng, tredje försöket 0.25

Spelaren antages vinna när spelaren har fått minst 8 poäng
Spelaren får ett "bra jobbat, nästan" om den får 6-7.9 poäng.
Spelaren får ett "du måste plugga mer" om de får lägre än 6.

---------------------------------------------------------------------------------------------------------------------------------

States:
start
generate question state
present question state
evaluate answer state
score update state
end