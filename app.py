from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Comprehensive dataset: Bryant University majors mapped to BLS occupations
# Salary data sourced from BLS Occupational Outlook Handbook (May 2024 estimates)
# Growth projections from BLS 2023-2033 outlook
MAJORS_DATA = [
    {
        "id": 1,
        "major": "Accounting",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Ranked in the top 4% nationally. Prepares for CPA and professional exams through real-world learning.",
        "breadth_score": 35,
        "breadth_label": "Focused",
        "typical_outcomes": "A defined pipeline: most grads start in public accounting or corporate accounting on the CPA track, with later pivots into consulting, forensics, and CFO roles.",
        "careers": [
            {
                "title": "Accountant / Auditor",
                "bls_code": "13-2011",
                "median_salary": 79880,
                "entry_salary": 50440,
                "top_salary": 132690,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 1538400,
                "annual_openings": 126500,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/accountants-and-auditors.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 65,
                "ai_analysis": "Routine bookkeeping and data entry are rapidly being automated. However, strategic advisory, complex tax planning, forensic accounting, and client relationships remain human-driven. CPAs who embrace AI tools for audit analytics will thrive; those doing only compliance work face displacement."
            },
            {
                "title": "Financial Examiner",
                "bls_code": "13-2061",
                "median_salary": 84300,
                "entry_salary": 53340,
                "top_salary": 153870,
                "growth_rate": 11,
                "growth_label": "Much faster than average",
                "total_employment": 67600,
                "annual_openings": 5100,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/financial-examiners.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 50,
                "ai_analysis": "AI enhances fraud detection and compliance monitoring, but regulatory judgment, interpretation of complex financial structures, and enforcement decisions require human expertise. Growing regulatory complexity may actually increase demand."
            }
        ]
    },
    {
        "id": 2,
        "major": "Actuarial Mathematics",
        "college": "College of Arts & Sciences",
        "degree": "BS",
        "description": "Intersects mathematics and business. 100% employment rate for graduates. Prepares for actuarial exams.",
        "breadth_score": 20,
        "breadth_label": "Focused",
        "typical_outcomes": "One of the most focused paths in the catalog — nearly all grads pursue actuarial roles in insurance and pensions, with the exam track mapped out for a decade.",
        "careers": [
            {
                "title": "Actuary",
                "bls_code": "15-2011",
                "median_salary": 120000,
                "entry_salary": 72960,
                "top_salary": 214000,
                "growth_rate": 23,
                "growth_label": "Much faster than average",
                "total_employment": 36100,
                "annual_openings": 2700,
                "bls_url": "https://www.bls.gov/ooh/math/actuaries.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "While AI can automate some modeling tasks, actuaries' deep expertise in risk assessment, regulatory requirements, and professional judgment is hard to replicate. AI is more of a productivity multiplier here. The profession's exam-based credentialing creates a strong moat."
            }
        ]
    },
    {
        "id": 3,
        "major": "Applied Mathematics and Statistics",
        "college": "College of Arts & Sciences",
        "degree": "BS",
        "description": "Develop skills to solve real-world problems through mathematical principles and statistical methods.",
        "breadth_score": 90,
        "breadth_label": "Very Broad",
        "typical_outcomes": "A classic generalist launchpad: grads land in banking, tech, insurance, government, and research — quantitative skills transfer almost anywhere.",
        "careers": [
            {
                "title": "Mathematician / Statistician",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "15-2041",
                "median_salary": 104860,
                "entry_salary": 61070,
                "top_salary": 170110,
                "growth_rate": 30,
                "growth_label": "Much faster than average",
                "total_employment": 46300,
                "annual_openings": 4400,
                "bls_url": "https://www.bls.gov/ooh/math/mathematicians-and-statisticians.htm",
                "ai_impact": "Low",
                "ai_impact_score": 20,
                "ai_analysis": "Mathematicians and statisticians are the architects behind AI itself. Strong demand driven by data-heavy industries. Those who understand both theory and application are uniquely positioned to lead AI development and validation."
            },
            {
                "title": "Data Scientist",
                "bls_code": "15-2051",
                "median_salary": 108020,
                "entry_salary": 60780,
                "top_salary": 184650,
                "growth_rate": 36,
                "growth_label": "Much faster than average",
                "total_employment": 192300,
                "annual_openings": 17700,
                "bls_url": "https://www.bls.gov/ooh/math/data-scientists.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Data scientists are AI enablers, not AI victims. While AutoML handles some routine modeling, the need for domain expertise, experimental design, causal inference, and communicating insights to stakeholders keeps demand very high."
            }
        ]
    },
    {
        "id": 4,
        "major": "Arts and Creative Industries",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Gain skills for creative ambitions with studio and practical learning in arts management and production.",
        "breadth_score": 45,
        "breadth_label": "Moderate",
        "typical_outcomes": "Grads scatter across media production, arts management, advertising, and design — many doors, but most are within the creative economy.",
        "careers": [
            {
                "title": "Art Director",
                "bls_code": "27-1011",
                "median_salary": 106500,
                "entry_salary": 56640,
                "top_salary": 196040,
                "growth_rate": 7,
                "growth_label": "As fast as average",
                "total_employment": 107300,
                "annual_openings": 9200,
                "bls_url": "https://www.bls.gov/ooh/arts-and-design/art-directors.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 55,
                "ai_analysis": "Generative AI is transforming visual content creation, but art directors who provide creative vision, brand strategy, and team leadership remain essential. The role shifts from producing to curating and directing AI-assisted workflows."
            },
            {
                "title": "Producer / Director",
                "bls_code": "27-2012",
                "median_salary": 82510,
                "entry_salary": 40040,
                "top_salary": 184660,
                "growth_rate": 7,
                "growth_label": "As fast as average",
                "total_employment": 141050,
                "annual_openings": 15700,
                "bls_url": "https://www.bls.gov/ooh/entertainment-and-sports/producers-and-directors.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 35,
                "ai_analysis": "Creative direction, storytelling vision, and managing human performers are fundamentally human tasks. AI assists with editing, effects, and scheduling but the leadership and artistic judgment of producers/directors remains irreplaceable."
            }
        ]
    },
    {
        "id": 5,
        "major": "Biology",
        "college": "School of Health & Behavioral Sciences",
        "degree": "BS",
        "description": "Multi-track program with General Biology, Pre-Health, and Environmental Biology tracks.",
        "breadth_score": 55,
        "breadth_label": "Moderate",
        "typical_outcomes": "Splits between lab and health tracks: research, biotech, pharma sales, and public health at the bachelor's level; medicine and academia via further study.",
        "careers": [
            {
                "title": "Biological Scientist",
                "bls_code": "19-1029",
                "median_salary": 87300,
                "entry_salary": 50620,
                "top_salary": 143130,
                "growth_rate": 5,
                "growth_label": "As fast as average",
                "total_employment": 93800,
                "annual_openings": 7100,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/microbiologists.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "Lab work, fieldwork, and experimental design require hands-on human skill. AI accelerates genomic analysis, drug discovery modeling, and literature review, but biological research fundamentally requires physical experimentation and creative hypothesis generation."
            },
            {
                "title": "Physician / Surgeon (with further education)",
                "grad_required": True,
                "grad_label": "Medical school (MD/DO) required",
                "bls_code": "29-1228",
                "median_salary": 229300,
                "entry_salary": 68000,
                "top_salary": 350000,
                "growth_rate": 3,
                "growth_label": "As fast as average",
                "total_employment": 821800,
                "annual_openings": 23500,
                "bls_url": "https://www.bls.gov/ooh/healthcare/physicians-and-surgeons.htm",
                "ai_impact": "Low",
                "ai_impact_score": 20,
                "ai_analysis": "While AI assists with diagnostics (radiology, pathology), the physician role involves physical examination, surgical skill, patient communication, and complex ethical decisions. Heavy regulation also protects the profession. AI is a powerful tool, not a replacement."
            }
        ]
    },
    {
        "id": 6,
        "major": "Business Economics",
        "college": "College of Arts & Sciences",
        "degree": "BS",
        "description": "Combine economic theory with business application for analytical decision-making roles.",
        "breadth_score": 80,
        "breadth_label": "Very Broad",
        "typical_outcomes": "Grads spread across banking, consulting, analytics, policy, and corporate strategy — economics reads as rigorous-generalist to nearly every employer.",
        "careers": [
            {
                "title": "Economist",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "19-3011",
                "median_salary": 115730,
                "entry_salary": 65550,
                "top_salary": 198230,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 18900,
                "annual_openings": 1300,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/economists.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI can automate data analysis and forecasting models, but economic interpretation, policy advising, and understanding complex institutional dynamics require human judgment. Economists who leverage AI for deeper analysis will have a competitive edge."
            },
            {
                "title": "Market Research Analyst",
                "bls_code": "13-1161",
                "median_salary": 74680,
                "entry_salary": 40960,
                "top_salary": 131850,
                "growth_rate": 13,
                "growth_label": "Much faster than average",
                "total_employment": 906100,
                "annual_openings": 94700,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/market-research-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "Survey design and basic data analysis are increasingly automated. However, strategic consumer insights, qualitative research, and translating data into business strategy remain human strengths. Entry-level positions face the most disruption."
            }
        ]
    },
    {
        "id": 7,
        "major": "Communication",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Develop strategic communication skills across media, public relations, and organizational contexts.",
        "breadth_score": 65,
        "breadth_label": "Broad",
        "typical_outcomes": "Feeds PR, corporate communications, media, marketing, and event roles across every industry — breadth comes from every organization needing communicators.",
        "careers": [
            {
                "title": "Public Relations Specialist",
                "bls_code": "27-3031",
                "median_salary": 67440,
                "entry_salary": 38080,
                "top_salary": 128800,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 281200,
                "annual_openings": 27300,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/public-relations-specialists.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "AI can draft press releases and social media content, but crisis management, relationship building, strategic messaging, and understanding organizational culture require human nuance. The role is shifting toward more strategic, less executional work."
            },
            {
                "title": "Technical Writer",
                "bls_code": "27-3042",
                "median_salary": 80050,
                "entry_salary": 48650,
                "top_salary": 126440,
                "growth_rate": 4,
                "growth_label": "As fast as average",
                "total_employment": 55400,
                "annual_openings": 4600,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/technical-writers.htm",
                "ai_impact": "High",
                "ai_impact_score": 75,
                "ai_analysis": "LLMs can produce technical documentation at scale. While human editors are still needed for accuracy and nuance, pure technical writing roles are among the most exposed to AI disruption. Pivoting to content strategy or UX writing offers more resilience."
            }
        ]
    },
    {
        "id": 8,
        "major": "Data Science",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Learn to extract insights from complex data using statistical methods, machine learning, and analytics.",
        "breadth_score": 85,
        "breadth_label": "Very Broad",
        "typical_outcomes": "In demand across every sector: tech, finance, healthcare, retail, sports, and government all hire data scientists and analysts from the same degree.",
        "careers": [
            {
                "title": "Data Scientist",
                "bls_code": "15-2051",
                "median_salary": 108020,
                "entry_salary": 60780,
                "top_salary": 184650,
                "growth_rate": 36,
                "growth_label": "Much faster than average",
                "total_employment": 192300,
                "annual_openings": 17700,
                "bls_url": "https://www.bls.gov/ooh/math/data-scientists.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Data scientists build and validate AI systems. While AutoML handles routine tasks, the need for problem framing, feature engineering, causal reasoning, and stakeholder communication ensures strong long-term demand."
            },
            {
                "title": "Operations Research Analyst",
                "bls_code": "15-2031",
                "median_salary": 83640,
                "entry_salary": 49550,
                "top_salary": 147050,
                "growth_rate": 23,
                "growth_label": "Much faster than average",
                "total_employment": 122900,
                "annual_openings": 11600,
                "bls_url": "https://www.bls.gov/ooh/math/operations-research-analysts.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 25,
                "ai_analysis": "OR analysts use advanced quantitative methods to help organizations solve complex problems. AI enhances but doesn't replace the need for modeling complex systems, understanding business constraints, and optimizing real-world operations."
            }
        ]
    },
    {
        "id": 9,
        "major": "Entrepreneurship",
        "college": "College of Business",
        "degree": "BS",
        "description": "Develop the skills to launch and grow ventures through innovation, business planning, and leadership.",
        "breadth_score": 70,
        "breadth_label": "Broad",
        "typical_outcomes": "By design an option-generator: grads found ventures, join startups, or take generalist business roles in product, operations, and sales.",
        "careers": [
            {
                "title": "Management Analyst / Consultant",
                "bls_code": "13-1111",
                "median_salary": 99410,
                "entry_salary": 52320,
                "top_salary": 170520,
                "growth_rate": 11,
                "growth_label": "Much faster than average",
                "total_employment": 965700,
                "annual_openings": 91300,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/management-analysts.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI can automate data gathering and basic analysis, but the consulting value proposition—client relationships, organizational change management, and creative problem-solving—remains fundamentally human. Junior analyst roles are most at risk."
            },
            {
                "title": "General / Operations Manager",
                "bls_code": "11-1021",
                "median_salary": 101280,
                "entry_salary": 45350,
                "top_salary": 210590,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 3293800,
                "annual_openings": 280100,
                "bls_url": "https://www.bls.gov/ooh/management/top-executives.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "Leadership, team motivation, strategic vision, and organizational judgment are deeply human skills. AI provides better data for decision-making but managers who can synthesize information and lead through ambiguity will be more valuable than ever."
            }
        ]
    },
    {
        "id": 10,
        "major": "Finance",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Build expertise in financial analysis, investment management, and corporate finance strategy.",
        "breadth_score": 75,
        "breadth_label": "Broad",
        "typical_outcomes": "Broad within the money economy: investment banking, wealth management, corporate finance, VC/PE, and fintech all recruit from the same degree.",
        "careers": [
            {
                "title": "Financial Analyst",
                "bls_code": "13-2051",
                "median_salary": 99890,
                "entry_salary": 57970,
                "top_salary": 176590,
                "growth_rate": 9,
                "growth_label": "Faster than average",
                "total_employment": 328600,
                "annual_openings": 27400,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/financial-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "Quantitative analysis and report generation are increasingly AI-assisted. However, relationship-driven roles like M&A advisory, client-facing wealth management, and strategic corporate finance require judgment, persuasion, and trust that AI cannot replicate."
            },
            {
                "title": "Personal Financial Advisor",
                "bls_code": "13-2052",
                "median_salary": 99580,
                "entry_salary": 46390,
                "top_salary": 208000,
                "growth_rate": 17,
                "growth_label": "Much faster than average",
                "total_employment": 263000,
                "annual_openings": 22900,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/personal-financial-advisors.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "Robo-advisors handle basic portfolio management, but holistic financial planning—estate, tax, retirement, and emotional coaching during market volatility—requires deep human empathy and trust. The advisory relationship remains the core value."
            }
        ]
    },
    {
        "id": 11,
        "major": "Financial Services",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Specialize in banking, insurance, real estate, and financial planning services.",
        "breadth_score": 45,
        "breadth_label": "Moderate",
        "typical_outcomes": "More specialized than general finance — grads concentrate in banking, insurance, and lending operations, with wealth advisory as the main branch point.",
        "careers": [
            {
                "title": "Loan Officer",
                "bls_code": "13-2072",
                "median_salary": 69990,
                "entry_salary": 36700,
                "top_salary": 144670,
                "growth_rate": 3,
                "growth_label": "As fast as average",
                "total_employment": 320400,
                "annual_openings": 28500,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/loan-officers.htm",
                "ai_impact": "High",
                "ai_impact_score": 70,
                "ai_analysis": "Automated underwriting and AI credit scoring are rapidly transforming lending. Routine mortgage and consumer lending roles face significant disruption. Commercial lending and relationship-intensive roles offer more protection."
            },
            {
                "title": "Insurance Underwriter",
                "bls_code": "13-2053",
                "median_salary": 77860,
                "entry_salary": 48640,
                "top_salary": 130430,
                "growth_rate": -6,
                "growth_label": "Decline",
                "total_employment": 113200,
                "annual_openings": 9400,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/insurance-underwriters.htm",
                "ai_impact": "High",
                "ai_impact_score": 80,
                "ai_analysis": "One of the most AI-exposed roles in finance. Automated underwriting systems are rapidly replacing routine risk assessment. Complex commercial lines and specialty insurance retain human involvement, but volume is declining."
            }
        ]
    },
    {
        "id": 12,
        "major": "Global Supply Chain Management",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Master logistics, procurement, and operations management in a global business context.",
        "breadth_score": 50,
        "breadth_label": "Moderate",
        "typical_outcomes": "Grads take logistics, procurement, and operations roles across manufacturers, retailers, and 3PLs — one function, but needed in every industry.",
        "careers": [
            {
                "title": "Logistician",
                "bls_code": "13-1081",
                "median_salary": 79400,
                "entry_salary": 48840,
                "top_salary": 128200,
                "growth_rate": 18,
                "growth_label": "Much faster than average",
                "total_employment": 208900,
                "annual_openings": 19600,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/logisticians.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI optimizes routing, inventory, and demand forecasting. But supply chain disruptions, vendor negotiations, geopolitical risk management, and crisis response require adaptive human thinking. AI is a powerful tool that amplifies logisticians' effectiveness."
            },
            {
                "title": "Purchasing Manager",
                "bls_code": "11-3061",
                "median_salary": 131350,
                "entry_salary": 73540,
                "top_salary": 205510,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 79800,
                "annual_openings": 6200,
                "bls_url": "https://www.bls.gov/ooh/management/purchasing-managers-buyers-and-purchasing-agents.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "Strategic sourcing, supplier relationship management, and contract negotiation remain human-centric. AI helps with spend analytics and market intelligence. Senior procurement roles that blend analytics with relationship management are well-positioned."
            }
        ]
    },
    {
        "id": 13,
        "major": "Healthcare Management & Strategy",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Prepare to lead healthcare organizations with business acumen and industry-specific strategy.",
        "breadth_score": 40,
        "breadth_label": "Moderate",
        "typical_outcomes": "A sector bet rather than a function bet: grads run departments, practices, and programs across a healthcare industry that is reliably growing.",
        "careers": [
            {
                "title": "Medical & Health Services Manager",
                "bls_code": "11-9111",
                "median_salary": 110680,
                "entry_salary": 67900,
                "top_salary": 209990,
                "growth_rate": 29,
                "growth_label": "Much faster than average",
                "total_employment": 562600,
                "annual_openings": 55800,
                "bls_url": "https://www.bls.gov/ooh/management/medical-and-health-services-managers.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 25,
                "ai_analysis": "Healthcare management requires navigating complex regulations, leading diverse clinical teams, and managing organizational change—all deeply human skills. AI aids operational efficiency but the aging population and regulatory complexity drive sustained demand for healthcare leaders."
            }
        ]
    },
    {
        "id": 14,
        "major": "Healthcare Informatics",
        "college": "School of Health & Behavioral Sciences",
        "degree": "BS",
        "description": "Bridge healthcare and technology by managing health data systems and analytics.",
        "breadth_score": 35,
        "breadth_label": "Focused",
        "typical_outcomes": "A deliberate niche at the intersection of health and IT — grads work in EHR systems, health data, and clinical analytics, mostly inside healthcare.",
        "careers": [
            {
                "title": "Health Information Technologist",
                "bls_code": "29-9021",
                "median_salary": 62990,
                "entry_salary": 37600,
                "top_salary": 101040,
                "growth_rate": 16,
                "growth_label": "Much faster than average",
                "total_employment": 82300,
                "annual_openings": 7800,
                "bls_url": "https://www.bls.gov/ooh/healthcare/health-information-technologists-and-medical-registrars.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "As healthcare systems adopt AI and interoperability standards, professionals who understand both clinical workflows and data systems are in high demand. This role is more of an AI implementer than an AI target."
            }
        ]
    },
    {
        "id": 15,
        "major": "Health Sciences",
        "college": "School of Health & Behavioral Sciences",
        "degree": "BS",
        "description": "Tracks in General Health Sciences, Neuroscience, and Nutrition for diverse health career paths.",
        "breadth_score": 50,
        "breadth_label": "Moderate",
        "typical_outcomes": "A springboard degree: many paths (nursing, PA, PT, nutrition, public health) but most of the high-earning ones require a graduate program.",
        "careers": [
            {
                "title": "Registered Nurse (with further education)",
                "grad_required": True,
                "grad_label": "Nursing program (BSN/ABSN) required",
                "bls_code": "29-1141",
                "median_salary": 86070,
                "entry_salary": 61250,
                "top_salary": 132680,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 3175390,
                "annual_openings": 193100,
                "bls_url": "https://www.bls.gov/ooh/healthcare/registered-nurses.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Nursing requires physical patient care, emotional support, and clinical judgment in unpredictable situations. AI assists with documentation and monitoring but cannot replace bedside care. Severe nursing shortages further protect this profession."
            },
            {
                "title": "Dietitian / Nutritionist",
                "grad_required": True,
                "grad_label": "Master's required for RD credential (since 2024)",
                "bls_code": "29-1031",
                "median_salary": 69680,
                "entry_salary": 43580,
                "top_salary": 97880,
                "growth_rate": 7,
                "growth_label": "As fast as average",
                "total_employment": 81000,
                "annual_openings": 5800,
                "bls_url": "https://www.bls.gov/ooh/healthcare/dietitians-and-nutritionists.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "Personalized nutrition counseling requires understanding individual medical histories, behavioral patterns, and motivational interviewing. AI meal-planning apps exist but lack the holistic clinical and psychological perspective of trained dietitians."
            }
        ]
    },
    {
        "id": 16,
        "major": "History",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Develop critical thinking, research, and analytical writing skills through historical study.",
        "breadth_score": 60,
        "breadth_label": "Broad",
        "typical_outcomes": "The archetypal generalist humanities degree: grads go to law school, government, education, museums, journalism, and business — strong skills, self-directed path.",
        "careers": [
            {
                "title": "Historian",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "19-3093",
                "median_salary": 68870,
                "entry_salary": 36700,
                "top_salary": 114000,
                "growth_rate": 3,
                "growth_label": "As fast as average",
                "total_employment": 3800,
                "annual_openings": 300,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/historians.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI can assist with archival research, document analysis, and pattern recognition in large datasets. But historical interpretation, contextual understanding, ethical framing of the past, and narrative construction remain deeply human. The small job market is the bigger concern."
            },
            {
                "title": "Paralegal / Legal Assistant",
                "bls_code": "23-2011",
                "median_salary": 60970,
                "entry_salary": 38250,
                "top_salary": 86640,
                "growth_rate": 4,
                "growth_label": "As fast as average",
                "total_employment": 350100,
                "annual_openings": 34600,
                "bls_url": "https://www.bls.gov/ooh/legal/paralegals-and-legal-assistants.htm",
                "ai_impact": "High",
                "ai_impact_score": 70,
                "ai_analysis": "Legal document review, contract analysis, and case research are heavily targeted by AI legal tech. Paralegals who can manage AI tools and handle complex, judgment-intensive tasks will adapt; pure research roles face significant disruption."
            }
        ]
    },
    {
        "id": 17,
        "major": "Human Resource Management",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Learn to manage talent, organizational development, and workplace strategy.",
        "breadth_score": 35,
        "breadth_label": "Focused",
        "typical_outcomes": "A defined function: grads enter recruiting, benefits, and HR generalist roles, deepening within people operations as they advance.",
        "careers": [
            {
                "title": "Human Resources Manager",
                "bls_code": "11-3121",
                "median_salary": 136350,
                "entry_salary": 81500,
                "top_salary": 232400,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 198800,
                "annual_openings": 16300,
                "bls_url": "https://www.bls.gov/ooh/management/human-resources-managers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "Resume screening and scheduling are automated, but employee relations, culture building, leadership coaching, and sensitive conflict resolution require deep emotional intelligence. Strategic HR business partners are well-protected."
            },
            {
                "title": "Compensation & Benefits Manager",
                "bls_code": "11-3111",
                "median_salary": 136154,
                "entry_salary": 79530,
                "top_salary": 224200,
                "growth_rate": 2,
                "growth_label": "Slower than average",
                "total_employment": 21400,
                "annual_openings": 1600,
                "bls_url": "https://www.bls.gov/ooh/management/compensation-and-benefits-managers.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 55,
                "ai_analysis": "Benchmarking and analytics in compensation are highly automatable. However, designing competitive total rewards strategies, managing executive compensation, and ensuring regulatory compliance in complex organizations retain human value."
            }
        ]
    },
    {
        "id": 18,
        "major": "Information Systems",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Bridge business and technology by designing and managing enterprise information systems.",
        "breadth_score": 70,
        "breadth_label": "Broad",
        "typical_outcomes": "Every company runs on systems — grads take analyst, security, IT management, and implementation roles across all industries.",
        "careers": [
            {
                "title": "Computer Systems Analyst",
                "bls_code": "15-1211",
                "median_salary": 103800,
                "entry_salary": 62060,
                "top_salary": 162470,
                "growth_rate": 10,
                "growth_label": "Faster than average",
                "total_employment": 561600,
                "annual_openings": 44900,
                "bls_url": "https://www.bls.gov/ooh/computer-and-information-technology/computer-systems-analysts.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "Systems analysts who understand both business needs and technology solutions are essential for AI implementation itself. AI code generation helps with routine tasks, but requirements gathering, stakeholder management, and system architecture remain human-driven."
            },
            {
                "title": "Information Security Analyst",
                "bls_code": "15-1212",
                "median_salary": 120360,
                "entry_salary": 67650,
                "top_salary": 193000,
                "growth_rate": 33,
                "growth_label": "Much faster than average",
                "total_employment": 175300,
                "annual_openings": 17400,
                "bls_url": "https://www.bls.gov/ooh/computer-and-information-technology/information-security-analysts.htm",
                "ai_impact": "Low",
                "ai_impact_score": 20,
                "ai_analysis": "Cybersecurity is an arms race where AI is used by both attackers and defenders. Human judgment in threat analysis, incident response, and security architecture is critical. The expanding attack surface (including AI systems themselves) drives exceptional demand."
            }
        ]
    },
    {
        "id": 19,
        "major": "International Business",
        "college": "College of Business",
        "degree": "BSIB",
        "description": "Prepare for global business careers with concentrations across business disciplines and language study.",
        "breadth_score": 70,
        "breadth_label": "Broad",
        "typical_outcomes": "Pairs business breadth with a global lens: grads land in multinationals, trade, consulting, and cross-border operations, often leveraging language skills.",
        "careers": [
            {
                "title": "Management Analyst / Consultant",
                "bls_code": "13-1111",
                "median_salary": 99410,
                "entry_salary": 52320,
                "top_salary": 170520,
                "growth_rate": 11,
                "growth_label": "Much faster than average",
                "total_employment": 965700,
                "annual_openings": 91300,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/management-analysts.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "Cross-cultural business acumen, relationship-building across borders, and understanding geopolitical risk add layers that AI cannot easily replicate. International expertise combined with analytical skills creates a strong moat."
            },
            {
                "title": "Compliance Officer",
                "bls_code": "13-1041",
                "median_salary": 75670,
                "entry_salary": 44600,
                "top_salary": 131450,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 361200,
                "annual_openings": 37800,
                "bls_url": "https://www.bls.gov/oes/current/oes131041.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 50,
                "ai_analysis": "AI helps monitor regulatory changes and flag potential violations. But interpreting ambiguous regulations, managing cross-border compliance, and building compliance culture require human judgment. Growing regulatory complexity increases demand."
            }
        ]
    },
    {
        "id": 20,
        "major": "Leadership and Innovation Management",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Develop leadership capabilities and innovation management skills for dynamic organizations.",
        "breadth_score": 60,
        "breadth_label": "Broad",
        "typical_outcomes": "A generalist management degree: grads enter rotational programs, operations, and team-lead roles — broad, but the path is what you make it.",
        "careers": [
            {
                "title": "Training & Development Manager",
                "bls_code": "11-3131",
                "median_salary": 125040,
                "entry_salary": 67370,
                "top_salary": 213200,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 42100,
                "annual_openings": 3500,
                "bls_url": "https://www.bls.gov/ooh/management/training-and-development-managers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "AI-powered learning platforms handle content delivery, but designing learning strategies, facilitating leadership development, and managing organizational change require human expertise. The need to train workforces on AI itself creates new demand."
            },
            {
                "title": "General / Operations Manager",
                "bls_code": "11-1021",
                "median_salary": 101280,
                "entry_salary": 45350,
                "top_salary": 210590,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 3293800,
                "annual_openings": 280100,
                "bls_url": "https://www.bls.gov/ooh/management/top-executives.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "Leadership is inherently human. Vision-setting, culture creation, team motivation, and navigating organizational politics cannot be automated. Leaders who effectively deploy AI will be exponentially more effective."
            }
        ]
    },
    {
        "id": 21,
        "major": "Literary and Cultural Studies",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Develop critical analysis, cultural literacy, and advanced communication skills through literary study.",
        "breadth_score": 55,
        "breadth_label": "Moderate",
        "typical_outcomes": "Writing and analysis transfer widely — grads become editors, content strategists, teachers, and marketers, though rarely via a marked pipeline.",
        "careers": [
            {
                "title": "Editor",
                "bls_code": "27-3041",
                "median_salary": 73580,
                "entry_salary": 39640,
                "top_salary": 134400,
                "growth_rate": -5,
                "growth_label": "Decline",
                "total_employment": 100000,
                "annual_openings": 10100,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/editors.htm",
                "ai_impact": "High",
                "ai_impact_score": 70,
                "ai_analysis": "AI writing tools are transforming editorial work. Basic copyediting and proofreading face heavy disruption. However, developmental editing, narrative shaping, and curating voice for brands require human sensibility. Editors who manage AI-assisted workflows will survive."
            },
            {
                "title": "Writer / Author",
                "bls_code": "27-3043",
                "median_salary": 73150,
                "entry_salary": 38250,
                "top_salary": 146120,
                "growth_rate": 4,
                "growth_label": "As fast as average",
                "total_employment": 143200,
                "annual_openings": 14200,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/writers-and-authors.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 65,
                "ai_analysis": "AI generates competent commodity content, but distinctive voice, cultural insight, investigative journalism, and deeply human storytelling maintain value. Writers who use AI to augment their process while maintaining authentic voice will differentiate themselves."
            }
        ]
    },
    {
        "id": 22,
        "major": "Marketing",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Learn consumer behavior, brand strategy, and marketing analytics for modern business.",
        "breadth_score": 70,
        "breadth_label": "Broad",
        "typical_outcomes": "Spans brand, digital, research, sales, and product marketing across every consumer and B2B industry — a function with many specializations.",
        "careers": [
            {
                "title": "Marketing Manager",
                "bls_code": "11-2021",
                "median_salary": 156580,
                "entry_salary": 78700,
                "top_salary": 239200,
                "growth_rate": 8,
                "growth_label": "Faster than average",
                "total_employment": 391050,
                "annual_openings": 34000,
                "bls_url": "https://www.bls.gov/ooh/management/advertising-promotions-and-marketing-managers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI automates ad optimization, A/B testing, and content generation. But brand strategy, creative direction, consumer empathy, and cross-functional leadership remain human domains. Marketing managers who leverage AI tools will see their impact multiply."
            },
            {
                "title": "Market Research Analyst",
                "bls_code": "13-1161",
                "median_salary": 74680,
                "entry_salary": 40960,
                "top_salary": 131850,
                "growth_rate": 13,
                "growth_label": "Much faster than average",
                "total_employment": 906100,
                "annual_openings": 94700,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/market-research-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "Survey analysis and trend spotting are increasingly AI-driven. Strategic consumer insights, qualitative research design, and translating data into actionable business recommendations remain human strengths."
            }
        ]
    },
    {
        "id": 23,
        "major": "Digital Marketing",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Specialize in data-driven digital marketing strategies including SEO, social media, and analytics.",
        "breadth_score": 50,
        "breadth_label": "Moderate",
        "typical_outcomes": "A sharper version of marketing: grads concentrate in SEO, paid media, social, and analytics roles — deep demand, narrower lane.",
        "careers": [
            {
                "title": "Advertising & Promotions Manager",
                "bls_code": "11-2011",
                "median_salary": 131870,
                "entry_salary": 62530,
                "top_salary": 208000,
                "growth_rate": 8,
                "growth_label": "Faster than average",
                "total_employment": 24000,
                "annual_openings": 2100,
                "bls_url": "https://www.bls.gov/ooh/management/advertising-promotions-and-marketing-managers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 50,
                "ai_analysis": "Programmatic advertising is already heavily automated. AI generates ad copy and optimizes campaigns. But creative strategy, brand storytelling, and understanding cultural moments require human intuition. The tools change; the strategic need persists."
            },
            {
                "title": "SEO / Digital Marketing Specialist",
                "bls_code": "13-1161",
                "median_salary": 74680,
                "entry_salary": 40960,
                "top_salary": 131850,
                "growth_rate": 13,
                "growth_label": "Much faster than average",
                "total_employment": 906100,
                "annual_openings": 94700,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/market-research-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "AI search (like Google SGE) is transforming SEO. Content generation and basic analytics are automated. Specialists who pivot to AI-search optimization, multi-platform strategy, and creative content that resonates emotionally will thrive."
            }
        ]
    },
    {
        "id": 24,
        "major": "Politics and Law",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Study political systems, legal theory, and public policy to prepare for law, government, or advocacy careers.",
        "breadth_score": 55,
        "breadth_label": "Moderate",
        "typical_outcomes": "Feeds law school, government, campaigns, and policy work — real breadth, but the highest-earning branches run through a JD.",
        "careers": [
            {
                "title": "Lawyer (with further education)",
                "grad_required": True,
                "grad_label": "Law school (JD) required",
                "bls_code": "23-1011",
                "median_salary": 145760,
                "entry_salary": 67490,
                "top_salary": 239200,
                "growth_rate": 8,
                "growth_label": "Faster than average",
                "total_employment": 813000,
                "annual_openings": 39800,
                "bls_url": "https://www.bls.gov/ooh/legal/lawyers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 45,
                "ai_analysis": "AI transforms legal research, document review, and contract drafting. But courtroom advocacy, client counseling, negotiation, and navigating novel legal questions require human judgment. Lawyers who integrate AI tools will be dramatically more productive."
            },
            {
                "title": "Political Scientist",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "19-3094",
                "median_salary": 132820,
                "entry_salary": 64500,
                "top_salary": 177990,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 7300,
                "annual_openings": 600,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/political-scientists.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "AI aids quantitative political analysis, but understanding political dynamics, institutional behavior, and advising on policy require deep contextual knowledge. Very small field—competition, not AI, is the bigger challenge."
            }
        ]
    },
    {
        "id": 25,
        "major": "Psychology",
        "college": "School of Health & Behavioral Sciences",
        "degree": "BS",
        "description": "Understand human behavior through scientific study, preparing for clinical, research, or business roles.",
        "breadth_score": 65,
        "breadth_label": "Broad",
        "typical_outcomes": "At the bachelor's level grads fan out into HR, UX research, sales, and social services; clinical practice requires the doctoral branch.",
        "careers": [
            {
                "title": "Clinical Psychologist (with further education)",
                "grad_required": True,
                "grad_label": "Doctorate (PhD/PsyD) required",
                "bls_code": "19-3031",
                "median_salary": 92740,
                "entry_salary": 51570,
                "top_salary": 144860,
                "growth_rate": 11,
                "growth_label": "Much faster than average",
                "total_employment": 198100,
                "annual_openings": 12800,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/psychologists.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Therapy is fundamentally relational. While AI chatbots offer basic mental health support, the therapeutic alliance, complex trauma work, and nuanced clinical judgment are irreplaceable. Growing mental health awareness drives strong demand."
            },
            {
                "title": "Industrial-Organizational Psychologist",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "19-3032",
                "median_salary": 147750,
                "entry_salary": 76250,
                "top_salary": 210030,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 1900,
                "annual_openings": 100,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/psychologists.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 30,
                "ai_analysis": "Understanding human behavior in organizations—motivation, team dynamics, leadership development—requires deep human expertise. AI helps with employee surveys and analytics, but designing interventions requires psychological insight."
            }
        ]
    },
    {
        "id": 26,
        "major": "Sociology and Anthropology",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Explore perspectives on people, society, and culture for a critical understanding of our global community.",
        "breadth_score": 55,
        "breadth_label": "Moderate",
        "typical_outcomes": "Grads take research, community services, HR, and market-insight roles — transferable analytical skills without a single marked pipeline.",
        "careers": [
            {
                "title": "Social & Community Service Manager",
                "bls_code": "11-9151",
                "median_salary": 77030,
                "entry_salary": 46900,
                "top_salary": 118650,
                "growth_rate": 9,
                "growth_label": "Faster than average",
                "total_employment": 192300,
                "annual_openings": 16600,
                "bls_url": "https://www.bls.gov/ooh/management/social-and-community-service-managers.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Community service requires empathy, cultural competence, and relationship-building with vulnerable populations. AI can assist with program management and data tracking but the human connection is the core of this work."
            },
            {
                "title": "Survey Researcher",
                "grad_required": True,
                "grad_label": "Master's degree typically required",
                "bls_code": "19-3022",
                "median_salary": 60960,
                "entry_salary": 36410,
                "top_salary": 102380,
                "growth_rate": 5,
                "growth_label": "As fast as average",
                "total_employment": 15800,
                "annual_openings": 1400,
                "bls_url": "https://www.bls.gov/ooh/life-physical-and-social-science/survey-researchers.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "AI automates survey distribution and basic analysis. Designing methodologically sound research, interpreting qualitative data, and understanding social context remain human tasks, but the field is small and routine work is vulnerable."
            }
        ]
    },
    {
        "id": 27,
        "major": "Spanish",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Develop advanced Spanish proficiency and cultural understanding for global career success.",
        "breadth_score": 40,
        "breadth_label": "Moderate",
        "typical_outcomes": "Usually strongest as a multiplier on another field — grads work in translation, education, and international business, often pairing the language with a second skill.",
        "careers": [
            {
                "title": "Interpreter / Translator",
                "bls_code": "27-3091",
                "median_salary": 57090,
                "entry_salary": 35240,
                "top_salary": 98230,
                "growth_rate": 4,
                "growth_label": "As fast as average",
                "total_employment": 70400,
                "annual_openings": 9200,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/interpreters-and-translators.htm",
                "ai_impact": "High",
                "ai_impact_score": 75,
                "ai_analysis": "Machine translation has improved dramatically. Routine document translation faces heavy disruption. However, simultaneous interpreting, legal/medical interpretation, literary translation, and culturally sensitive communication still benefit from human expertise."
            },
            {
                "title": "Foreign Language Teacher (Post-secondary)",
                "grad_required": True,
                "grad_label": "Master's or PhD typically required",
                "bls_code": "25-1124",
                "median_salary": 75810,
                "entry_salary": 41590,
                "top_salary": 122260,
                "growth_rate": 4,
                "growth_label": "As fast as average",
                "total_employment": 29500,
                "annual_openings": 2500,
                "bls_url": "https://www.bls.gov/ooh/education-training-and-library/postsecondary-teachers.htm",
                "ai_impact": "Low-Medium",
                "ai_impact_score": 35,
                "ai_analysis": "AI language tutors complement but don't replace classroom instruction. Cultural immersion, conversation practice with feedback, and mentoring remain human strengths. Enrollment trends in language departments are the bigger risk factor."
            }
        ]
    },
    {
        "id": 28,
        "major": "Sports Industries, Media and Promotion",
        "college": "College of Arts & Sciences",
        "degree": "BA",
        "description": "Take a multifaceted look at the global sports phenomenon through media, business, and culture.",
        "breadth_score": 30,
        "breadth_label": "Focused",
        "typical_outcomes": "A passion-industry bet: grads compete for agency, media, and team-front-office roles inside a single, crowded sector.",
        "careers": [
            {
                "title": "Sports Agent / Promoter",
                "bls_code": "13-1011",
                "median_salary": 78860,
                "entry_salary": 40640,
                "top_salary": 174810,
                "growth_rate": 7,
                "growth_label": "As fast as average",
                "total_employment": 95200,
                "annual_openings": 11200,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/agents-and-business-managers.htm",
                "ai_impact": "Low",
                "ai_impact_score": 20,
                "ai_analysis": "Sports agency is relationship-driven—negotiation, trust-building, and understanding athlete psychology are fundamentally human. AI helps with contract analytics and market data, but the dealmaking is personal."
            },
            {
                "title": "Broadcast Analyst / Sports Reporter",
                "bls_code": "27-3023",
                "median_salary": 55960,
                "entry_salary": 28040,
                "top_salary": 125740,
                "growth_rate": -3,
                "growth_label": "Decline",
                "total_employment": 53200,
                "annual_openings": 5200,
                "bls_url": "https://www.bls.gov/ooh/media-and-communication/reporters-correspondents-and-broadcast-news-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 65,
                "ai_analysis": "AI generates game recaps and statistical analysis at scale. But live commentary, interviewing, investigative sports journalism, and building audience trust through personality remain human domains. The industry is contracting due to media fragmentation."
            }
        ]
    },
    {
        "id": 29,
        "major": "Exercise and Movement Science",
        "college": "School of Health & Behavioral Sciences",
        "degree": "BS",
        "description": "Study human movement and exercise science with tracks in Applied Exercise/Coaching and Healthcare Provider Prep.",
        "breadth_score": 30,
        "breadth_label": "Focused",
        "typical_outcomes": "A focused clinical-prep track: grads become trainers and exercise physiologists or continue to PT/OT school — mostly within health and fitness.",
        "careers": [
            {
                "title": "Exercise Physiologist",
                "bls_code": "29-1128",
                "median_salary": 53860,
                "entry_salary": 38060,
                "top_salary": 79700,
                "growth_rate": 11,
                "growth_label": "Much faster than average",
                "total_employment": 14300,
                "annual_openings": 900,
                "bls_url": "https://www.bls.gov/ooh/healthcare/exercise-physiologists.htm",
                "ai_impact": "Low",
                "ai_impact_score": 15,
                "ai_analysis": "Hands-on physical assessment, exercise prescription, and patient motivation require in-person human interaction. Wearable tech and AI fitness apps complement but cannot replace clinical expertise in rehabilitation and chronic disease management."
            },
            {
                "title": "Athletic Trainer",
                "grad_required": True,
                "grad_label": "Master's degree required",
                "bls_code": "29-9091",
                "median_salary": 56420,
                "entry_salary": 37180,
                "top_salary": 76780,
                "growth_rate": 14,
                "growth_label": "Much faster than average",
                "total_employment": 35700,
                "annual_openings": 3000,
                "bls_url": "https://www.bls.gov/ooh/healthcare/athletic-trainers.htm",
                "ai_impact": "Low",
                "ai_impact_score": 10,
                "ai_analysis": "Requires hands-on injury assessment, rehabilitation, and emergency response. AI may help with performance analytics and injury prediction, but physical care and athlete relationships are irreplaceable."
            }
        ]
    },
    {
        "id": 30,
        "major": "Team and Project Management",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Master the skills to lead teams and manage complex projects across industries.",
        "breadth_score": 65,
        "breadth_label": "Broad",
        "typical_outcomes": "Project managers are needed in construction, tech, healthcare, and finance alike — one skill set, hireable nearly everywhere.",
        "careers": [
            {
                "title": "Project Management Specialist",
                "bls_code": "13-1082",
                "median_salary": 98580,
                "entry_salary": 53440,
                "top_salary": 166430,
                "growth_rate": 6,
                "growth_label": "As fast as average",
                "total_employment": 976800,
                "annual_openings": 68100,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/project-management-specialists.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "AI handles scheduling, risk modeling, and status reporting. But managing stakeholder expectations, navigating organizational politics, motivating teams through challenges, and making judgment calls under uncertainty are deeply human skills."
            }
        ]
    },
    {
        "id": 31,
        "major": "Managerial Accounting and Finance",
        "college": "College of Business",
        "degree": "BSBA",
        "description": "Combine accounting expertise with financial analysis for strategic business decision-making roles.",
        "breadth_score": 55,
        "breadth_label": "Moderate",
        "typical_outcomes": "Broader than pure accounting: grads move between corporate accounting, FP&A, and finance manager tracks inside companies of every kind.",
        "careers": [
            {
                "title": "Financial Manager",
                "bls_code": "11-3031",
                "median_salary": 156100,
                "entry_salary": 81590,
                "top_salary": 239200,
                "growth_rate": 17,
                "growth_label": "Much faster than average",
                "total_employment": 734800,
                "annual_openings": 66700,
                "bls_url": "https://www.bls.gov/ooh/management/financial-managers.htm",
                "ai_impact": "Medium",
                "ai_impact_score": 40,
                "ai_analysis": "Financial managers who set strategy, manage capital allocation, and lead teams are well-protected. AI enhances forecasting and reporting, making managers more effective. The combination of accounting + finance + leadership creates a strong value proposition."
            },
            {
                "title": "Budget Analyst",
                "bls_code": "13-2031",
                "median_salary": 84940,
                "entry_salary": 53290,
                "top_salary": 129300,
                "growth_rate": 3,
                "growth_label": "As fast as average",
                "total_employment": 49000,
                "annual_openings": 4100,
                "bls_url": "https://www.bls.gov/ooh/business-and-financial/budget-analysts.htm",
                "ai_impact": "Medium-High",
                "ai_impact_score": 60,
                "ai_analysis": "Routine budget tracking and variance analysis are highly automatable. Budget analysts who focus on strategic financial planning, cross-functional collaboration, and scenario analysis will retain value. Pure spreadsheet work is at risk."
            }
        ]
    }
]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/methodology')
def methodology():
    """Transparency page explaining how AI impact scores are derived."""
    all_careers = []
    for m in MAJORS_DATA:
        for c in m['careers']:
            all_careers.append({
                'major': m['major'],
                'career': c['title'],
                'ai_impact': c['ai_impact'],
                'ai_impact_score': c['ai_impact_score'],
                'median_salary': c['median_salary'],
                'growth_rate': c['growth_rate'],
            })

    bands = [
        ('Low', 0, 25),
        ('Low-Medium', 26, 40),
        ('Medium', 41, 55),
        ('Medium-High', 56, 70),
        ('High', 71, 100),
    ]

    distribution = []
    total = len(all_careers)
    for label, lo, hi in bands:
        members = [c for c in all_careers if lo <= c['ai_impact_score'] <= hi]
        distribution.append({
            'label': label,
            'range': f'{lo}\u2013{hi}',
            'count': len(members),
            'pct': round(100 * len(members) / total, 1) if total else 0,
            'examples': sorted(members, key=lambda c: c['ai_impact_score'])[:4],
        })

    most_resilient = sorted(all_careers, key=lambda c: c['ai_impact_score'])[:8]
    most_exposed = sorted(all_careers, key=lambda c: -c['ai_impact_score'])[:8]

    return render_template(
        'methodology.html',
        distribution=distribution,
        total_careers=total,
        total_majors=len(MAJORS_DATA),
        most_resilient=most_resilient,
        most_exposed=most_exposed,
    )


