import os
import re
import numpy 
import pandas
import json
import numpy 
import faiss
from pathlib import Path
from pypdf import PdfReader
from docx import Document
from typing import Dict
from numpy.typing import NDArray
from sklearn.cluster import KMeans
from llama_index.core.node_parser import SentenceSplitter, SimpleNodeParser
from llama_index.core import Settings,VectorStoreIndex