import csv
import random

# 200 unique first names
first_names = [
    "John", "Jane", "Michael", "Michelle", "Chris", "Christina", "David", "Danielle", "James", "Jennifer", "William", "Sophia",
    "Oliver", "Emma", "Benjamin", "Isabella", "Lucas", "Ava", "Mason", "Mia", "Ethan", "Amelia", "Alexander", "Harper", "Henry", 
    "Ella", "Sebastian", "Elizabeth", "Jack", "Sofia", "Owen", "Avery", "Elijah", "Scarlett", "Liam", "Grace", "Jackson", "Lily", 
    "Wyatt", "Zoey", "Dylan", "Hazel", "Caleb", "Layla", "Luke", "Riley", "Matthew", "Nora", "Carter", "Eleanor", "Isaac", "Camila", 
    "Gabriel", "Aria", "Jayden", "Penelope", "Leo", "Chloe", "Levi", "Lillian", "Julian", "Addison", "Hudson", "Willow", "Grayson", 
    "Lucy", "Parker", "Savannah", "Zachary", "Victoria", "Aaron", "Aubrey", "Miles", "Hannah", "Connor", "Stella", "Lincoln", "Violet",
    "Ryan", "Aurora", "Ezra", "Paisley", "Nathan", "Brooklyn", "Hunter", "Ellie", "Joshua", "Samantha", "Cooper", "Leah", "Dominic", 
    "Ariana", "Isaiah", "Allison", "Andrew", "Sarah", "Adrian", "Cora", "Eli", "Madelyn", "Joseph", "Luna", "Charlie", "Elena", "Robert",
    "Natalie", "Samuel", "Maya", "Anthony", "Kinsley", "Theo", "Mila", "Adam", "Brielle", "Landon", "Sadie", "Evan", "Julia", "Carson",
    "Bella", "Brayden", "Clara", "Asher", "Eva", "Axel", "Quinn", "Christian", "Delilah", "Nolan", "Alice", "Jeremiah", "Ivy", "Jonathan",
    "Hazel", "Easton", "Ruby", "Xavier", "Rose", "Max", "Anna", "Nicholas", "Eloise", "Levi", "Kennedy", "Jacob", "Isla", "Gavin", 
    "Liliana", "Jackson", "Athena", "Christopher", "Emery", "Jaxon", "Mackenzie", "Henry", "Zara", "Elliot", "Alana", "Justin", "Eliza", 
    "Maverick", "Adalyn", "Declan", "Sydney", "Emmett", "Piper", "Chase", "Vivian", "Leo", "Bailey", "Calvin", "Marley", "Damian", "Adeline", 
    "Blake", "Charlotte", "Zane", "Isabelle", "Sawyer", "Hadley", "Nathaniel", "Reagan", "Finn", "Sienna", "Austin", "Clara", "Brody", "Adaline"
]

# 200 unique last names
last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", 
    "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", 
    "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", 
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart", "Sanchez", 
    "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", 
    "Torres", "Peterson", "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", 
    "Ross", "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler", 
    "Simmons", "Foster", "Gonzales", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford", "Hamilton", 
    "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan", "Owens", "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", 
    "Mcdonald", "Cruz", "Marshall", "Ortiz", "Gomez", "Murray", "Freeman", "Wells", "Webb", "Simpson", "Stevens", "Tucker", "Porter", 
    "Hunter", "Hicks", "Crawford", "Henry", "Boyd", "Mason", "Morales", "Kennedy", "Warren", "Dixon", "Ramos", "Reyes", "Burns", "Gordon", 
    "Shaw", "Holmes", "Rice", "Robertson", "Hunt", "Black", "Daniels", "Palmer", "Mills", "Nichols", "Grant", "Knight", "Ferguson", 
    "Rose", "Stone", "Hawkins", "Dunn", "Perkins", "Hudson", "Spencer", "Gardner", "Stephens", "Payne", "Pierce", "Berry", "Matthews", 
    "Arnold", "Wagner", "Willis", "Ray", "Watkins", "Olson", "Carroll", "Duncan", "Snyder", "Hart", "Cunningham", "Bradley", "Lane"
]

