Architecture and Design Decisions:
	1.	UI library: shadcn/ui + tailwind css
why: beautiful, accessible components that you own (not a dependancy). tailwind makes styling super fast without custom css.
reason for choice: full control over components and better customisation without bloated deps.
	2.	State management: tanstack query (react query)
why: handles server state with caching, background refetching, and optimistic updates. no redux headache needed.
reason for choice: made for server state and removes 90% of redux boilerplate.
	3.	LLM: openai gpt-4
why: used for two main things:
    (1) dynamic prompt generation - turns simple scenario descriptions into detailed system prompts
    (2) post-call analysis - pulls out structured data from call transcripts
    alternative: retell’s built-in analysis
reason for choice: custom llm gives full control on data extraction per scenario.
	4.	API auth: simple api key
why: its an internal tool so api key in headers is enough and super easy to setup.
alternative: jwt, oauth
reason for choice: much simpler for internal app, no complex user roles.
	5.	Form handling: react hook form + zod
why: great performance, fewer re-renders, zod gives awesome typescript validation.
alternative: formik
reason for choice: faster, cleaner and better ts support.
	6.	Routing: react router v6
why: solid choice for react spas with simple declarative syntax.
reason for choice: mature and widely used with good community support.

Key Implementation Decisions

- variable handling in prompts
decision: use {{driver_name}} and {{load_number}} format for dynamic vars.
why: simple and predictable, retell ai replaces them when a call starts.

- prompt generation strategy
decision: llm creates detailed prompts from user’s natural language input.
why: lets non-tech users build smart ai agents easily — they just describe what they want.

- post-processing approach
decision: use custom llm extraction instead of retell’s default one.
why: gives full control over what’s extracted, can change logic per usecase, no limitations.

- web calls vs phone calls
decision: only doing web calls (browser based).
why: im in india, phone calls would’ve added extra costs.

- real-time updates
decision: polling instead of websockets.
why: easier to build, update freq is fine, retell webhooks handle live call events anyway.

- modular architecture
decision: split services for agents, drivers, conversations, calls, and webhooks.
why: easy to test, maintain, and scale — each part does one job well.


# GETTING STARTED

Prerequisites
Python 3.11 or higher
Node.js 18 or higher
OpenAI API key

## BACKEND SETUP

1. Navigate to backend directory:
cd be-e3

2. Create virtual environment:
python -m venv env
source env/bin/activate
(On Windows: env\Scripts\activate)

3. Install dependencies:
pip install -r requirements.txt

4. Set up with shared environment variables:
Open .env and add your credentials, rest remain the same:
OPENAI_API_KEY=your_openai_api_key

5. Start the backend server:
uvicorn app.main:app --reload --port 8000

Backend will be running at http://localhost:8000
API documentation available at http://localhost:8000/docs

## FRONTEND SETUP

1. Navigate to frontend directory:
cd fe-e3

2. Install dependencies:
npm install

3. Set up environment variables:
Add .env

4. Start the development server:
npm run dev

Frontend will be running at http://localhost:5173

# USING THE APPLICATION

1. Create an Agent
Go to the Agents page
Click Create Agent
Enter a natural language scenario description of what you want the agent to do
The system will automatically generate a detailed system prompt

2. Add Drivers
Go to the Drivers page
Click Add Driver
Enter driver name and phone number

3. Start a Test Call
Go to the Test page
Select an agent and driver
Enter a load number
Click Start Test Call
Allow microphone access when prompted
Speak with the AI agent
Click End Call when finished

4. View Results
The conversation will automatically update with full transcript, extracted structured data, recording URL, and call duration
View all conversations in the Conversations page
Click on any conversation to see details

## CONFIGURATION

Retell AI Settings:
Voice: 11labs-Adrian (customizable)
Backchannel: Enabled (agent says "uh-huh", "yeah", etc.)
Interruption Sensitivity: 0.8 (allows natural interruptions)
Ambient Sound: Coffee shop (adds realistic background)
End Call After Silence: 30 seconds

## OpenAI Settings:
Model: GPT-4o (configurable)
Temperature: 0.7 for prompt generation, 0.3 for data extraction
Response Format: JSON for structured data extraction

## DEVELOPMENT

Backend Development:
Run: uvicorn app.main:app

Frontend Development:
Run dev server: npm run dev

## SECURITY NOTES

API keys are required for all backend endpoints
Supabase handles database security with Row Level Security (RLS)
CORS is configured to allow all origins in development (restrict in production)