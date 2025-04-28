from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from typing import Annotated
from extract_cli import extract

app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.get("/extract", response_model=dict)
def extract_from_text(text: str,
                      f: Annotated[list[str] | None, Query(description="List of tags to filter by")] = None,
                      e: bool = Query(default=False, description="Use filter tags as an exclusion list?"),
                      o: int = Query(default=100, description="Fuzzy matching threshold (0-100)"),
                      p: bool = Query(default=False, description="Use premium translation?")):
    if not text:
        return JSONResponse(content={"error": "Please provide a text to extract from."}, status_code=400)
    results_dataframe = extract(text=text, filter_tags=f or [], exclude=e, fuzzy_threshold=o, use_premium=p)
    if results_dataframe is None:
        return {}
    return results_dataframe.to_dict()
