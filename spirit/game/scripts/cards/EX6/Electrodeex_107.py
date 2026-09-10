from typing import cast

from spirit.game.card_effects.support_common import _has_conditions, distribute_energy
from spirit.game.card_effects.trainers import is_energy_card
from spirit.game.data_utils import PokemonCardDef, Attack, Ability, Activations, is_pokemon_ex
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.models.board import BoardState, PokemonEntity
from spirit.game.session.effects import EffectContext

def extra_energy_bomb_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    """This power can't be used if Electrode ex is affected by a Special Condition. """
    discard = board.find_player_area(player_id, "discard")
    eligible_pokemon = [p for p in board.pokemon_in_play(player_id) if not is_pokemon_ex(p.archetype_id)]
    return bool(discard) and any(is_energy_card(c) for c in discard.children) and not _has_conditions(pokemon) and bool(eligible_pokemon)

async def extra_energy_bomb(ctx: EffectContext):
    """Once during your turn (before your attack), you may discard Electrode ex and all the cards attached to it (this counts as Knocking Out Electrode ex). 
    If you do, search your discard pile for 5 Energy cards and attach them to any of your Pokémon (excluding Pokémon-ex) in any way you like."""
    energies = [c for c in ctx.discard_pile() if is_energy_card(c)]
    eligible_pokemon = [p for p in ctx.my_pokemon_in_play() if not is_pokemon_ex(p.archetype_id)]
    if energies:
        picks = await ctx.choose_cards(
            energies, min(5, len(energies)), minimum=0,
            prompt="Choose up to 5 Energy cards to attach.",
        )
        if picks:
            await distribute_energy(ctx, picks, eligible_pokemon)
    await ctx.knock_out(cast(PokemonEntity, ctx.source))

async def crash_and_burn(ctx: EffectContext):
    """ You may discard as many Energy as you like attached to your Pokémon in play. If you do, this attack does 30 damage plus 20 more damage for each Energy you discarded. """
    energies = [
        energy
        for pokemon in ctx.my_pokemon_in_play()
        for energy in ctx.attached_energies(pokemon)
    ]
    discarded = []
    if energies:
        discarded = await ctx.choose_cards(
            energies,
            len(energies),
            minimum=0,
            prompt="Choose Energy to discard for Crush and Burn.",
        )
        if discarded:
            await ctx.discard_cards(discarded)
    await ctx.deal_damage(30 + 20 * len(discarded))

card = PokemonCardDef(
    guid="606e6205-9bb1-5875-92d3-2b83e7837d44",
    key="EX6",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Electrodeex.Name",
    display_name="Electrode ex",
    searchable_by=["Electrode ex","Stage 1","ex","Electrodeex"],
    subtypes=["Stage 1","ex"],
    collector_number=107,
    set_code="EX6",
    rarity=Rarities.RareHoloEX,
    hp=90,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.STAGE1,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIGHTING,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Voltorb.Name",
    abilities=[
        Ability(
            title="Extra Energy Bomb",
            game_text="Once during your turn (before your attack), you may discard Electrode ex and all the cards attached to it (this counts as Knocking Out Electrode ex). If you do, search your discard pile for 5 Energy cards and attach them to any of your Pokémon (excluding Pokémon-ex) in any way you like. This power can't be used if Electrode ex is affected by a Special Condition.",
            activation=Activations.ONCE_PER_TURN,
            effect=extra_energy_bomb,
            condition=extra_energy_bomb_condition,
        ),
        Attack(
            title="Crush and Burn",
            game_text="You may discard as many Energy as you like attached to your Pokémon in play. If you do, this attack does 30 damage plus 20 more damage for each Energy you discarded.",
            cost={PokemonTypes.LIGHTNING: 1, PokemonTypes.COLORLESS: 1},
            damage=30,
            damage_operator="+",
            effect=crash_and_burn,
        ),
    ],
)
