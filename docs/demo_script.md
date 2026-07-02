# 5-Minute Demo Script

## 1. Start Service
```powershell
uvicorn app.main:app --reload
```
Open: http://127.0.0.1:8000/docs

## 2. Mandatory URL Shortener Flow
### Create
```powershell
curl -X POST "http://127.0.0.1:8000/links" -H "Content-Type: application/json" -d '{"original_url":"https://example.com"}'
```
Copy `short_code` from response.

### Redirect
```powershell
curl -i "http://127.0.0.1:8000/<short_code>"
```
Expect `307 Temporary Redirect` + `Location` header.

### Metadata
```powershell
curl "http://127.0.0.1:8000/links/<short_code>"
```

### Stats
```powershell
curl "http://127.0.0.1:8000/links/<short_code>/stats"
```

## 3. AI-Assisted Engineering Pipeline
### Greenfield
```powershell
curl -X POST "http://127.0.0.1:8000/engineering/run" -H "Content-Type: application/json" --data-binary "@examples/greenfield_requirement.json"
```

### Brownfield
```powershell
curl -X POST "http://127.0.0.1:8000/engineering/run" -H "Content-Type: application/json" --data-binary "@examples/brownfield_requirement.json"
```

### Ambiguous
```powershell
curl -X POST "http://127.0.0.1:8000/engineering/run" -H "Content-Type: application/json" --data-binary "@examples/ambiguous_requirement.json"
```

Optional: show pre-generated scenario outputs used in submission package:
```powershell
Get-Content examples/greenfield_output.json
Get-Content examples/brownfield_output.json
Get-Content examples/ambiguous_output.json
```

## 4. Validation
```powershell
python -m pytest -q
```

## 5. Close With Engineering Rationale
- AI assists within each development task, not autonomous end-to-end coding.
- Engineer validates outputs (tests + review + risk checks).
- Trade-offs and limitations are explicitly documented.