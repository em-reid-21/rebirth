from spirit.game.card_effects.trainers import Passive
from spirit.game.attributes import AttrID, PokemonTypes
from spirit.game.data_utils import StadiumCardDef
from spirit.game.attributes import Rarities

"""Each Special Energy card that provides 2 or more Energy (both yours and your opponent's) now provides only 1 [C] Energy. This isn't affected by any Poké-Powers or Poké-Bodies."""
    
class CrystalBeachPassive(Passive):
    """Special Energy providing 2+ Energy (either side) provides only 1 [C]."""
    def modify_energy_provided(self, options, energy, holder, board):
        if not energy.get_attribute(AttrID.IS_SPECIAL_ENERGY):
            return options
        if any(len(option) >= 2 for option in options):
            return [[PokemonTypes.COLORLESS.value]]
        return options

card = StadiumCardDef(
    passive=CrystalBeachPassive(),
    guid="c0f1f75e-b36f-5dfa-ba42-791f4f99283e",
    key="EX14",
    name="com.direwolfdigital.cake.data.archetypes.trainer.CrystalBeach.Name",
    display_name="Crystal Beach",
    searchable_by=["Crystal Beach","Stadium","CrystalBeach"],
    subtypes=["Stadium"],
    collector_number=75,
    set_code="EX14",
    rarity=Rarities.Uncommon,
)
