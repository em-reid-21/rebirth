from typing import cast

from spirit.game.data_utils import PokemonCardDef, Attack, Ability, Activations
from spirit.game.attributes import AbilityTypes, AttrID, CardType, PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack
from spirit.game.models.board import CardEntity
from spirit.game.session.effects import EffectContext, EnergyEntity
from spirit.game.session.game_session import BoardState
from spirit.game.session.legal_actions import PokemonEntity
from spirit.game.session.passives import effective_bench_capacity

def holons_voltorb_attach_condition(board: BoardState, player_id: str, card: CardEntity) -> bool:
    bench = board.find_player_area(player_id, "bench")
    has_bench_space = bench is not None and len(bench.children) < \
        effective_bench_capacity(board, player_id)
    energy_attachment_available = not getattr(
        getattr(board, "turn_state", None), "energy_attached", False
    )
    return has_bench_space or energy_attachment_available

async def holons_voltorb_attach(ctx: EffectContext):
    bench = ctx.board.find_player_area(ctx.player_id, "bench")
    has_bench_space = bench is not None and len(bench.children) < \
        effective_bench_capacity(ctx.board, ctx.player_id)
    choices = []
    if has_bench_space:
        choices.append("Put Holon's Voltorb on your Bench")
        choices.append("Attach Holon's Voltorb as Energy")
    selected = await ctx.choose(
        "Choose how to play Holon's Voltorb", choices, use_panel=False
    )
    if choices[selected] == "Put Holon's Voltorb on your Bench":
        await ctx.bench_pokemon(cast(CardEntity, ctx.source))
        return
    targets = await ctx.choose_cards(
        ctx.my_pokemon_in_play(), 1, prompt="Choose a Pokemon to attach Holon's Voltorb to"
    )
    if not targets:
        return
    ctx.source.set_attribute(AttrID.CARD_TYPE, CardType.ENERGY.value)
    ctx.source.__class__ = EnergyEntity
    # Ensure that Voltorb is treated as the players energy attachment for turn
    if await ctx.attach_energy(
        cast(CardEntity, ctx.source),
        cast(PokemonEntity, targets[0]),
        counts_as_attachment=True,
    ):
        ctx.session.turn_state.energy_attached = True


card = PokemonCardDef(
    guid="658be6b1-7434-54a7-9f5c-96883adf08bd",
    key="EX11",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.HolonsVoltorb.Name",
    display_name="Holon's Voltorb",
    searchable_by=["Holon's Voltorb","Basic","HolonsVoltorb"],
    subtypes=["Basic"],
    collector_number=71,
    set_code="EX11",
    rarity=Rarities.Common,
    hp=40,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIGHTING,
    abilities=[
        Ability(
            title="Holon Energy",
            game_text="You may attach this as an Energy card from your hand to 1 of your Pokémon. While attached, this card is a Special Energy card and provides Colorless Energy.",
            ability_type=AbilityTypes.POKE_ABILITY,
            activation=Activations.ONCE_PER_TURN,
            usable_from="hand",
            effect=holons_voltorb_attach,
            condition=holons_voltorb_attach_condition,
        ),

        Attack(
            title="Thundershock",
            game_text="Flip a coin. If heads, the Defending Pokémon is now Paralyzed.",
            cost={PokemonTypes.LIGHTNING: 1},
            damage=10,
            effect=condition_attack(SpecialConditions.PARALYZED, flip=True),
        ),
    ],
    energy_provides=[[PokemonTypes.COLORLESS]]
)
