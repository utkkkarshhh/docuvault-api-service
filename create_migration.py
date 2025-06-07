import subprocess
from datetime import datetime

# Generate a timestamp
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Create a migration name with the timestamp
migration_name = f"auto_{timestamp}"

# Run the makemigrations command with the custom name
subprocess.call(["python", "manage.py", "makemigrations", "service", f"--name={migration_name}"])
