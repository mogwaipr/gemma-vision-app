"""TTB regulatory taxonomy and category-specific label requirements."""

GUIDELINE_MAP = {
    "4.1": {
        "section_name": "Distilled Spirits",
        "cfr_part": "27 CFR Part 5",
        "class_types": [
            "Vodka", "Grain Neutral Spirits", "Grain Spirits", "Neutral Spirits",
            "Bourbon Whisky", "Straight Bourbon Whisky", "Rye Whisky", "Straight Rye Whisky",
            "Wheat Whisky", "Straight Wheat Whisky", "Malt Whisky", "Peanut Butter Whiskey", "Straight Malt Whisky",
            "Rye Malt Whisky", "Straight Rye Malt Whisky", "Corn Whisky", "Straight Corn Whisky",
            "Tennessee Whisky", "Blended Whisky", "Canadian Whisky", "Scotch Whisky",
            "Irish Whisky", "American Single Malt Whisky", "Light Whisky", "Spirit Whisky",
            "Gin", "Distilled Gin", "London Dry Gin", "Plymouth Gin", "Flavored Gin",
            "Rum", "Puerto Rican Rum", "Jamaican Rum", "Agricultural Rum", "Flavored Rum",
            "Tequila", "Tequila Blanco", "Tequila Silver", "Tequila Joven", "Tequila Reposado",
            "Tequila Añejo", "Tequila Extra Añejo", "Mezcal", "Mezcal Joven", "Mezcal Reposado",
            "Mezcal Añejo", "Brandy", "Grape Brandy", "Pisco", "Cognac", "Armagnac",
            "Applejack", "Apple Brandy", "Fruit Brandy", "Grappa", "Pomace Brandy",
            "Flavored Brandy", "Calvados", "Kirsch", "Slivovitz", "Liqueur", "Cordial",
            "Triple Sec", "Amaretto", "Schnapps", "Coffee Liqueur", "Cream Liqueur",
            "Sambuca", "Anisette", "Ouzo", "Crème de Menthe", "Crème de Cacao",
            "Crème de Cassis", "Rock and Rye", "Flavored Vodka", "Flavored Tequila",
            "Flavored Whisky", "Prepared Cocktails", "Margarita", "Martini", "Manhattan",
            "Old Fashioned", "Daiquiri", "Distilled Spirits Specialty", "Agave Spirits",
            "Alcohol", "Whisky", "Flavored Spirits", "Specialty Spirits", "Cocktails",
            "Imitation Spirits"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content",
            "net_contents", "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["50 mL", "100 mL", "200 mL", "375 mL", "750 mL", "1 L", "1.75 L"]
    },
    "4.2": {
        "section_name": "Wine",
        "cfr_part": "27 CFR Part 4",
        "class_types": [
            "Cabernet Sauvignon", "Wine", "agricultural wine", "amber wine",
            "american champagne", "amontillado sherry", "angelico", "aperitif wine",
            "apple wine", "berry wine", "blackberry wine", "blueberry wine", "brut",
            "california champagne", "carbonated grape wine", "carbonated wine", "cava",
            "champagne", "cherry wine", "cider", "citrus wine", "cyser", "demi-sec",
            "dessert wine", "dry vermouth", "extra dry", "fino sherry", "flavored wine",
            "fortified wine", "fruit wine", "grape wine", "grapefruit wine", "honey wine",
            "imitation wine", "light wine", "madeira", "malmsey madeira", "manzanilla sherry",
            "marsala", "mead", "melomel", "muscatel", "oloroso sherry", "orange wine",
            "pedro ximénez sherry", "perry", "pink wine", "plum wine", "port", "prosecco",
            "pyment", "red wine", "retsina", "retsina wine", "rice wine", "rosé wine",
            "ruby port", "sake", "sec", "sherry", "sparkling grape wine", "sparkling wine",
            "spumante", "substandard wine", "sweet vermouth", "table wine", "tawny port",
            "tokay", "vermouth", "vintage port", "white wine", "wine specialty"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content", "net_contents",
            "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["187 mL", "375 mL", "500 mL", "750 mL", "1.5 L", "3 L"]
    },
    "4.3": {
        "section_name": "Malt Beverages (Beer)",
        "cfr_part": "27 CFR Part 7",
        "class_types": [
            "Beer", "Draft Beer", "Draught Beer", "Lager", "Pale Lager", "Pilsner",
            "Pilsen", "Light Lager", "Dark Lager", "Bock", "Doppelbock", "Eisbock",
            "Vienna Lager", "Märzen", "Oktoberfest", "Rauchbier", "Ale", "Pale Ale",
            "India Pale Ale", "IPA", "New England IPA", "Session IPA", "Imperial IPA",
            "Double IPA", "American Pale Ale", "Amber Ale", "Red Ale", "Brown Ale",
            "Blonde Ale", "Golden Ale", "Cream Ale", "Lo-Cal Ale", "Wheat Ale", "Hefeweizen",
            "Weissbier", "Dunkelweizen", "Weizenbock", "Witbier", "Saison",
            "Farmhouse Ale", "Biere de Garde", "Sour Ale", "Gose", "Berliner Weisse",
            "Lambic", "Gueuze", "Fruit Lambic", "Porter", "Robust Porter", "Baltic Porter",
            "Stout", "Dry Stout", "Irish Stout", "Milk Stout", "Oatmeal Stout",
            "Imperial Stout", "Russian Imperial Stout", "Barleywine", "Wheatwine",
            "Rye Ale", "Scotch Ale", "Wee Heavy", "Malt Liquor", "Flavored Malt Beverage",
            "FMB", "Hard Seltzer", "Hard Cider", "Hard Lemonade", "Non-Alcoholic Malt Beverage",
            "Cereal Beverage", "Malt Beverage", "Near Beer"
        ],
        "mandatory_checks": [
            "brand_name", "class_type", "alcohol_content", "net_contents",
            "company_name", "location_address", "government_warning"
        ],
        "net_content_allowed_values": ["12 fl. oz.", "16 fl. oz.", "1 Pint", "22 fl. oz."]
    }
}
