"""
Sample Data for Demand-Supply Matching Prototype
Represents real-world logistics, e-commerce, and emergency resource distribution scenarios.
"""

DEMAND_RECORDS = [
    {
        "id": "D101",
        "client": "Metro General Hospital",
        "category": "Medical Supplies",
        "quantity": 40,
        "max_price": 150.0,
        "urgency": 9,  # Scale 1-10
        "location": "North_Hub",
        "tags": ["sterile", "cold_chain", "express", "certified"]
    },
    {
        "id": "D102",
        "client": "Apex Construction Corp",
        "category": "Industrial Steel",
        "quantity": 120,
        "max_price": 95.0,
        "urgency": 4,
        "location": "East_District",
        "tags": ["heavy_load", "bulk", "standard_ground"]
    },
    {
        "id": "D103",
        "client": "GreenLeaf Organic Grocers",
        "category": "Perishable Foods",
        "quantity": 60,
        "max_price": 45.0,
        "urgency": 8,
        "location": "Central_Square",
        "tags": ["cold_chain", "organic", "express", "perishable"]
    },
    {
        "id": "D104",
        "client": "Silicon Systems Labs",
        "category": "Semiconductors",
        "quantity": 25,
        "max_price": 280.0,
        "urgency": 7,
        "location": "Tech_Park",
        "tags": ["fragile", "anti_static", "express", "insured"]
    },
    {
        "id": "D105",
        "client": "City Relief NGO",
        "category": "Emergency Rations",
        "quantity": 100,
        "max_price": 30.0,
        "urgency": 10,
        "location": "South_Port",
        "tags": ["humanitarian", "express", "high_volume"]
    },
    {
        "id": "D106",
        "client": "Nova Energy Utilities",
        "category": "Solar Components",
        "quantity": 50,
        "max_price": 120.0,
        "urgency": 5,
        "location": "West_End",
        "tags": ["fragile", "heavy_load", "certified"]
    }
]

SUPPLY_RECORDS = [
    {
        "id": "S201",
        "supplier": "BioPharm Global Logistics",
        "category": "Medical Supplies",
        "available_qty": 80,
        "unit_price": 135.0,
        "urgency_rating": 9,
        "location": "Airport_Logistics_Center",
        "tags": ["sterile", "cold_chain", "express", "certified", "insured"]
    },
    {
        "id": "S202",
        "supplier": "Titan Heavy Foundries",
        "category": "Industrial Steel",
        "available_qty": 200,
        "unit_price": 88.0,
        "urgency_rating": 3,
        "location": "Industrial_Zone_A",
        "tags": ["heavy_load", "bulk", "standard_ground"]
    },
    {
        "id": "S203",
        "supplier": "FarmFresh Coldways",
        "category": "Perishable Foods",
        "available_qty": 90,
        "unit_price": 40.0,
        "urgency_rating": 8,
        "location": "Rural_Depot",
        "tags": ["cold_chain", "organic", "express", "perishable"]
    },
    {
        "id": "S204",
        "supplier": "Quantum Microtech Ltd",
        "category": "Semiconductors",
        "available_qty": 50,
        "unit_price": 260.0,
        "urgency_rating": 7,
        "location": "Tech_Park",
        "tags": ["fragile", "anti_static", "express", "cleanroom", "insured"]
    },
    {
        "id": "S205",
        "supplier": "Global Feed & Aid Services",
        "category": "Emergency Rations",
        "available_qty": 150,
        "unit_price": 25.0,
        "urgency_rating": 10,
        "location": "South_Port",
        "tags": ["humanitarian", "express", "high_volume"]
    },
    {
        "id": "S206",
        "supplier": "Helios Clean Power",
        "category": "Solar Components",
        "available_qty": 70,
        "unit_price": 110.0,
        "urgency_rating": 6,
        "location": "West_End",
        "tags": ["fragile", "heavy_load", "certified"]
    }
]

# Regional Logistics Network Map (Nodes and weighted edges)
# Nodes: North_Hub, East_District, Central_Square, Tech_Park, South_Port, West_End,
#        Airport_Logistics_Center, Industrial_Zone_A, Rural_Depot, Harbor_Terminal
LOGISTICS_NODES = [
    "North_Hub",
    "East_District",
    "Central_Square",
    "Tech_Park",
    "South_Port",
    "West_End",
    "Airport_Logistics_Center",
    "Industrial_Zone_A",
    "Rural_Depot",
    "Harbor_Terminal"
]

# Undirected/Bidirectional transport links with (u, v, transport_cost_usd, travel_time_hours)
LOGISTICS_EDGES = [
    ("North_Hub", "Airport_Logistics_Center", 15, 0.5),
    ("North_Hub", "Central_Square", 22, 1.0),
    ("North_Hub", "Tech_Park", 35, 1.5),
    ("Central_Square", "Tech_Park", 18, 0.8),
    ("Central_Square", "East_District", 25, 1.2),
    ("Central_Square", "West_End", 20, 0.9),
    ("Central_Square", "South_Port", 30, 1.4),
    ("East_District", "Industrial_Zone_A", 12, 0.6),
    ("Industrial_Zone_A", "South_Port", 28, 1.3),
    ("South_Port", "Harbor_Terminal", 10, 0.4),
    ("West_End", "Rural_Depot", 24, 1.1),
    ("Rural_Depot", "Central_Square", 26, 1.2),
    ("Airport_Logistics_Center", "Tech_Park", 20, 0.9),
    ("Airport_Logistics_Center", "Central_Square", 16, 0.7)
]

# Directed transport links with discounts/incentives (can have negative weights representing green delivery subsidies or route rebate credits)
DIRECTED_LOGISTICS_WITH_DISCOUNTS = [
    ("Airport_Logistics_Center", "North_Hub", 15),
    ("North_Hub", "Central_Square", 22),
    ("Airport_Logistics_Center", "Tech_Park", 20),
    ("Tech_Park", "Central_Square", 18),
    ("Central_Square", "West_End", 20),
    ("West_End", "Rural_Depot", 24),
    ("Central_Square", "East_District", 25),
    ("East_District", "Industrial_Zone_A", 12),
    ("Industrial_Zone_A", "South_Port", 28),
    ("Central_Square", "South_Port", 30),
    ("South_Port", "Harbor_Terminal", 10),
    # Green logistics subsidies / promotional backhaul route discount (-8 and -5)
    ("Airport_Logistics_Center", "Central_Square", -5),
    ("Central_Square", "Rural_Depot", -8),
    ("Tech_Park", "West_End", 14),
]