@app.route('/api/majors')
def get_majors():
    college = request.args.get('college', '')
    sort_by = request.args.get('sort', '')
    ai_filter = request.args.get('ai_impact', '')
    education = request.args.get('education', '')

    filtered = MAJORS_DATA

    if college:
        filtered = [m for m in filtered if m['college'] == college]

    if education == 'bachelors':
        # Keep only careers reachable with a bachelor's; drop majors with none left
        filtered = [
            {**m, 'careers': [c for c in m['careers'] if not c.get('grad_required')]}
            for m in filtered
        ]
        filtered = [m for m in filtered if m['careers']]

    if ai_filter:
        ranges = {
            'low': (0, 25),
            'low-medium': (26, 40),
            'medium': (41, 55),
            'medium-high': (56, 70),
            'high': (71, 100)
        }
        if ai_filter in ranges:
            lo, hi = ranges[ai_filter]
            filtered = [m for m in filtered if any(
                lo <= c['ai_impact_score'] <= hi for c in m['careers']
            )]

    if sort_by == 'salary_high':
        filtered = sorted(filtered, key=lambda m: max(c['median_salary'] for c in m['careers']), reverse=True)
    elif sort_by == 'salary_low':
        filtered = sorted(filtered, key=lambda m: max(c['median_salary'] for c in m['careers']))
    elif sort_by == 'growth':
        filtered = sorted(filtered, key=lambda m: max(c['growth_rate'] for c in m['careers']), reverse=True)
    elif sort_by == 'ai_safe':
        filtered = sorted(filtered, key=lambda m: min(c['ai_impact_score'] for c in m['careers']))
    elif sort_by == 'ai_risk':
        filtered = sorted(filtered, key=lambda m: max(c['ai_impact_score'] for c in m['careers']), reverse=True)
    elif sort_by == 'breadth':
        filtered = sorted(filtered, key=lambda m: m['breadth_score'], reverse=True)
    elif sort_by == 'name':
        filtered = sorted(filtered, key=lambda m: m['major'])

    return jsonify(filtered)


