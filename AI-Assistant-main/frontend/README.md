Holly AI Assistant
Holly is an AI-powered leasing and resident assistant built for property management teams. Designed to integrate directly with Entrata, Supabase, and AWS, Holly automates communication across multiple channels — including web chat, SMS, and voice — while maintaining full control, customization, and brand consistency for each property.

Project Status
✅ Entrata API integration (live property/unit data)

✅ Supabase database for dynamic property knowledge base

✅ AI assistant built with OpenAI GPT models

✅ Web dashboard (in progress) for managing property knowledge

✅ Initial billing for chat usage tied to properties

🚧 Admin panel UI (property-specific editing and approvals)

🚧 Voice call integration (Twilio planned for MVP demo)

🚧 Resident vs Prospect logic branching

🚧 Maintenance request routing logic (in planning)

Features
Multi-Channel Communication: Chat, SMS, and Voice (demo version)

Dynamic Knowledge Base: Per-property FAQs, updated via Supabase

Live Property Data Sync: Pulls live unit and property info via Entrata API

Customizable Branding: Property teams can customize assistant names, responses, and workflows

Automation Ready: Future plans include rent collection, maintenance triaging, and lead nurturing automations

Cost-Efficient: Designed to significantly reduce reliance on third-party solutions like Elise AI while offering more control

Tech Stack

Category	Tools/Frameworks
Backend	Node.js, Python (for scripts)
Frontend	React, TailwindCSS (Admin Dashboard)
Database	Supabase
Hosting	AWS (S3, Lambda planned), Vercel (frontend)
APIs	Entrata Partner API, OpenAI API, Twilio (planned)
Automation	Playwright (for scraping), Custom Scripts
Setup Instructions (for Local Dev)
Clone the Repository

bash
Copy
Edit
git clone https://github.com/yourusername/holly-ai-assistant.git
cd holly-ai-assistant
Install Frontend Dependencies

bash
Copy
Edit
cd frontend
npm install
npm run dev
Environment Variables Create .env files in both the frontend and backend folders. Example variables include:

ini
Copy
Edit
OPENAI_API_KEY=your-openai-key
ENTRATA_API_KEY=your-entrata-key
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-api-key
TWILIO_ACCOUNT_SID=(future)
TWILIO_AUTH_TOKEN=(future)
Run Backend Scripts (API Integrations, etc.)

Example:

bash
Copy
Edit
python sync_properties.py
Database Initialization

Import initial CSV of property knowledge into Supabase (Admin > Table Editor > Import).

Deployment

Frontend: Vercel

Backend: AWS Lambda (planned) or dedicated server for MVP

Demo Plan (MVP)
Show web chat interaction with Holly answering leasing questions.

Show dashboard to update knowledge base.

Call Holly via Twilio demo number to showcase voice capabilities.

Emphasize real-world time savings and control vs current solution (Elise AI).

Future Roadmap
📞 Full voice support: Answering calls after hours and routing maintenance.

🛠️ Maintenance ticket generation (direct to Entrata or email).

📈 Advanced analytics dashboard for lead/resident interactions.

🤖 RAG (Retrieval Augmented Generation) for even faster/fact-checked responses.

🏡 Expandable architecture for other industries (beyond property management).

License
© 2025 Jesus Acosta
All rights reserved. This project is proprietary.