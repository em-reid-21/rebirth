from spirit.game.data_utils import PokemonToolCardDef
from spirit.game.attributes import Rarities
from spirit.game.card_effects.trainers import Passive, carrier_pokemon

"""The Pokémon Balloon Berry is attached to has a Retreat Cost of 0. When the Pokémon Balloon Berry is attached to retreats, discard Balloon Berry."""

class BalloonBerryPassive(Passive):
    """The holder's retreat cost is 0 with Balloon Berry attached, and Balloon Berry is
    discarded when the holder retreats."""

    def modify_retreat_cost(self, cost, pokemon, carrier, board):
        if carrier_pokemon(carrier) is pokemon:
            return 0
        return cost

    def on_retreat(self, pokemon, carrier, board):
        return carrier_pokemon(carrier) is pokemon

card = PokemonToolCardDef(
    passive=BalloonBerryPassive(),
    guid="aa5139df-9e98-52e2-9333-93f2df26d571",
    key="EX3",
    name="com.direwolfdigital.cake.data.archetypes.trainer.BalloonBerry.Name",
    display_name="Balloon Berry",
    searchable_by=["Balloon Berry","Pokémon Tool","Tool","BalloonBerry"],
    subtypes=["Pokémon Tool","Tool"],
    collector_number=82,
    set_code="EX3",
    rarity=Rarities.Uncommon,
)
