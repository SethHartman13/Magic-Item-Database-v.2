# Magic Item JSON formats
<br>

## Potion

```json
{
    "name": "name",
    "item_type": "potion",
    "rarity": "rarity",
    "homebrew": false,
    "details": "Item details"
}
```
<br>

## Spell Scroll

```json
{
    "name": "name",
    "item_type": "scroll",
    "rarity": "rarity",
    "level": 0,
    "spells": [""],
    "homebrew": false,
    "details": "Item details"
}
```

## Every other type:

```json
{
    "name": "name",
    "item_type": "type",
    "rarity": "rarity",
    "attunement": false,
    "attunement_type": "None",
    "class": "None",
    "race": "None",
    "other": "None",
    "variations": [""],
    "homebrew": false,
    "details": "Item details"
}
```
