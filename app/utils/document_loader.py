import logging
from typing import List, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def load_architecture_documents(docs_directory: str) -> List[Dict[str, Any]]:
    documents = []
    docs_path = Path(docs_directory)
    
    if not docs_path.exists():
        raise FileNotFoundError(f"Directory not found: {docs_directory}")
    
    # Find all .txt files
    txt_files = list(docs_path.glob("*.txt"))
    
    if not txt_files:
        raise ValueError(f"No .txt files found in {docs_directory}")
    
    logger.info(f"Found {len(txt_files)} architecture documents to load")
    
    for txt_file in txt_files:
        try:
            # Read file content
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the structured content
            parsed_doc = parse_architecture_document(content, txt_file.name)
            
            # Chunk the document (each section becomes a chunk for better retrieval)
            chunks = chunk_architecture_document(parsed_doc)
            
            documents.extend(chunks)
            
            logger.info(f"Loaded and chunked: {txt_file.name} ({len(chunks)} chunks)")
            
        except Exception as e:
            logger.error(f"Error loading {txt_file.name}: {str(e)}")
            continue
    
    logger.info(f"Total chunks created: {len(documents)}")
    return documents


def parse_architecture_document(content: str, filename: str) -> Dict[str, Any]:
    doc = {
        'filename': filename,
        'architecture': '',
        'description': '',
        'key_components': '',
        'pros': '',
        'cons': '',
        'use_cases': '',
        'full_text': content
    }
    
    # Define field markers
    fields = [
        ('Architecture:', 'architecture'),
        ('Description:', 'description'),
        ('KeyComponents:', 'key_components'),
        ('Pros:', 'pros'),
        ('Cons:', 'cons'),
        ('UseCases:', 'use_cases')
    ]
    
    lines = content.split('\n')
    current_field = None
    current_content = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if this line is a field marker
        field_found = False
        for marker, field_name in fields:
            if line_stripped.startswith(marker):
                # Save previous field content
                if current_field:
                    doc[current_field] = '\n'.join(current_content).strip()
                
                # Start new field
                current_field = field_name
                current_content = [line_stripped[len(marker):].strip()]
                field_found = True
                break
        
        if not field_found and current_field:
            # Continue adding to current field
            current_content.append(line)
    
    # Save last field
    if current_field:
        doc[current_field] = '\n'.join(current_content).strip()
    
    return doc


def chunk_architecture_document(parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    chunks = []
    architecture_name = parsed_doc['architecture']
    
    # Create a main overview chunk
    overview_text = f"""
        Architecture: {parsed_doc['architecture']}

        Description: {parsed_doc['description']}

        Key Components: {parsed_doc['key_components']}
        """
    
    chunks.append({
        'text': overview_text,
        'metadata': {
            'source': parsed_doc['filename'],
            'architecture': architecture_name,
            'section': 'overview'
        }
    })
    
    # Create a pros/cons evaluation chunk
    evaluation_text = f"""
        Architecture: {parsed_doc['architecture']}

        Pros: {parsed_doc['pros']}

        Cons: {parsed_doc['cons']}
        """
    
    chunks.append({
        'text': evaluation_text,
        'metadata': {
            'source': parsed_doc['filename'],
            'architecture': architecture_name,
            'section': 'evaluation'
        }
    })
    
    # Create a use cases chunk
    use_cases_text = f"""
        Architecture: {parsed_doc['architecture']}

        Use Cases: {parsed_doc['use_cases']}

        Description: {parsed_doc['description']}
        """
    
    chunks.append({
        'text': use_cases_text,
        'metadata': {
            'source': parsed_doc['filename'],
            'architecture': architecture_name,
            'section': 'use_cases'
        }
    })
    
    return chunks