# Role configuration from COMMON_ROLE_CONFIG
COMMON_ROLE_CONFIG = {
    "SCRUM_MASTER": {"name": "Scrum Master", "count": 2},
    "PRODUCT_OWNER": {"name": "Product Owner", "count": 2},
    "TEAM_MEMBER": {"name": "TeamMember", "count": 20},
    "ADMIN": {"name": "Admin", "count": 1},
    "EDITOR": {"name": "Editor", "count": 1},
    "VIEWER": {"name": "Viewer", "count": 2},
    "MANAGER": {"name": "Manager", "count": 2},
    "CONTRIBUTOR": {"name": "Contributor", "count": 2},
    "DEVELOPER": {"name": "Developer", "count": 2},
    "DESIGNER": {"name": "Designer", "count": 2},
    "UI_UX": {"name": "UI/UX", "count": 5},
    "SYSTEM_ARCHITECT": {"name": "System Architect", "count": 5},
    "ENTERPRISE_ARCHITECT": {"name": "Enterprise Architect", "count": 5},
    "BUSINESS_OWNER": {"name": "Business Owner", "count": 5},
    "PROGRAM_MANAGER": {"name": "Program Manager", "count": 5},
    "PROJECT_MANAGER": {"name": "Project Manager", "count": 5},
    "PORTFOLIO_MANAGER": {"name": "Portfolio Manager", "count": 5},
    "BLOG_ADMIN": {"name": "Blog Admin", "count": 5},
    "BLOG_WRITER": {"name": "Blog Writer", "count": 5},
    "BLOG_EDITOR": {"name": "Blog Editor", "count": 5},
    "BLOG_VIEWER": {"name": "Blog Viewer", "count": 5},
    "SITE_ADMIN": {"name": "Site Admin", "count": 1},
    "ORG_ADMIN": {"name": "Org Admin", "count": 1},
    "PROJECT_ADMIN": {"name": "Project Admin", "count": 1},
    "QA": {"name": "QA", "count": 2},
    "ARCHITECT": {"name": "Architect", "count": 2},
    "DEVOPS": {"name": "DevOps", "count": 2},
    "SECURITY": {"name": "Security", "count": 2},
    "BUSINESS_ANALYST": {"name": "Business Analyst", "count": 2},
    "IT_ENGINEER": {"name": "IT Engineer", "count": 2},
    "NETWORK_ENGINEER": {"name": "Network Engineer", "count": 2},
    "TECH_LEAD": {"name": "Tech Lead", "count": 2},
    "PROJECT_LEAD": {"name": "Project Lead", "count": 2},
    "SUPER_USER": {"name": "Super User", "count": 0},
    "NO_ROLE": {"name": "No Role", "count": 0},
}

# Create a CSV file with the combination of usernames and roles
with open('user_roles.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write the header row
    writer.writerow(['first_name', 'last_name', 'username', 'email', 'role'])

    first_name_index = 0
    last_name_index = 0

    # Iterate through each role config and generate users
    for role_key, role_data in COMMON_ROLE_CONFIG.items():
        role_name = role_data["name"]
        count = role_data["count"]
        
        for _ in range(count):
            # Get first and last names from the list in a round-robin way
            first_name = first_names[first_name_index % len(first_names)]
            last_name = last_names[last_name_index % len(last_names)]

            username = f"{first_name.lower()}.{last_name.lower()}"
            email = f"{username}@example.com"

            # Write the row to the CSV
            writer.writerow([first_name, last_name, username, email, role_name])

            # Move to the next first and last name
            first_name_index += 1
            last_name_index += 1

print("CSV file 'user_roles.csv' has been created.")
