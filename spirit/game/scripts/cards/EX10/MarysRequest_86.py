from spirit.game.data_utils import SupporterCardDef, subtypes_for
from spirit.game.attributes import Rarities
from spirit.game.card_effects.support_common import draw_attack
from spirit.game.session.effects import EffectContext

async def marys_request(ctx: EffectContext):
    """You can play only one Supporter card each turn. When you play this card,
    put it next to your Active Pokemon. When your turn ends, discard this
    card. Draw a card. If you don't have any Stage 2 Evolved Pokemon in
    play, draw 2 more cards."""
    await ctx.draw_cards(1)    
    if not any(
                subtype in { "Stage 2"}
                for pokemon in ctx.my_pokemon_in_play()
                for subtype in subtypes_for(pokemon.archetype_id)
            ):
        await ctx.draw_cards(2)

card = SupporterCardDef(
    guid="7aa632dd-492d-5b8d-ad8b-c79660e635cb",
    key="EX10",
    name="com.direwolfdigital.cake.data.archetypes.trainer.MarysRequest.Name",
    display_name="Mary's Request",
    searchable_by=["Mary's Request","Supporter","MarysRequest"],
    subtypes=["Supporter"],
    collector_number=86,
    set_code="EX10",
    rarity=Rarities.Uncommon,
    effect=marys_request
)
