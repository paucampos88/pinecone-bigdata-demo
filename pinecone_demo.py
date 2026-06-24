from pinecone import Pinecone, ServerlessSpec
import os


INDEX_NAME = "demo-bigdata-pinecone"
NAMESPACE = "demo"
DIMENSION = 5


pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])


existing_indexes = [idx.name for idx in pc.indexes.list()]
if INDEX_NAME not in existing_indexes:
    pc.indexes.create(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )


index = pc.index(INDEX_NAME)


records = [
    {
        "id": "doc_kubernetes",
        "values": [0.95, 0.10, 0.20, 0.05, 0.02],
        "metadata": {
            "titulo": "Kubernetes para aplicaciones distribuidas",
            "categoria": "cloud",
        },
    },
    {
        "id": "doc_relacional",
        "values": [0.05, 0.98, 0.10, 0.05, 0.02],
        "metadata": {
            "titulo": "Fundamentos de bases de datos relacionales",
            "categoria": "database",
        },
    },
    {
        "id": "doc_cloud",
        "values": [0.80, 0.35, 0.25, 0.10, 0.05],
        "metadata": {
            "titulo": "Arquitecturas modernas de computación en la nube",
            "categoria": "cloud",
        },
    },
    {
        "id": "doc_ml",
        "values": [0.08, 0.20, 0.92, 0.05, 0.10],
        "metadata": {
            "titulo": "Conceptos básicos de Machine Learning",
            "categoria": "ai",
        },
    },
    {
        "id": "doc_devops",
        "values": [0.75, 0.10, 0.15, 0.80, 0.05],
        "metadata": {
            "titulo": "Implementación de sistemas DevOps",
            "categoria": "software",
        },
    },
]


index.upsert(vectors=records, namespace=NAMESPACE)


def buscar(nombre, vector, filtro=None):
    resultados = index.query(
        namespace=NAMESPACE,
        vector=vector,
        top_k=2,
        include_metadata=True,
        filter=filtro,
    )
    print("\n" + nombre)
    for match in resultados.matches:
        print(round(match.score, 3), match.id, match.metadata["titulo"])


buscar(
    "Consulta 1: tecnologias para administrar contenedores",
    [0.90, 0.08, 0.20, 0.10, 0.00],
)


buscar(
    "Consulta 2: organizacion de datos en tablas relacionales",
    [0.05, 0.95, 0.05, 0.02, 0.00],
)


buscar(
    "Consulta 3: automatizacion de despliegues de software",
    [0.65, 0.10, 0.15, 0.85, 0.00],
    filtro={"categoria": "software"},
)
