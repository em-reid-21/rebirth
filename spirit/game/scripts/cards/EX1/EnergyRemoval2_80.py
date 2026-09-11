from spirit.game.card_effects.trainers import opponent_has_energy_attached
from spirit.game.data_utils import ItemCardDef, unimplemented
from spirit.game.attributes import Rarities
from spirit.game.scripts.cards.CZ.CrushingHammer_125 import crushing_hammer
from spirit.game.session.effects import EffectContext

card = ItemCardDef(
    guid="1e441269-b8be-54c4-8d06-1123d4c5722b",
    key="EX1",
    name="com.direwolfdigital.cake.data.archetypes.trainer.EnergyRemoval2.Name",
    display_name="Energy Removal 2",
    searchable_by=["Energy Removal 2","Item","EnergyRemoval2"],
    subtypes=["Item"],
    collector_number=80,
    set_code="EX1",
    rarity=Rarities.Uncommon,
    effect=crushing_hammer,
    condition=opponent_has_energy_attached
)
