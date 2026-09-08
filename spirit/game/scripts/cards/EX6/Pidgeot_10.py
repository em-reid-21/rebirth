from spirit.game.card_effects.support_common import _has_conditions
from spirit.game.data_utils import PokemonCardDef, Attack, Ability, Activations
from spirit.game.attributes import AbilityTypes, PokemonStage, PokemonTypes, Rarities
from spirit.game.models.board import BoardState
from spirit.game.session.effects import EffectContext
from spirit.game.session.passives import PokemonEntity

def quick_search_condition(board: BoardState, player_id: str, pokemon: PokemonEntity) -> bool:
    """This power can't be used if Pidgeot is affected by a Special Condition and only one Quick search can be used per turn."""
    return not bool(_has_conditions(pokemon))

async def quick_search_effect(ctx: EffectContext):
    """Once during your turn (before your attack), you may choose any 1 card from your deck and put it into your hand. Shuffle your deck afterward. You can't use more than 1 Quick Search Poké-Power each turn. This power can't be used if Pidgeot is affected by a Special Condition."""
    candidates = list(ctx.deck())
    if not candidates:
        return
    picks = await ctx.choose_cards(
        candidates,
        1,
        minimum=1,
        prompt="Choose a card from your deck to put into your hand.",
    )
    if picks:
        await ctx.put_in_hand(picks, reveal=False)
    await ctx.shuffle_deck()

def clutch_effect(ctx: EffectContext):
    """The Defending Pokémon can't retreat until the end of your opponent's next turn."""
    ctx.session.turn_state.retreat_blockers.append(
        lambda source, target: ctx.board.defending_pokemon
        if source == ctx.source else None
    )

card = PokemonCardDef(
    guid="31484bcd-cf88-52f8-b35a-ed7e57655185",
    key="EX6",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Pidgeot.Name",
    display_name="Pidgeot",
    searchable_by=["Pidgeot","Stage 2","Pidgeot"],
    subtypes=["Stage 2"],
    collector_number=10,
    set_code="EX6",
    rarity=Rarities.RareHolo,
    hp=100,
    elements=[PokemonTypes.COLORLESS],
    stage=PokemonStage.STAGE2,
    retreat_cost=0,
    weakness_type=PokemonTypes.LIGHTNING,
    resistance_type=PokemonTypes.FIGHTING,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Pidgeotto.Name",
    abilities=[
        Ability(
            title="Quick Search",
            ability_type=AbilityTypes.POKE_POWER,
            game_text="Once during your turn (before your attack), you may choose any 1 card from your deck and put it into your hand. Shuffle your deck afterward. You can't use more than 1 Quick Search Poké-Power each turn. This power can't be used if Pidgeot is affected by a Special Condition.",
            activation=Activations.ONCE_PER_TURN,
            shared_once_per_turn='Quick Search',
            effect=quick_search_effect,
            condition=quick_search_condition
        ),
        Attack(
            title="Clutch",
            game_text="The Defending Pokémon can't retreat until the end of your opponent's next turn.",
            cost={PokemonTypes.COLORLESS: 2},
            damage=40,
            effect=clutch_effect,
        ),
    ],
)
