# Magic Item JSON formats
<br>

## Potion

```json
{
    "$schema": "https://json-schema.org/draft-07/schema",
    "$id": "https://raw.githubusercontent.com/SethHartman13/Magic-Item-Database-v.2/master/storage_data/potion_schema.json",
    "type": "object",
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
    "$schema": "https://json-schema.org/draft-07/schema",
    "$id": "https://raw.githubusercontent.com/SethHartman13/Magic-Item-Database-v.2/master/storage_data/scroll_schema.json",
    "type": "object",
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
    "$schema": "https://json-schema.org/draft-07/schema",
    "$id": "https://raw.githubusercontent.com/SethHartman13/Magic-Item-Database-v.2/master/storage_data/general_schema.json",
    "type": "object",
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
