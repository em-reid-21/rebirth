from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities, SpecialConditions
from spirit.game.card_effects.attacks_common import condition_attack

card = PokemonCardDef(
    guid="fbecd163-0231-5de9-83a6-533d1ba41fe7",
    key="EX10",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Bayleef.Name",
    display_name="Bayleef",
    searchable_by=["Bayleef","Stage 1","Bayleef"],
    subtypes=["Stage 1"],
    collector_number=35,
    set_code="EX10",
    rarity=Rarities.Uncommon,
    hp=70,
    elements=[PokemonTypes.GRASS],
    stage=PokemonStage.STAGE1,
    retreat_cost=1,
    weakness_type=PokemonTypes.FIRE,
    resistance_type=PokemonTypes.WATER,
    evolves_from="com.direwolfdigital.cake.data.archetypes.pokemon.Chikorita.Name",
    abilities=[
        Attack(
            title="Soothing Scent",
            game_text="The Defending Pokémon is now Asleep.",
            cost={PokemonTypes.COLORLESS: 1},
            damage=10,
            effect=condition_attack(SpecialConditions.ASLEEP),
        ),
        Attack(
            title="Razor Leaf",
            cost={PokemonTypes.GRASS: 2, PokemonTypes.COLORLESS: 1},
            damage=50,
        ),
    ],
)
