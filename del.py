from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://neondb_owner:npg_cV97DHAhJtne@ep-aged-mouse-ator01be-pooler.c-9.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.fetchone())

except Exception as e:
    print(e)