from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack

card = PokemonCardDef(
    guid="ddcc2e66-2e67-5d50-ab4b-1589f484431a",
    key="EX15",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Bayleef.Name",
    display_name="Bayleef δ",
    searchable_by=["Bayleef δ","Stage 1","Bayleef"],
    subtypes=["Stage 1", "Delta Species"],
    collector_number=26,
    set_code="EX15",
    rarity=Rarities.Uncommon,
    hp=70,
    elements=[PokemonTypes.FIGHTING],
    stage=PokemonStage.STAGE1,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIRE,
    resistance_type=PokemonTypes.WATER,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Chikorita.Name",
    abilities=[
        Attack(
            title="Poisonpowder",
            game_text="The Defending Pokémon is now Poisoned.",
            cost={PokemonTypes.FIGHTING: 1, PokemonTypes.COLORLESS: 1},
            damage=20,
            effect=condition_attack(SpecialConditions.POISONED),
        ),
    ],
)
