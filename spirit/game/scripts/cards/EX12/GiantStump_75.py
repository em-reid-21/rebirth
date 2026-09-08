from spirit.game.data_utils import StadiumCardDef, unimplemented
from spirit.game.attributes import Rarities
from spirit.game.session.passives import Passive

class GiantStumpPassive(Passive):
    """ Each player can't have more than 3 Benched Pokémon.
When Giant Stump comes into play, each player discards Benched Pokémon and any cards attached to them until he or she has 3 Benched Pokémon. (You discard your Pokémon first.) """

    def bench_capacity(self, player_id, carrier):
        # Stadium: carrier -> activeStadium -> playmat
        playmat = carrier.parent.parent if carrier.parent else None
        if playmat is None:
            return None
        return 3

card = StadiumCardDef(
    guid="3fd75fd0-ef97-5631-9870-02e27e2a7fb2",
    key="EX12",
    name="com.direwolfdigital.cake.data.archetypes.trainer.GiantStump.Name",
    display_name="Giant Stump",
    searchable_by=["Giant Stump","Stadium","GiantStump"],
    subtypes=["Stadium"],
    collector_number=75,
    set_code="EX12",
    rarity=Rarities.Uncommon,
    passive=GiantStumpPassive()
)
