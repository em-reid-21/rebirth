from spirit.game.card_effects.support_common import shuffle_hand_into_deck_draw
from spirit.game.data_utils import SupporterCardDef, unimplemented
from spirit.game.attributes import Rarities
from spirit.game.session.effects import EffectContext

def rockets_admin_effect(ctx: EffectContext):
    """Each player shuffles their hand into their deck and draws cards equal to the number of prizes they have."""
    player_prizes = len(ctx.board.find_player_area(ctx.player_id, "prizePile").children)
    opponent_prizes = len(ctx.board.find_player_area(ctx.opponent_id, "prizePile").children)
    return shuffle_hand_into_deck_draw(n=player_prizes, opponent_n=opponent_prizes)(ctx)

card = SupporterCardDef(
    guid="c3c090b0-c699-54e5-ab59-60890a9c6fd6",
    key="EX7",
    name="com.direwolfdigital.cake.data.archetypes.trainer.RocketsAdmin.Name",
    display_name="Rocket's Admin.",
    searchable_by=["Rocket's Admin.","Supporter","RocketsAdmin"],
    subtypes=["Supporter"],
    collector_number=86,
    set_code="EX7",
    rarity=Rarities.Uncommon,
    effect=rockets_admin_effect
)
