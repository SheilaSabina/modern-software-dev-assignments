# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Sheila Sabina \
SUNet ID: 2310817220028 \
Citations: N/A

This assignment took me about 4-6 hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
I want to perform TODO 1. Implement LLM extraction using Ollama in services/extract.py. The prompt should be flexible to detect the input language and return a JSON list of action items.

Generated Code Snippets:
week2/app/services/extract.py: Line 85-130 (fungsi extract_action_items_llm).

### Exercise 2: Add Unit Tests
Prompt: 
Generate unit tests for the extraction service in tests/test_extract.py to ensure both Regex and LLM extraction work for various Indonesian and English inputs.

Generated Code Snippets:
week2/tests/test_extract.py: All line.

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
I want to perform TODO 3. Refactor week2/app/main.py and its routers to use FastAPI lifespan, ensure Pydantic schemas are used for all endpoints, and clean up the database layer to return dictionaries.

Generated/Modified Code Snippets:
- week2/app/main.py: Line 1-40 (lifespan implementation).
- week2/app/routers/notes.py: Use of Pydantic models.
- week2/app/services/db.py: Added dict(row) to fetch data.


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
Improve the frontend in week2/frontend/index.html with a premium blue theme. Add a custom delete modal and top-center toast notifications for success messages

Generated Code Snippets:
- week2/frontend/index.html: Line 10-150 (CSS & Modal/Toast Logic).
- week2/app/routers/notes.py: Added endpoint @router.delete("/{note_id}").


### Exercise 5: Generate a README from the Codebase
Prompt: 
Generate a comprehensive README.md for this Week 2 project based on the current codebase, explaining how to run the FastAPI server and use the AI extraction features.

Generated Code Snippets:
week2/README.md: All line.


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 