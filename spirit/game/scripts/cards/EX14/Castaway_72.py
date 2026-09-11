from spirit.game.card_effects.trainers import is_basic_energy_card
from spirit.game.data_utils import SupporterCardDef
from spirit.game.session.effects import EffectContext, is_tool_card
from spirit.game.attributes import Rarities
from spirit.game.attributes import Rarities
from spirit.game.session.effects import AttrID, TrainerType
from spirit.game.session.effects import is_supporter_card

    
async def castaway_effect(ctx: EffectContext):
    supporter, tool, basic_energy = await ctx.search_deck_groups(
        [
            (is_supporter_card, 1, "Supporter card"),
            (is_tool_card, 1, "Tool card"),
            (is_basic_energy_card, 1, "Basic Energy card"),
        ],
        prompt="Choose a Supporter, a Tool card, and a Basic Energy card",
    )
    await ctx.put_in_hand(supporter + tool + basic_energy, reveal=True)
    await ctx.shuffle_deck()

card = SupporterCardDef(
    guid="e13d3738-9e26-5020-810f-a901b29d6c2b",
    key="EX14",
    name="com.direwolfdigital.cake.data.archetypes.trainer.Castaway.Name",
    display_name="Castaway",
    searchable_by=["Castaway","Supporter","Castaway"],
    subtypes=["Supporter"],
    collector_number=72,
    set_code="EX14",
    rarity=Rarities.Uncommon,
    effect=castaway_effect
)
