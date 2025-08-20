import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

from crew import MarketingCrew  # Import the CrewBase class

app = FastAPI(title="CrewAI Marketing API")

# Input schema (matching Streamlit)
class AgentRequest(BaseModel):
    message: str
    goal: str
    audience: str
    platform: str

@app.post("/run")
def run_agent(req: AgentRequest):
    try:
        marketing_crew = MarketingCrew().marketing_crew()

        # Map Streamlit fields → crew inputs
        crew_inputs = {
            "product_name": req.goal,
            "target_audience": req.audience,
            "product_description": req.message,
            "budget": "N/A",
            "current_date": datetime.now().strftime("%Y-%m-%d"),
            "platform": req.platform,
            "goal": req.goal  # so {goal} works in tasks/agents
        }

        result = marketing_crew.kickoff(inputs=crew_inputs)

        # Decide response type
        if req.message.lower().startswith("generate campaign"):
            return {"content": result}
        else:
            return {"reply": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
