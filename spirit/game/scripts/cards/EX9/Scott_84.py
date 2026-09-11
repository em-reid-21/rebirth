from spirit.game.data_utils import SupporterCardDef, unimplemented
from spirit.game.attributes import Rarities, TrainerType
from spirit.game.session.effects import AttrID, EffectContext, is_stadium_card, is_supporter_card

""" Search your deck for up to 3 cards in any combination of Supporter cards and Stadium cards, show them to your opponent, and put them into your hand. Shuffle your deck afterward. """

def eligible(card) -> bool:
    return is_supporter_card(card) or is_stadium_card(card)

async def scott_effect(ctx: EffectContext):
    cards = await ctx.search_deck(eligible, 3, prompt="Search your deck for up to 3 Supporter or Stadium cards in any combination")
    await ctx.put_in_hand(cards, reveal=True)
    await ctx.shuffle_deck()

card = SupporterCardDef(
    guid="fedad97e-c47b-551b-88bf-a60a71c50154",
    key="EX9",
    name="com.direwolfdigital.cake.data.archetypes.trainer.Scott.Name",
    display_name="Scott",
    searchable_by=["Scott","Supporter","Scott"],
    subtypes=["Supporter"],
    collector_number=84,
    set_code="EX9",
    rarity=Rarities.Uncommon,
    effect=scott_effect
)
