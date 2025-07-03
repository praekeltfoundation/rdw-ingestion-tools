from api.turn_bq import pyTurnBQ

cards = pyTurnBQ().cards.get_cards()

print(cards.collect().head(5))

cards_by_id = pyTurnBQ().cards.get_cards_by_id(card_id=817938)

print(cards_by_id.collect())
