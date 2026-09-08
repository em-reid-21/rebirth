from spirit.game.data_utils import PokemonCardDef, Attack, def_for, is_pokemon_ex
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities
from spirit.game.card_effects.trainers import is_basic_energy_card
from spirit.game.models.board import PokemonEntity
from spirit.game.session.effects import CLIENT_POKEMON_TYPE_NAMES, EffectContext
from spirit.game.session.legal_actions import attack_cost_satisfied
from typing import Dict, List, cast

def pokemon_types_to_str(types: Dict[PokemonTypes, int]) -> Dict[str, int]:
    return {
        CLIENT_POKEMON_TYPE_NAMES[pokemon_type]: value
        for pokemon_type, value in types.items()
    }

def get_valid_attacks(ctx: EffectContext) -> List[Attack]:
    defender = ctx.defender
    if defender is None:
        return []

    definition = def_for(defender.archetype_id)
    attacks =[
        attack for attack in getattr(definition, "abilities", [])
        if isinstance(attack, Attack) and attack_cost_satisfied(
            pokemon_types_to_str(attack.cost),
            ctx.attached_energies(cast(PokemonEntity, ctx.source)),
            ctx.board,
        )
    ]
    return attacks

async def copy_attack_effect(ctx: EffectContext):
    """Choose 1 of the Defending Pokémon's attacks. Copy copies that attack. This attack does nothing if Mew doesn't have the Energy necessary to use that attack. (You must still do anything else required for that attack.) Mew performs that attack."""
    defender = ctx.defender
    attacks = get_valid_attacks(ctx)
    if not attacks:
        return

    picked = await ctx.choose_attack_to_copy(
        [(defender, attack) for attack in attacks],
        "Choose an attack to copy",
    )
    if picked is None:
        return

    await ctx.use_attack(picked[1])

async def extra_draw_effect(ctx: EffectContext):
    """If your opponent has any Pokémon-ex in play, search your deck for up to 2 basic Energy cards and attach them to Mew. Shuffle your deck afterward."""
    opponents_pokemon = ctx.opponent_pokemon_in_play()
    if not any(is_pokemon_ex(pokemon.archetype_id) for pokemon in opponents_pokemon):
        return

    energy, energy2 = await ctx.search_deck_groups(
        [
            (is_basic_energy_card, 1, "Choose a Basic Energy card to attach to Mew."),
            (is_basic_energy_card, 1, "Choose another Basic Energy card to attach to Mew."),
        ],
        prompt="Search your deck for up to 2 basic Energy cards and attach them to Mew.",
    )
    for energy in [energy[0], energy2[0]]:
        await ctx.attach_energy(energy, cast(PokemonEntity, ctx.source))
    await ctx.shuffle_deck()

card = PokemonCardDef(
    guid="be3e8e6c-449a-52b6-a42b-d93ceb684037",
    key="POP5",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Mew.Name",
    display_name="Mew δ",
    searchable_by=["Mew δ","Basic","Mew"],
    subtypes=["Basic"],
    collector_number=3,
    set_code="POP5",
    rarity=Rarities.Rare,
    hp=60,
    elements=[PokemonTypes.FIRE],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.PSYCHIC,
    abilities=[
        Attack(
            title="Copy",
            game_text="Choose 1 of the Defending Pokémon's attacks. Copy copies that attack. This attack does nothing if Mew doesn't have the Energy necessary to use that attack. (You must still do anything else required for that attack.) Mew performs that attack.",
            cost={PokemonTypes.COLORLESS: 1},
            effect=copy_attack_effect,
        ),
        Attack(
            title="Extra Draw",
            game_text="If your opponent has any Pokémon-ex in play, search your deck for up to 2 basic Energy cards and attach them to Mew. Shuffle your deck afterward.",
            cost={PokemonTypes.FIRE: 1},
            effect=extra_draw_effect,
        ),
    ],
)
