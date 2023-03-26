import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="StoriesAI",
    user="・・・",
    password="・・・"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE  storiestable(
    id SERIAL PRIMARY KEY, 
    title VARCHAR(600) NOT NULL, 
    select_font VARCHAR(500) NOT NULL,
    select_color VARCHAR(500) NOT NULL,
    length_text VARCHAR(10) NOT NULL, 
    length_plot VARCHAR(10) NOT NULL,
    category VARCHAR(100),
    hero VARCHAR(10), 
    cast1 VARCHAR(10), 
    cast2 VARCHAR(10), 
    cast3 VARCHAR(10), 
    story_term VARCHAR(20),
    keywords1 VARCHAR(10),
    keywords2 VARCHAR(10), 
    keywords3 VARCHAR(10),
    language  VARCHAR(10) NOT NULL,
    prompt VARCHAR(500) NOT NULL,
    stories_text_data VARCHAR(5000) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")




conn.commit()
conn.close()