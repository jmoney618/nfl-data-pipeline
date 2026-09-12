#db_utils.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

def load_to_postgres(df, table_name, schema="raw"):
	"""
	Accepts a  pandas DataFrame and pushes it to PostgreSQL using environment variables.
	"""
	# Fetch credentials securely from the environment
	USER = os.getenv("DB_USER")
	PASSWORD = os.getenv("DB_PASSWORD", "") # Defaults to empty string if not found
	HOST = os.getenv("DB_HOST")
	PORT = os.getenv("DB_PORT")
	DATABASE = os.getenv("DB_NAME")

	# Build the connection engine securely
	connection_string = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
	engine = create_engine(connection_string)

	print(f"Connecting to DB and dumping data into {schema}.{table_name}...")

	df.to_sql(
		name=table_name,
		con=engine,
		schema=schema,
		if_exists="replace",
		index=False
	)
	print("Upload successful!")