@app.route('/api/compare')
def compare():
    ids = request.args.getlist('ids', type=int)
    if not ids:
        return jsonify([])
    result = [m for m in MAJORS_DATA if m['id'] in ids]
    return jsonify(result)


@app.route('/api/stats')
def stats():
    all_careers = []
    for m in MAJORS_DATA:
        for c in m['careers']:
            all_careers.append({
                'major': m['major'],
                'career': c['title'],
                'median_salary': c['median_salary'],
                'growth_rate': c['growth_rate'],
                'ai_impact_score': c['ai_impact_score'],
                'ai_impact': c['ai_impact'],
                'grad_required': c.get('grad_required', False)
            })

    avg_salary = sum(c['median_salary'] for c in all_careers) / len(all_careers)
    avg_growth = sum(c['growth_rate'] for c in all_careers) / len(all_careers)
    avg_ai = sum(c['ai_impact_score'] for c in all_careers) / len(all_careers)

    return jsonify({
        'total_majors': len(MAJORS_DATA),
        'total_careers': len(all_careers),
        'avg_salary': round(avg_salary),
        'avg_growth': round(avg_growth, 1),
        'avg_ai_score': round(avg_ai, 1),
        'all_careers': all_careers
    })


if __name__ == '__main__':
    # Port 5000 is taken by macOS AirPlay Receiver (Control Center), which
    # answers 403 on IPv6 localhost even when Flask is bound on IPv4.
    app.run(debug=True, port=5001)
