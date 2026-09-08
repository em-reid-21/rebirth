from spirit.game.card_effects.support_common import _has_conditions
from spirit.game.card_effects.trainers import is_basic_energy_card, is_grass_energy_card
from spirit.game.data_utils import PokemonCardDef, Attack, Ability, Activations
from spirit.game.attributes import AbilityTypes, PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.models.board import BoardState, PokemonEntity
from spirit.game.session.effects import EffectContext
from typing import cast


def nurture_and_heal_condition(board: BoardState, player_id: str, pokemon: PokemonEntity):
    """This power can't be used if Meganium ex is affected by a Special Condition."""
    hand = board.find_player_area(player_id, "hand")
    return bool(hand) and any(is_basic_energy_card(c) and is_grass_energy_card(c) for c in hand.children) and not _has_conditions(pokemon)

async def nurture_and_heal_effect(ctx: EffectContext):
    """Once during your turn (before your attack), you may attach a Grass Energy card from your hand to 1 of your Pokémon. If you do, remove 1 damage counter from that Pokémon. This power can't be used if Meganium ex is affected by a Special Condition."""
    grass_energy_cards = [
        c for c in ctx.hand() if is_basic_energy_card(c) and is_grass_energy_card(c)
    ]
    if not grass_energy_cards:
        return
    candidates = ctx.my_pokemon_in_play()
    if not candidates:
        return
    target = await ctx.choose_cards(
        candidates, 1, minimum=0,
        prompt="Choose 1 of your Pokémon.",
    )
    for target in target:
        energies = [c for c in grass_energy_cards]
        if not energies:
            break
        picks = await ctx.choose_cards(
            energies, 1,
            prompt="Choose a Basic Energy to attach.",
        )
        if picks:
            await ctx.attach_energy(picks[0], cast(PokemonEntity, target))
            await ctx.heal(10, cast(PokemonEntity, target))

async def power_poison_effect(ctx: EffectContext):
    """Discard 1 Energy attached to Meganium ex. The Defending Pokémon is now Poisoned."""
    await ctx.deal_damage()
    if not ctx.board.attached_energies(ctx.source):
        return
    energy_to_discard = await ctx.choose_cards(
        ctx.board.attached_energies(ctx.source), 1, prompt="Choose an Energy to discard"
    )
    if not energy_to_discard:
        return
    await ctx.discard_cards(energy_to_discard)
    await ctx.apply_special_condition(ctx.defender, SpecialConditions.POISONED)

card = PokemonCardDef(
    guid="660886fa-1ebf-5f39-b642-c139200a7ad6",
    key="EX10",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Meganiumex.Name",
    display_name="Meganium ex",
    searchable_by=["Meganium ex","Stage 2","ex","Meganiumex"],
    subtypes=["Stage 2","ex"],
    collector_number=106,
    set_code="EX10",
    rarity=Rarities.RareHoloEX,
    hp=150,
    elements=[PokemonTypes.GRASS],
    stage=PokemonStage.STAGE2,
    retreat_cost=2,
    weakness_type=PokemonTypes.GRASS,
    resistance_type=PokemonTypes.WATER,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Bayleef.Name",
    abilities=[
        Ability(
            title="Nurture and Heal",
            ability_type=AbilityTypes.POKE_POWER,
            game_text="Once during your turn (before your attack), you may attach a Grass Energy card from your hand to 1 of your Pokémon. If you do, remove 1 damage counter from that Pokémon. This power can't be used if Meganium ex is affected by a Special Condition.",
            activation=Activations.ONCE_PER_TURN,
            effect=nurture_and_heal_effect,
            condition=nurture_and_heal_condition,
        ),
        Attack(
            title="Razor Leaf",
            cost={PokemonTypes.COLORLESS: 3},
            damage=50,
        ),
        Attack(
            title="Power Poison",
            game_text="Discard 1 Energy attached to Meganium ex. The Defending Pokémon is now Poisoned.",
            cost={PokemonTypes.GRASS: 2, PokemonTypes.COLORLESS: 3},
            damage=90,
            effect=power_poison_effect,
        ),
    ],
)
