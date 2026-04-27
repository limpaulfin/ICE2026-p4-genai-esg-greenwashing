"""Configuration for building real ESG corpus from GreenClaims dataset."""

CONFIRMED_KEYWORDS = [
    "fine", "lawsuit", "sued", "penalty", "settlement", "banned",
    "class action", "court", "ruling", "charged", "violation",
    "FTC", "SEC", "ASA", "ACCC", "regulat"
]

SECTOR_MAP = {
    "Ryanair": "Aviation", "AirFrance": "Aviation", "Lufthansa": "Aviation",
    "Delta": "Aviation", "Etihad": "Aviation", "Ethiad": "Aviation",
    "Shell": "Energy", "Equinor": "Energy", "TotalEnergies": "Energy",
    "BP": "Energy", "Chevron": "Energy",
    "H&M": "Fashion/Retail", "Zara": "Fashion/Retail", "Asos": "Fashion/Retail",
    "Boohoo": "Fashion/Retail", "Shein": "Fashion/Retail", "Primark": "Fashion/Retail",
    "Amazon": "Technology/Retail", "Apple": "Technology",
    "Adidas": "Consumer Goods", "Ikea": "Consumer Goods", "Innocent": "Consumer Goods",
    "Oatly": "Consumer Goods", "Nestle": "Consumer Goods", "P&G": "Consumer Goods",
    "Brewdog": "Consumer Goods", "Keurig": "Consumer Goods",
    "HSBC": "Financial Services", "DBS": "Financial Services",
    "Volkswagen": "Automotive", "BMW": "Automotive", "Toyota": "Automotive",
    "KPN": "Telecommunications", "Coca-Cola": "Consumer Goods",
    "Unilever": "Consumer Goods", "Samsung": "Electronics",
}

COUNTRY_MAP = {
    "Ryanair": "Ireland", "AirFrance": "France", "Lufthansa": "Germany",
    "Delta": "USA", "Etihad": "UAE", "Ethiad": "UAE",
    "Shell": "Netherlands", "Equinor": "Norway", "TotalEnergies": "France",
    "H&M": "Sweden", "Zara": "Spain", "Asos": "UK", "Boohoo": "UK",
    "Shein": "China", "Primark": "Ireland",
    "Amazon": "USA", "Apple": "USA",
    "Adidas": "Germany", "Ikea": "Sweden", "Innocent": "UK",
    "Oatly": "Sweden", "Nestle": "Switzerland", "P&G": "USA",
    "Brewdog": "UK", "Keurig": "Canada", "DBS": "Singapore",
    "HSBC": "UK", "BMW": "Germany", "Toyota": "Japan",
    "KPN": "Netherlands", "Coca-Cola": "USA", "Unilever": "UK",
    "Volkswagen": "Germany", "Samsung": "South Korea",
}

SIN_KEYWORDS = {
    "sin_vagueness": ["vague", "broad", "unclear", "ambiguous", "unsubstantiated"],
    "sin_no_proof": ["no proof", "no evidence", "unverified", "not substantiated"],
    "sin_fibbing": ["false", "misleading", "incorrect", "fabricat", "lie"],
    "sin_hidden_tradeoff": ["offset", "trade-off", "while", "but", "despite"],
    "ext_selective": ["cherry", "selective", "omit", "ignore", "hide"],
    "ext_aspirational": ["pledge", "commit", "promise", "target", "net-zero"],
}
