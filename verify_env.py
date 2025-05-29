from dotenv import load_dotenv
import os

load_dotenv()

for var in ["INFLUX_URL", "INFLUX_TOKEN", "INFLUX_ORG", "INFLUX_BUCKET"]:
    print(f"{var}: {repr(os.getenv(var))}")

