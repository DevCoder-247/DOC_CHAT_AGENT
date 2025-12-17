from nebula3.gclient.net import ConnectionPool
from nebula3.Config import Config

config = Config()
config.max_connection_pool_size = 10

pool = ConnectionPool()
pool.init([("127.0.0.1", 9669)], config)

def get_session():
    return pool.get_session("root", "nebula")

SPACE = "doc_graph"

def ensure_space():
    session = get_session()
    session.execute(f"""
    CREATE SPACE IF NOT EXISTS {SPACE}
    (vid_type=FIXED_STRING(256));
    """)
    session.execute(f"USE {SPACE}")
    session.release()


# def create_doc_node(doc_id, title):
#     session = get_session()
#     session.execute(
#         f'INSERT VERTEX Document(title) VALUES "{doc_id}":("{title}")'
#     )

def insert_document(doc_id, title):
    s = get_session()
    s.execute(f"USE {SPACE}")
    s.execute(
        f'INSERT VERTEX Document(doc_id, title) VALUES "{doc_id}":("{doc_id}", "{title}")'
    )
    s.release()

def insert_chunk(doc_id, chunk_id, text):
    s = get_session()
    s.execute(f"USE {SPACE}")

    safe_text = (
        text.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", " ")
    )

    s.execute(
        f'''
        INSERT VERTEX Chunk(chunk_id, text)
        VALUES "{chunk_id}":("{chunk_id}", "{safe_text}");
        '''
    )

    s.execute(
        f'''
        INSERT EDGE HAS_CHUNK()
        VALUES "{doc_id}"->"{chunk_id}":();
        '''
    )

    s.release()


# c.Chunk.text 
# must be added with tag name 
def graph_search_keywords(keywords, limit=5):
    if not keywords:
        return []

    s = get_session()
    s.execute(f"USE {SPACE}")

    clauses = []
    for kw in keywords:
        clauses.append(f'c.Chunk.text CONTAINS "{kw}"')
        clauses.append(f'c.Chunk.text CONTAINS "{kw.capitalize()}"')
        clauses.append(f'c.Chunk.text CONTAINS "{kw.upper()}"')

    kw_filter = " OR ".join(clauses)

    query = f"""
    MATCH (d:Document)-[:HAS_CHUNK]->(c:Chunk)
    WHERE {kw_filter}
    RETURN c.Chunk.text AS text
    LIMIT {limit}
    """

    result = s.execute(query)

    texts = [
        row.values[0].get_sVal().decode("utf-8")
        for row in result.rows()
    ]

    s.release()
    return texts






def clear_graph():
    s = get_session()
    s.execute(f"USE {SPACE}")

    s.execute("MATCH ()-[r]->() DELETE r")
    s.execute("MATCH (n) DELETE n")

    s.release()


ensure_space()


