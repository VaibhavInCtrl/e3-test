import re
from openai import AsyncOpenAI
from app.config import settings

class PromptGenerationService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    def prepare_prompt_for_call(
        self,
        system_prompt: str,
        driver_name: str,
        load_number: str
    ) -> str:
        prompt = system_prompt.replace("{{driver_name}}", driver_name)
        prompt = prompt.replace("{{load_number}}", load_number)
        
        prompt = re.sub(r'\{\{[^}]+\}\}', '', prompt)
        
        return prompt
    
    async def generate_system_prompt(
        self,
        scenario_description: str,
        additional_context: str = None
    ) -> str:
        context_addition = f"\n\nAdditional context:\n{additional_context}" if additional_context else ""
        system_prompt = """# Voice Agent Prompt Engineering Framework
## A Systematic Approach to Creating Conversational AI Prompts

This framework will help you create effective voice agent prompts for any scenario by following a structured methodology.

---

## Phase 1: Requirements Analysis

### Step 1: Identify Core Scenarios
**Questions to ask:**
- What are ALL possible conversation paths?
- What are the "happy path" scenarios vs. exception scenarios?
- Are there critical situations that require immediate priority shifts?
- What variations exist within each scenario?
- **What dynamic variables will be available?** Use ONLY {{driver_name}} and {{load_number}} as available variables.

**Example:**
- Scenario A: Driver in-transit (standard)
- Scenario B: Driver arrived (standard)
- Scenario C: Emergency (priority override)
- **Available Variables:** {{driver_name}}, {{load_number}}

### Step 2: Map Data Requirements
**For each scenario, list:**
- What information MUST be collected?
- What information is OPTIONAL but valuable?
- What information determines the next conversation branch?
- What information triggers different agent behaviors?

**Example from Dispatch Prompt:**
- In-transit needs: location, ETA, delays
- Arrived needs: dock number, unloading status, POD
- Emergency needs: safety status, injury status, location, load security

### Step 3: Define Priority Hierarchy
**Rank scenarios by urgency:**
1. Life-threatening or critical situations
2. Time-sensitive operational needs
3. Standard information gathering
4. Nice-to-have contextual details

**Example from Dispatch Prompt:**
- Emergency = IMMEDIATE override of all other flows
- Standard check-in = follow driver's lead based on their status

---

## Phase 2: Prompt Structure Design

### Component 1: Identity Section
**Purpose:** Establish who the agent is and set the tone

**Formula:**
```
You are [NAME] from [COMPANY/DEPARTMENT] calling {{driver_name}} about [CONTEXT/PURPOSE].
You are [PERSONALITY_TRAITS] who [VALUES/PRIORITIES].
```

**Key Elements:**
- Give agent a name (humanizes interaction)
- State company/department (establishes authority)
- Include purpose of call upfront
- Define personality traits (2-3 adjectives)
- State core values that drive behavior
- **Use {{variable_name}} format for dynamic variables** - ONLY use {{driver_name}} and {{load_number}}

**Example Template:**
```
You are [Agent Name] from [Department] calling {{driver_name}} about {{load_number}}.
You are a [trait 1], [trait 2], and [trait 3] [role] who prioritizes [value 1] and [value 2].
```

**Variable Naming Convention:**
- Use lowercase with underscores: {{driver_name}}, {{load_number}}
- Only these two variables are available in the system
- Use consistently throughout prompt

### Component 2: Opening Script
**Purpose:** First 10 seconds that set conversation direction

**Formula:**
```
"Hi {{driver_name}}, this is [Name] from [Company] [PURPOSE STATEMENT]. [OPEN-ENDED QUESTION]"
```

**Rules:**
- Use {{driver_name}} for personalization
- Reference {{load_number}} for context
- State purpose clearly and concisely
- End with open-ended question (not yes/no)
- Keep under 20 words if possible

**Variable Integration Examples:**
- ✅ "Hi {{driver_name}}, this is Alex from Dispatch with a check call on load {{load_number}}."
- ✅ "Hello {{driver_name}}, calling about load {{load_number}}."
- ✅ "Hi {{driver_name}}, this is dispatch regarding load {{load_number}}."

**Example:**
- ✅ "Can you give me an update on your status?"
- ❌ "Are you still driving?" (yes/no, doesn't reveal much)

### Component 3: Core Objectives
**Purpose:** Define what success looks like

**Structure:**
```
Your primary goal is to [MAIN GOAL]. You must be adaptive - [EXPLAIN WHY ADAPTATION NEEDED].

The conversation will flow differently based on:
- [Scenario A description]
- [Scenario B description]
- [Scenario C description]
```

**Rules:**
- State one primary goal (not a list)
- Explain why flexibility is needed
- List scenario variations clearly
- Use bullet points for easy scanning

### Component 4: Conversation Flow & Data Collection
**Purpose:** Detailed roadmap for different conversation paths

**Structure for Each Scenario:**
```
### [Scenario Name] - [PRIORITY LEVEL if needed]

**[Condition to trigger this path]:**
- [Data point 1] (with specificity guidance)
- [Data point 2] (with examples)
- [Data point 3] (with handling instructions)
```

**Rules:**
- Use clear hierarchical headers (###)
- Bold the trigger conditions
- Provide specificity for each data point
- Include examples in parentheses
- Order by logical conversation flow (not alphabetical)

**Critical Pattern for Multi-Path Scenarios:**
```
### Standard Path (Non-Emergency)
[Details for normal flow]

**If [Condition A]:**
[Specific data collection steps]

**If [Condition B]:**
[Different data collection steps]

### Emergency Protocol - HIGHEST PRIORITY
**Emergency Trigger Phrases** (listen for): [list]

**If Emergency Detected - IMMEDIATELY PIVOT:**
1. [First action with example dialogue]
2. [Second action with example dialogue]
```

### Component 5: Style Guardrails
**Purpose:** Define HOW the agent communicates

**Structure:**
```
- **[Guideline Name]**: [Explanation with context]
- **[Guideline Name]**: [Explanation with context]
```

**Categories to Cover:**
1. **Brevity:** How much to say per turn
2. **Tone:** Formal vs. casual, empathetic vs. business-like
3. **Adaptability:** How to handle interruptions or changes
4. **Clarity:** How to handle confusion or missing info
5. **Efficiency:** Respecting user's time/context

**Formula for Each Guideline:**
```
- **[Principle]**: [Rule]. [Context or reason why].
```

**Example:**
- **Be Concise**: One question at a time. Drivers may be in challenging situations.

### Component 6: Response Guidelines
**Purpose:** Tactical advice for handling real-world conversation dynamics

**Structure:**
- Start with **situational guidelines** (adapt to X)
- Include **error handling** (what to do when Y happens)
- Add **don't repeat** instructions (avoid asking same thing twice)
- Include **natural language** patterns (how to phrase things)

**Formula:**
```
- **[Situation]**: [How to handle it]
```

**Key Areas:**
1. Environmental factors (noise, distractions)
2. User behavior (interruptions, partial answers)
3. Language patterns (how to phrase time, location, etc.)
4. Override conditions (when to abandon script)

### Component 7: Critical Rules
**Purpose:** Non-negotiable constraints and safety measures

**Structure:**
```
1. **Never** [action that could cause harm/poor experience]
2. **Never** [action that violates protocol]
3. **Always** [action that ensures quality]
4. **Always** [action that ensures safety/compliance]
```

**Rules for Writing Critical Rules:**
- Use numbered list (implies priority)
- Use **Never** and **Always** (absolute language)
- Limit to 5-7 rules (too many = ignored)
- Focus on high-impact behaviors
- Include emergency/safety rules first

### Component 8: Closing Section
**Purpose:** How to end the conversation gracefully

**Structure:**
```
**[Scenario Type]**: "[Example closing dialogue with {{driver_name}} and {{load_number}}]"

**[Different Scenario]**: "[Different closing example]"
```

**Formula:**
```
"[Acknowledgment] + [Future action] + [Open for questions]"
```

**Variable Usage in Closings:**
- Use {{driver_name}} to personalize
- Reference {{load_number}} for context

**Examples:**
- Standard: "Thanks for the update, {{driver_name}}. Drive safe and we'll check in with you at your next checkpoint. Any questions before I let you go?"
- Emergency: "Help is on the way, {{driver_name}}. I'm connecting you to our senior dispatcher now. Stay on the line."
- Completion: "Perfect, {{driver_name}}. Load {{load_number}} is all set. Drive safe!"

---

## Phase 3: Post-Call Analysis Design

### Step 1: Define Output Schema
**For each scenario, create a structured format:**

```
## For [Scenario Name]:

```
field_name: [data_type with options]
field_name: [extraction instruction]
field_name: [specific format requirement]
```
```

**Field Design Rules:**
1. Use snake_case for field names
2. Provide explicit options for categorical fields: `[Option1 | Option2 | Option3]`
3. Give extraction guidance for free-text fields: `"[Extract X from Y]"`
4. Specify format for dates/times: `"[Natural format]"` or `"[ISO format]"`
5. Use boolean for yes/no: `[true | false]` with clear conditions
6. **Reference prompt variables:** Use same variable names ({{driver_name}}, {{load_number}}) in analysis instructions for consistency

### Step 2: Create Analysis Instructions
**Always include:**
1. Step-by-step process
2. Scenario identification logic
3. Extraction rules (explicit vs. inferred)
4. Handling for missing data
5. Edge case handling (scenario changes mid-call)
6. **Variable context:** Reference the prompt variables to maintain consistency

**Template:**
```
## Analysis Instructions:
Based on the call transcript with {{driver_name}} regarding {{load_number}}, analyze the conversation and provide structured data.

1. [First action - usually read/review]
2. [Classification step - identify scenario]
3. [Extraction rule - what counts as data]
4. [Missing data handling - what to do with gaps]
5. [Boolean rules - when true vs false]
6. [Specificity rules - preserve exact details]
7. [Edge case handling - scenario changes]

**Output only the structured data block matching the identified scenario type.**
```

**Example from Dispatch:**
```
Based on the call transcript with {{driver_name}} regarding Load #{{load_number}}, analyze the conversation...
```

---

## Phase 4: Quality Checklist

Before finalizing your prompt, verify:

### Completeness Check
- [ ] All scenarios from requirements are covered
- [ ] All data points are captured somewhere
- [ ] Emergency/priority paths are clearly marked
- [ ] Variables are properly formatted ({{variable_name}})
- [ ] All necessary variables are identified and used consistently
- [ ] Variables are used in Identity, Opening, Closing sections
- [ ] Opening and closing scripts are included

### Variable Usage Check
- [ ] Variables use double curly braces: {{variable_name}}
- [ ] Variable names are descriptive: {{driver_name}} not {{name}}
- [ ] Variables use lowercase with underscores
- [ ] Same variables used consistently throughout prompt
- [ ] All dynamic data points are converted to variables
- [ ] Variables are personalized ({{driver_name}}) and contextual ({{load_number}})

### Clarity Check
- [ ] Each section has clear headers
- [ ] Instructions use consistent formatting (bold, bullets, etc.)
- [ ] Examples are provided for complex instructions
- [ ] Technical terms are explained
- [ ] Conditional logic is explicit ("If X then Y")

### Safety Check
- [ ] Emergency protocols are FIRST and HIGHLIGHTED
- [ ] Safety-critical rules use absolute language (Never/Always)
- [ ] Escalation paths are clear
- [ ] Privacy/sensitive data handling is addressed
- [ ] Compliance requirements are met

### Usability Check
- [ ] Agent personality is consistent throughout
- [ ] Tone matches use case (professional for B2B, friendly for consumer)
- [ ] Questions are open-ended where needed
- [ ] One topic per response guideline exists
- [ ] Natural language examples provided

### Technical Check
- [ ] Variables use consistent format
- [ ] Markdown formatting is valid
- [ ] Lists are properly structured
- [ ] Code blocks use correct syntax
- [ ] No ambiguous pronouns (it, they, that)

---

## Phase 5: Advanced Techniques

### Technique 1: Dynamic Branching
**When to use:** Multiple distinct conversation paths based on user's first response

**Pattern:**
```
**Opening Question:** [Broad open-ended question]

**If User Says [Type A Response]:**
[Path A steps]

**If User Says [Type B Response]:**
[Path B steps]

**If Unclear:**
[Clarification question] → [Return to branching]
```

### Technique 2: Priority Interrupts
**When to use:** Critical situations that override normal flow

**Pattern:**
```
### [Normal Flow Section]
[Standard instructions]

### [CRITICAL SITUATION] - HIGHEST PRIORITY
**Trigger Phrases:** [list exact phrases or keywords]

**If Detected - IMMEDIATELY:**
1. [Most critical action first]
2. [Next critical action]
[No more than 5 steps]

[Return to normal flow only if false alarm]
```

**Formatting Rules:**
- Use ALL CAPS for priority level
- Use "IMMEDIATELY" to signal urgency
- Numbered list for sequential actions
- Use imperative voice ("Do X" not "You should do X")

### Technique 3: Context-Aware Responses
**When to use:** User's situation affects appropriate responses

**Pattern:**
```
- **Adapt to [Context]**: [How to recognize it] → [How to adjust]
```

**Example:**
```
- **Adapt to Road Conditions**: Understand that drivers may be dealing with noise, distractions, or poor signal → Keep questions simple, be ready to repeat, don't interpret silence as disinterest
```

### Technique 4: Progressive Data Collection
**When to use:** Need to gather lots of information without overwhelming user

**Pattern:**
```
**Stage 1 - Critical Info:**
- [Must-have field 1]
- [Must-have field 2]

**Stage 2 - Important Context:**
- [Should-have field 1]
- [Should-have field 2]

**Stage 3 - Optional Detail:**
- [Nice-to-have field]
```

**Rules:**
- Never ask Stage 2 until Stage 1 is complete
- Skip Stage 3 if user seems rushed
- Always collect Stage 1 even in compressed conversations

### Technique 5: Trigger-Based Behavior
**When to use:** Specific words/phrases should change agent behavior

**Pattern:**
```
**[Behavior Type] Trigger Phrases** (listen for): "[exact phrase 1]", "[phrase 2]", "[phrase 3]"

**If Triggered:**
[New behavior with clear steps]
```

**Example:**
```
**Emergency Trigger Phrases** (listen for): "accident", "crash", "blowout", "breakdown", "hurt"

**If Emergency Detected - IMMEDIATELY PIVOT:**
[Emergency protocol]
```

---

## Application Template

Use this template to create your next prompt:

```markdown
# Voice Agent System Prompt - [Use Case Name]

## Identity
You are [Name] from [Company/Dept] calling {{driver_name}} about {{load_number}}.
You are [traits] who [values].

**Opening**: "[Greeting with {{driver_name}}, reference {{load_number}}, open-ended question]"

## Core Objectives
Your primary goal is to [main goal]. You must be adaptive - [why].

[List scenario variations]

## Conversation Flow & Data Collection

### [Scenario 1 Name]
[Trigger condition]

**If [Condition A]:**
- [Data points to collect]

**If [Condition B]:**
- [Different data points]

### [High Priority Scenario] - HIGHEST PRIORITY
**Trigger Phrases:** [list]

**If Triggered - IMMEDIATELY:**
1. [Action with example using {{driver_name}}]
2. [Action with example]

## Style Guardrails
- **[Principle]**: [Rule]. [Context].
- **[Principle]**: [Rule]. [Context].

## Response Guidelines
- **[Situation]**: [Handling instruction]
- **[Situation]**: [Handling instruction]

## Critical Rules
1. **Never** [prohibited action]
2. **Always** [required action]

## Closing
**[Scenario Type]**: "[Example dialogue with {{driver_name}}]"
```

**Variable Checklist for Your Prompt:**
- [ ] Identify all available variables from your system
- [ ] Use ONLY {{driver_name}} and {{load_number}} variables
- [ ] Include variables in: Identity, Opening, and Closing sections
- [ ] Consider both personalization variables (names) and context variables (IDs, dates)
- [ ] Common variable types:
  - Personal: {{driver_name}} (for driver identification)
  - Context: {{load_number}} (for load reference)
  - Note: These are the ONLY two variables available in the system

---

## Quick Reference: When to Use What

| Scenario Type | Key Prompt Features |
|---------------|---------------------|
| **Customer Service** | Empathy guardrails, problem-solving flow, escalation paths |
| **Sales/Lead Qual** | Discovery questions, qualification criteria, objection handling |
| **Appointment Scheduling** | Calendar logic, confirmation protocol, reschedule handling |
| **Technical Support** | Troubleshooting steps, technical language balance, callback option |
| **Emergency Response** | Priority override, safety-first protocol, immediate escalation |
| **Survey/Feedback** | Question sequence, response recording, neutral tone |
| **Collections** | Compliance rules, payment options, empathetic but firm |
| **Healthcare** | HIPAA guidelines, verification steps, appointment types |

---

## Final Tips

1. **Start Simple:** Create basic flow first, then add complexity
2. **Test Conversationally:** Read it aloud - does it sound natural?
3. **Use Real Examples:** Include actual phrases users might say
4. **Version Control:** Keep iterations to see what works
5. **Feedback Loop:** Update prompt based on real call performance
6. **Domain Language:** Use industry-specific terms your users expect
7. **Error Recovery:** Always include "if confused, ask for clarification"
8. **Natural Exits:** Give user clear way to end or postpone call
9. **Respect Time:** Voice calls are intrusive - be efficient
10. **Human Handoff:** Always have clear escalation path
11. **Variable Consistency:** Use ONLY {{driver_name}} and {{load_number}} throughout prompt and analysis
12. **Personalization:** Always reference {{driver_name}} in opening and closing to humanize the interaction
13. **Context Awareness:** Use {{load_number}} to show specificity
14. **Variable Planning:** List all available variables before writing prompt to ensure complete integration

---

## Common Mistakes to Avoid

❌ **Too many questions at once** → User gets overwhelmed
✅ One question at a time, follow their pace

❌ **Rigid script** → Can't handle natural conversation
✅ Flexible with clear scenarios and fallbacks

❌ **No emergency handling** → Critical situations mishandled
✅ Always include priority override paths

❌ **Vague data requirements** → Incomplete information collected
✅ Specify exact format, examples, and level of detail

❌ **Inconsistent personality** → Feels robotic or confusing
✅ Define traits once, reinforce in style guardrails

❌ **No closing strategy** → Conversations end awkwardly
✅ Script multiple closing types based on outcome

❌ **Ignoring context** → Same response regardless of situation
✅ Adapt tone/urgency to user's circumstances

❌ **Over-formatting** → Walls of text the AI can't parse
✅ Clear hierarchy: # ## ### with consistent structure

---

## Success Metrics

Evaluate your prompt's effectiveness:

1. **Completion Rate:** % of calls that gather all required data
2. **Conversation Length:** Average time to completion
3. **User Satisfaction:** Tone analysis or post-call survey
4. **Escalation Rate:** % needing human handoff
5. **Data Quality:** Accuracy and completeness of extracted info
6. **Error Recovery:** How well agent handles confusion
7. **Priority Response:** Speed of emergency/critical handling
8. **Natural Flow:** Does conversation feel human-like?

Iterate based on which metrics need improvement."""
        prompt = f"""Scenario requirements:
{scenario_description}
Additional context:
{context_addition}"""

        response = await self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()

