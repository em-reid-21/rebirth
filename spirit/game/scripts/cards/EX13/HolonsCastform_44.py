from spirit.game.data_utils import Ability, Activations, Attack, PokemonCardDef, def_for
from spirit.game.attributes import (
    AbilityTypes, AttrID, CardType, PokemonStage, PokemonTypes, Rarities,
)
from spirit.game.models.board import BoardState, CardEntity, EnergyEntity, PokemonEntity
from spirit.game.session.effects import EffectContext
from spirit.game.session.passives import effective_bench_capacity
from typing import cast


def _has_delta_on_card(pokemon: PokemonEntity) -> bool:
    """Check if a Pokemon has the delta symbol on its card."""
    archetype_def = def_for(pokemon.archetype_id)
    return archetype_def is not None and "Delta Species" in archetype_def.subtypes


async def delta_draw(ctx: EffectContext):
    """Draw up to the number of your in-play Delta Species Pokémon."""
    count = sum(_has_delta_on_card(pokemon) for pokemon in ctx.my_pokemon_in_play())
    await ctx.draw_cards(count)


def holons_castform_attach_condition(board: BoardState, player_id: str, card: CardEntity) -> bool:
    bench = board.find_player_area(player_id, "bench")
    has_bench_space = bench is not None and len(bench.children) < \
        effective_bench_capacity(board, player_id)
    energy_attachment_available = not getattr(
        getattr(board, "turn_state", None), "energy_attached", False
    )
    has_energy_target = any(
        board.attached_energies(pokemon)
        for pokemon in board.pokemon_in_play(player_id)
    ) and energy_attachment_available
    return has_bench_space or has_energy_target


async def holons_castform_attach(ctx: EffectContext):
    bench = ctx.board.find_player_area(ctx.player_id, "bench")
    has_bench_space = bench is not None and len(bench.children) < \
        effective_bench_capacity(ctx.board, ctx.player_id)
    eligible = [
        pokemon for pokemon in ctx.my_pokemon_in_play()
        if ctx.board.attached_energies(pokemon) and ctx.session.turn_state.energy_attached is False
    ]
    choices = []
    if has_bench_space:
        choices.append("Put Holon's Castform on your Bench")
    if eligible:
        choices.append("Attach Holon's Castform as Energy")
    selected = await ctx.choose(
        "Choose how to play Holon's Castform", choices, use_panel=False
    )
    if choices[selected] == "Put Holon's Castform on your Bench":
        await ctx.bench_pokemon(cast(CardEntity, ctx.source))
        return
    targets = await ctx.choose_cards(
        eligible, 1, prompt="Choose a Pokemon to attach Holon's Castform to"
    )
    if not targets:
        return
    energy = await ctx.choose_cards(
        ctx.board.attached_energies(targets[0]), 1,
        prompt="Choose an Energy to return to your hand",
    )
    if not energy:
        return
    returned_energy = energy[0]
    if returned_energy.archetype_id == ctx.source.archetype_id:
        returned_energy.set_attribute(AttrID.CARD_TYPE, CardType.POKEMON.value)
        returned_energy.__class__ = PokemonEntity
    await ctx.put_in_hand(energy)
    # Ensure that Holon's Castform is treated as an Energy card
    ctx.source.set_attribute(AttrID.CARD_TYPE, CardType.ENERGY.value)
    ctx.source.__class__ = EnergyEntity
    # Ensure that Castform is treated as the players energy attachment for turn
    if await ctx.attach_energy(
        cast(CardEntity, ctx.source),
        cast(PokemonEntity, targets[0]),
        counts_as_attachment=True,
    ):
        ctx.session.turn_state.energy_attached = True


card = PokemonCardDef(
    guid="37d114e0-b3c9-5452-93c4-09ba6aae18f6",
    key="EX13",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.HolonsCastform.Name",
    display_name="Holon's Castform",
    searchable_by=["Holon's Castform","Basic","HolonsCastform"],
    subtypes=["Basic"],
    collector_number=44,
    set_code="EX13",
    rarity=Rarities.Uncommon,
    hp=50,
    elements=[PokemonTypes.COLORLESS],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIGHTING,
    abilities=[
        Ability(
            title="Holon Energy",
            game_text="You may put this Pokémon onto your Bench, or attach it to 1 of your Pokémon that already has an Energy card attached to it as a Special Energy card. When you attach this card, return an Energy card attached to that Pokémon to your hand.",
            ability_type=AbilityTypes.POKE_ABILITY,
            activation=Activations.ONCE_PER_TURN,
            usable_from="hand",
            condition=holons_castform_attach_condition,
            effect=holons_castform_attach,
        ),
        Attack(
            title="Delta Draw",
            game_text="Count the number of Pokémon you have in play that has δ on its card. Draw up to that many cards.",
            cost={PokemonTypes.COLORLESS: 1},
            ability_type=AbilityTypes.NON_DAMAGING_ATTACK,
            effect=delta_draw,
        ),
    ],
    energy_provides=[
        [energy_type, energy_type]
        for energy_type in (
            PokemonTypes.GRASS, PokemonTypes.FIRE, PokemonTypes.WATER,
            PokemonTypes.LIGHTNING, PokemonTypes.PSYCHIC,
            PokemonTypes.FIGHTING, PokemonTypes.DARKNESS,
            PokemonTypes.METAL, PokemonTypes.FAIRY, PokemonTypes.DRAGON,
            PokemonTypes.COLORLESS,
        )
    ],
)
