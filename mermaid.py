from typing import Literal, Tuple, Dict
import json

DiagramType = Literal['flowchart', 'sequenceDiagram', 'classDiagram']

def clean_mermaid_code(text: str):
    code = text.strip()
    start = code.split('\n')[0].strip().lower()

    if start.startswith('graph') or start.startswith('flowchart'):
        return {
            'type': 'flowchart',
            'code': code
        }
    elif start.startswith('sequencediagram'):
        return {
            'type': 'sequenceDiagram',
            'code': code
        }
    elif start.startswith('classdiagram'):
        return {
            'type': 'classDiagram',
            'code': code
        }
    else:
        raise ValueError("Invalid mermaid code")
import re
def convertToJson(code: str) -> str:
    mermaid_lines = [line.strip() for line in code.strip().splitlines()]
    joined_mermaid = "\n".join(mermaid_lines)

    # Convert to JSON format
    json_output = json.dumps({"mermaid_syntax": joined_mermaid}, separators=(',', ':'))
    return json_output



# --- Supabase below for fetching tohe requrement and diagram type ---
from supabase import create_client, Client
from typing import Tuple, Optional

SUPABASE_URL = "https://ydogoylwenufckscqijp.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlkb2dveWx3ZW51ZmNrc2NxaWpwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY3MzUxNjYsImV4cCI6MjA1MjMxMTE2Nn0.Oy0K0aalki4e4b5h8caHYdWxZVKB6IWDDYQ3zvCUu4Y"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_latest_req_diagramType() -> Optional[Tuple[str, str]]:
    """
    Fetch the latest requirement and diagram_type input from Supabase.
    Returns: Tuple of (requirement, diagram_type) 
    """
    try:
        # will modify tablename once found database table , need to double check with charles
        response = supabase.table("able_name").select("requirement, diagram_type").order("created_at", desc=True).limit(1).execute()

        if not response.data:
            print("No input found.")
            return None

        latest = response.data[0]
        requirement = latest['requirement'].strip()
        diagram_type = latest['diagram_type'].strip()

        return requirement, diagram_type

    except Exception as e:
        print("Error fetching input:", str(e))
        return None

   


if __name__ == "__main__":

    try:
        '''fetch plain text req and diagram type'''
        result = fetch_latest_req_diagramType()
        if result:
            requirement, diagram_type = result
            #test purpose 
            print("Requirement:", "If the seatbelt is unbuckled while the vehicle is in motion, alert the driver within 3 seconds.")
            print("Diagram Type:", "Flowchart")

            

            # Then use the req and diagram type here as input and 
            # use LLM for gernerate mermaid output(assigned for evan)

            '''also this below part for mermaid syntax will be not static , 
            content will be the output from Evan generate and assign here'''

            mermaid = """
            graph TD
            A[Vehicle in motion]->B{Seatbelt unbuckled?}
            B -- No->F[No action]
            B --Yes->C[Start 3s timer]
            C -> D{Alert within 3 seconds?}
            D -- Yes--E[Alert driver]
            D -- No --G[Timeout / Failed]
            """
        else:
            print("Failed to fetch inputs.")

        #clean to mermaid syntax
        result = clean_mermaid_code(mermaid)
        print("Detected Diagram Type:", result['type'])
        print("Clean Mermaid Code:\n", result['code'])
        jsonRes = convertToJson(mermaid)
        print("Json Mermaid Code:\n", jsonRes)

    except Exception as e:
        print("Error:", str(e))
