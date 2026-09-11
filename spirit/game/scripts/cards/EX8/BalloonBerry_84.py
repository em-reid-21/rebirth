from spirit.game.data_utils import reprint, sibling_card
from spirit.game.attributes import Rarities

card = reprint(sibling_card(__file__, "../EX3/BalloonBerry_82.py"),
               collector_number=84, rarity=Rarities.Uncommon,
               set_code="EX8", key="EX8")
