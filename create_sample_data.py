#!/usr/bin/env python3
"""
Create sample battle data for BattleThread timeline demonstration.
"""

import json
import os
import random
from datetime import datetime

def create_sample_battles():
    """Create a comprehensive sample dataset of battles."""
    battles = []
    
    # Famous historical battles with accurate dates
    historical_battles = [
        # Ancient battles
        {"name": "Battle of Marathon", "year": -490, "date": "September 490 BC"},
        {"name": "Battle of Thermopylae", "year": -480, "date": "August 480 BC"},
        {"name": "Battle of Salamis", "year": -480, "date": "September 480 BC"},
        {"name": "Battle of Plataea", "year": -479, "date": "479 BC"},
        {"name": "Battle of Gaugamela", "year": -331, "date": "1 October 331 BC"},
        {"name": "Battle of Cannae", "year": -216, "date": "2 August 216 BC"},
        {"name": "Battle of Zama", "year": -202, "date": "19 October 202 BC"},
        {"name": "Battle of Actium", "year": -31, "date": "2 September 31 BC"},
        
        # Early Medieval
        {"name": "Battle of the Teutoburg Forest", "year": 9, "date": "September 9 AD"},
        {"name": "Battle of Adrianople", "year": 378, "date": "9 August 378"},
        {"name": "Battle of Tours", "year": 732, "date": "10 October 732"},
        {"name": "Battle of Hastings", "year": 1066, "date": "14 October 1066"},
        
        # High Medieval
        {"name": "Battle of Manzikert", "year": 1071, "date": "26 August 1071"},
        {"name": "Battle of Hattin", "year": 1187, "date": "4 July 1187"},
        {"name": "Battle of Bouvines", "year": 1214, "date": "27 July 1214"},
        {"name": "Battle of Ain Jalut", "year": 1260, "date": "3 September 1260"},
        
        # Late Medieval
        {"name": "Battle of Crécy", "year": 1346, "date": "26 August 1346"},
        {"name": "Battle of Poitiers", "year": 1356, "date": "19 September 1356"},
        {"name": "Battle of Kosovo", "year": 1389, "date": "15 June 1389"},
        {"name": "Battle of Agincourt", "year": 1415, "date": "25 October 1415"},
        
        # Early Modern
        {"name": "Battle of Pavia", "year": 1525, "date": "24 February 1525"},
        {"name": "Battle of Lepanto", "year": 1571, "date": "7 October 1571"},
        {"name": "Battle of Vienna", "year": 1683, "date": "12 September 1683"},
        {"name": "Battle of Blenheim", "year": 1704, "date": "13 August 1704"},
        
        # 18th Century
        {"name": "Battle of Poltava", "year": 1709, "date": "8 July 1709"},
        {"name": "Battle of Plassey", "year": 1757, "date": "23 June 1757"},
        {"name": "Battle of Quebec", "year": 1759, "date": "13 September 1759"},
        {"name": "Battle of Bunker Hill", "year": 1775, "date": "17 June 1775"},
        {"name": "Battle of Saratoga", "year": 1777, "date": "19 September 1777"},
        {"name": "Battle of Yorktown", "year": 1781, "date": "28 September 1781"},
        
        # Napoleonic Era
        {"name": "Battle of Valmy", "year": 1792, "date": "20 September 1792"},
        {"name": "Battle of the Pyramids", "year": 1798, "date": "21 July 1798"},
        {"name": "Battle of Marengo", "year": 1800, "date": "14 June 1800"},
        {"name": "Battle of Trafalgar", "year": 1805, "date": "21 October 1805"},
        {"name": "Battle of Austerlitz", "year": 1805, "date": "2 December 1805"},
        {"name": "Battle of Jena-Auerstedt", "year": 1806, "date": "14 October 1806"},
        {"name": "Battle of Wagram", "year": 1809, "date": "5-6 July 1809"},
        {"name": "Battle of Borodino", "year": 1812, "date": "7 September 1812"},
        {"name": "Battle of Leipzig", "year": 1813, "date": "16-19 October 1813"},
        {"name": "Battle of Waterloo", "year": 1815, "date": "18 June 1815"},
        
        # 19th Century
        {"name": "Battle of the Alamo", "year": 1836, "date": "23 February 1836"},
        {"name": "Battle of Balaclava", "year": 1854, "date": "25 October 1854"},
        {"name": "Battle of Gettysburg", "year": 1863, "date": "1-3 July 1863"},
        {"name": "Battle of Königgrätz", "year": 1866, "date": "3 July 1866"},
        {"name": "Battle of Sedan", "year": 1870, "date": "1 September 1870"},
        {"name": "Battle of Little Bighorn", "year": 1876, "date": "25-26 June 1876"},
        {"name": "Battle of Isandlwana", "year": 1879, "date": "22 January 1879"},
        {"name": "Battle of Adwa", "year": 1896, "date": "1 March 1896"},
        
        # 20th Century
        {"name": "Battle of Tsushima", "year": 1905, "date": "27-28 May 1905"},
        {"name": "Battle of Tannenberg", "year": 1914, "date": "26-30 August 1914"},
        {"name": "Battle of the Marne", "year": 1914, "date": "5-12 September 1914"},
        {"name": "Battle of Gallipoli", "year": 1915, "date": "25 April 1915"},
        {"name": "Battle of Verdun", "year": 1916, "date": "21 February 1916"},
        {"name": "Battle of the Somme", "year": 1916, "date": "1 July 1916"},
        {"name": "Battle of Passchendaele", "year": 1917, "date": "31 July 1917"},
        
        # World War II
        {"name": "Battle of Poland", "year": 1939, "date": "1 September 1939"},
        {"name": "Battle of Britain", "year": 1940, "date": "10 July 1940"},
        {"name": "Battle of Moscow", "year": 1941, "date": "2 October 1941"},
        {"name": "Battle of Pearl Harbor", "year": 1941, "date": "7 December 1941"},
        {"name": "Battle of Midway", "year": 1942, "date": "4-7 June 1942"},
        {"name": "Battle of Stalingrad", "year": 1942, "date": "23 August 1942"},
        {"name": "Battle of Kursk", "year": 1943, "date": "5 July 1943"},
        {"name": "Battle of Normandy", "year": 1944, "date": "6 June 1944"},
        {"name": "Battle of the Philippine Sea", "year": 1944, "date": "19-20 June 1944"},
        {"name": "Battle of Berlin", "year": 1945, "date": "16 April 1945"},
        
        # Modern Era
        {"name": "Battle of Inchon", "year": 1950, "date": "15 September 1950"},
        {"name": "Battle of Dien Bien Phu", "year": 1954, "date": "13 March 1954"},
        {"name": "Battle of Ia Drang", "year": 1965, "date": "14 November 1965"},
        {"name": "Battle of Khe Sanh", "year": 1968, "date": "21 January 1968"},
        {"name": "Battle of 73 Easting", "year": 1991, "date": "26 February 1991"},
    ]
    
    # Convert to battle format
    for idx, battle in enumerate(historical_battles):
        year = battle["year"]
        battles.append({
            "id": f"battle_{idx}",
            "name": battle["name"],
            "date": {
                "year": year,
                "display": battle["date"],
                "sortKey": year + 10000,
                "confidence": "high",
                "era": "BC" if year < 0 else "AD",
                "original": battle["date"]
            },
            "categories": []
        })
    
    # Add some randomly generated battles to fill timeline
    regions = ["Europe", "Asia", "Africa", "Americas", "Middle East"]
    battle_types = ["Siege", "Naval Battle", "Skirmish", "Campaign", "Raid"]
    
    for century in range(-30, 21):  # 3000 BC to 2000 AD
        # Random number of battles per century (0-5)
        num_battles = random.randint(0, 5)
        
        for _ in range(num_battles):
            year = century * 100 + random.randint(0, 99)
            region = random.choice(regions)
            battle_type = random.choice(battle_types)
            
            if year < 0:
                display_year = f"{abs(year)} BC"
                era = "BC"
            else:
                display_year = str(year)
                era = "AD"
            
            battles.append({
                "id": f"generated_battle_{len(battles)}",
                "name": f"{battle_type} of {region} {display_year}",
                "date": {
                    "year": year,
                    "display": display_year,
                    "sortKey": year + 10000,
                    "confidence": "low",
                    "era": era,
                    "original": f"c. {display_year}"
                },
                "categories": [region, battle_type]
            })
    
    # Sort by date
    battles.sort(key=lambda b: b["date"]["sortKey"])
    
    return battles

def main():
    """Create and save the sample dataset."""
    battles = create_sample_battles()
    
    # Create dataset structure
    dataset = {
        "battles": battles,
        "metadata": {
            "total": len(battles),
            "dateRange": {
                "earliest": battles[0]["date"]["year"] if battles else None,
                "latest": battles[-1]["date"]["year"] if battles else None
            },
            "generated": datetime.now().isoformat()
        }
    }
    
    # Save dataset
    os.makedirs("battlethread/data", exist_ok=True)
    with open("battlethread/data/battles_timeline.json", "w") as f:
        json.dump(dataset, f, indent=2)
    
    print(f"Created sample dataset with {len(battles)} battles")
    print(f"Date range: {dataset['metadata']['dateRange']['earliest']} to {dataset['metadata']['dateRange']['latest']}")

if __name__ == "__main__":
    main()