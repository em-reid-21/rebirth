from spirit.game.data_utils import PokemonCardDef, Attack
from spirit.game.attributes import PokemonStage, PokemonTypes, Rarities

card = PokemonCardDef(
    guid="fd8243dd-45f3-5689-bf4e-6300cfacafc3",
    key="EX13",
    name="com.direwolfdigital.cake.data.archetypes.pokemon.Pidgey.Name",
    display_name="Pidgey δ",
    searchable_by=["Pidgey δ","Basic","Pidgey"],
    subtypes=["Basic", "Delta Species"],
    collector_number=77,
    set_code="EX13",
    rarity=Rarities.Common,
    hp=40,
    elements=[PokemonTypes.LIGHTNING],
    stage=PokemonStage.BASIC,
    retreat_cost=1,
    weakness_type=PokemonTypes.LIGHTNING,
    resistance_type=PokemonTypes.FIGHTING,
    abilities=[
        Attack(
            title="Wing Attack",
            cost={PokemonTypes.COLORLESS: 1},
            damage=10,
        ),
    ],
)
