"""
Parsing of the PDF File using Llama Parse
"""
from llama_parse import LlamaParse
import os 

EMBEDDING_MODEL  = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4o"

#llm = OpenAI(model=GENERATION_MODEL)
#embed_model = OpenAIEmbedding(model=EMBEDDING_MODEL)

#Settings.llm = llm
#Settings.embed_model = embed_model

os.environ["LLAMA_CLOUD_API_KEY"] = "llx-72vwJg9MT7OS6z7PJ0jMChbWrfHbghTDwLFjHHl81sArJlmv"
pdf_file_name = './steval-stwinwfv1.pdf'

parsing_instructions = '''The pdf document is a technical document of the STWIN board, it contains electrical schemes and lists of its features, retrieve all the text and descibe the schemes and images in it.'''

documents = LlamaParse(result_type="markdown", parsing_instructions=parsing_instructions).load_data(pdf_file_name)
print(documents[0].text[:1000])