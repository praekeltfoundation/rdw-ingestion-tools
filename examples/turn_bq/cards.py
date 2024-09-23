from api.turn_bq import pyTurnBQ

cards = pyTurnBQ.cards.get_cards()

print(cards.head(5))
