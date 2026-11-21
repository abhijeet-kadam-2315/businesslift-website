#!/usr/bin/env python3
"""
BusinessLift — build.py  (OPTIONAL page generator)

The website is plain static HTML/CSS/JS and does NOT need this script to run.
It exists so the shared header, footer and metadata stay identical across all
pages. Edit content here, then run:   python3 build.py

It regenerates: all *.html pages, sitemap.xml and robots.txt.
Standard library only (Python 3.8+).
"""
import html
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Site settings — change BASE_URL to your real domain before launch
# ----------------------------------------------------------------------------
SITE = {
    "name": "BusinessLift",
    "tagline": "Lift Your Business. Grow Your Brand.",
    "base": "https://www.your-domain.com",   # <-- replace with real domain (no trailing slash)
    "phone": "+91 9284569706",
    "tel": "+919284569706",
    "email": "kadamabhijeet2315@gmail.com",
    "wa": "https://wa.me/919284569706",
}

e = lambda s: html.escape(s, quote=True)

NAV = [
    ("index.html", "Home", "home"),
    ("about.html", "About", "about"),
    ("services.html", "Services", "services"),
    ("industries.html", "Industries", "industries"),
    ("portfolio.html", "Our Work", "portfolio"),
    ("pricing.html", "Pricing", "pricing"),
    ("blog.html", "Blog", "blog"),
    ("contact.html", "Contact", "contact"),
]

# ----------------------------------------------------------------------------
# Icons (inline SVG paths, 24x24 stroke icons)
# ----------------------------------------------------------------------------
ICONS = {
    "pin": '<path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "share": '<circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="m8.2 10.8 7.6-3.6M8.2 13.2l7.6 3.6"/>',
    "layout": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 20V9"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2"/>',
    "funnel": '<path d="M3 5h18l-7 8v6l-4-2v-4z"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="m16 10 5-3v10l-5-3z"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "palette": '<path d="M12 3a9 9 0 1 0 0 18c1.1 0 1.8-.9 1.5-1.9-.3-1 .4-2.1 1.5-2.1H17a4 4 0 0 0 4-4c0-5-4-10-9-10z"/><circle cx="7.5" cy="11" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="15" cy="7.5" r="1"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    "chat": '<path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 20.5l1.7-5.4A8.5 8.5 0 1 1 21 11.5z"/><path d="M8.5 11.5h.01M12 11.5h.01M15.5 11.5h.01"/>',
    "chart": '<path d="M4 20V4M4 20h16M8 16v-5M13 16V8M18 16v-9"/>',
    "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>',
    "refresh": '<path d="M20 11a8 8 0 0 0-14-4.5L4 9M4 5v4h4M4 13a8 8 0 0 0 14 4.5L20 15M20 19v-4h-4"/>',
    "bed": '<path d="M3 18V7M3 14h18v4M21 14v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="11" r="1.6"/>',
    "heart": '<path d="M12 20s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 9c0 6-8 11-8 11z"/>',
    "briefcase": '<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
    "home": '<path d="m3 11 9-8 9 8"/><path d="M5 10v10h14V10M10 20v-5h4v5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "bag": '<path d="M5 8h14l-1 12H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "cart": '<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M3 4h2.5l2.2 11h10.5L20 8H6.5"/>',
    "cap": '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-4.5"/>',
    "factory": '<path d="M3 20V9l6 4V9l6 4V5h3v15z"/>',
    "store": '<path d="M4 9 5.5 4h13L20 9a3 3 0 0 1-5.3 1.9 3 3 0 0 1-5.4 0A3 3 0 0 1 4 9z"/><path d="M5 12v8h14v-8"/>',
    "rocket": '<path d="M5 15c-1.5 1.5-2 5-2 5s3.5-.5 5-2"/><path d="M12 15 9 12c1-4 4-8 11-9 0 7-4 10-8 12z"/><circle cx="15" cy="9" r="1.2"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "doc": '<path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M16 5.2a3.2 3.2 0 0 1 0 5.6M18 14.3c1.8.8 3 2.6 3 4.7"/>',
}


def icon(name, size=24, cls="icon"):
    return ('<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (cls, size, size, ICONS[name]))


# ----------------------------------------------------------------------------
# Content data
# ----------------------------------------------------------------------------
SERVICES = [
    {
        "slug": "google-business-profile", "title": "Google Business Profile Management", "icon": "pin", "wa": "gbp",
        "short": "Keep your local listing accurate, active and ready for customers who find you on Google Search and Maps.",
        "intro": "A complete, up-to-date profile is often the first thing a nearby customer sees. We keep yours accurate and active.",
        "what": "We review and optimise your Google Business Profile so customers see correct, complete and current information when they find you on Search and Maps. Ongoing management keeps the listing active instead of leaving it as a one-time set-up.",
        "who": "Clinics, restaurants and hotels, retail stores, CA and professional offices, solar installers and any business that serves customers in a specific area.",
        "deliverables": ["Profile audit and optimisation (categories, description, services, attributes)", "Business information and opening-hours updates", "Regular post creation and publishing", "Photo and logo management", "Review-response guidance with reply drafts", "Periodic performance monitoring using Google's own insights"],
        "objectives": ["More accurate and trustworthy local listings", "Better local discovery on Search and Maps", "More calls, direction requests and website visits", "A responsive, credible public presence"],
        "note": "Google decides how profiles are displayed. We do not promise specific ranking positions.",
    },
    {
        "slug": "seo", "title": "Search Engine Optimization (SEO)", "icon": "search", "wa": "seo",
        "short": "Help the right people find your website through practical on-page, technical and local SEO.",
        "intro": "Sustainable visibility starts with a website that search engines can understand and people want to use.",
        "what": "We study how your customers search, then improve your site's content, structure and technical health so it can be found for relevant queries. For location-based businesses we also strengthen local search signals.",
        "who": "Businesses with a website that want steadier, relevant organic traffic: professional firms, schools and colleges, e-commerce stores, manufacturers and service providers.",
        "deliverables": ["Keyword and search-intent research", "On-page optimisation (titles, headings, content, internal links)", "Technical SEO checks (speed, mobile usability, indexing, structure)", "Local SEO recommendations", "Content recommendations and topic ideas", "Performance monitoring and reporting"],
        "objectives": ["Improve relevant organic visibility over time", "Attract more qualified website visitors", "Fix technical issues that hold a site back", "Build content that answers customer questions"],
        "note": "SEO takes time and results depend on competition and search-engine behaviour. We do not guarantee rankings.",
    },
    {
        "slug": "social-media-management", "title": "Social Media Management", "icon": "share", "wa": "social",
        "short": "Plan, create and publish consistent content that keeps your brand visible and engages your audience.",
        "intro": "A steady, well-planned social presence builds familiarity and trust with the people you want to reach.",
        "what": "We plan a content calendar around your offers, audience and brand voice, then create and coordinate publishing across the platforms that make sense for your business. We also guide how to handle comments and messages.",
        "who": "Restaurants and hotels, clinics, retailers, educational institutions, real estate businesses and startups that want a consistent presence without managing it day to day.",
        "deliverables": ["Monthly content calendar", "Post design and creative direction", "Caption writing", "Publishing coordination", "Engagement and comment-handling guidance", "Regular performance reporting"],
        "objectives": ["Consistent brand visibility", "Higher audience engagement", "Stronger brand recall and credibility", "Support for offers, events and launches"],
        "note": "",
    },
    {
        "slug": "website-design-management", "title": "Website Design & Management", "icon": "layout", "wa": "website",
        "short": "Responsive websites and landing pages built to look credible and turn visits into enquiries.",
        "intro": "Your website is your most important marketing asset. We design it well, then help you keep it healthy.",
        "what": "We design responsive, easy-to-navigate websites and landing pages with clear calls to action. After launch, we can continue to manage content, updates and improvements. Website design and website management are separate scopes.",
        "who": "New businesses needing a first website, established businesses with an outdated site, and anyone running campaigns who needs focused landing pages.",
        "deliverables": ["Responsive website or landing page design", "Page structure and content guidance", "Enquiry forms and click-to-call / WhatsApp buttons", "User experience improvements", "Basic on-page SEO set-up", "Ongoing content updates and maintenance (separate plan)"],
        "objectives": ["A credible, professional online presence", "Clear paths for visitors to enquire", "A site that works well on mobile", "A reliable base for SEO and advertising"],
        "note": "",
        "extra": "web",
    },
    {
        "slug": "google-ads-meta-ads", "title": "Google Ads & Meta Ads Management", "icon": "target", "wa": "ads",
        "short": "Plan, launch and optimise paid campaigns on Google and Meta to reach people who are ready to act.",
        "intro": "Paid advertising can bring quick visibility when it is planned around a clear goal and tracked carefully.",
        "what": "We define campaign goals, research audiences, set up campaigns, coordinate the ad creatives, and optimise based on the data available. You see what is working and what we are changing.",
        "who": "Businesses that want to promote specific offers, services or products to a defined audience: real estate, solar, healthcare, education, retail and e-commerce.",
        "deliverables": ["Campaign planning and goal setting", "Audience and keyword research", "Campaign set-up and tracking set-up", "Ad creative and copy coordination", "Ongoing optimisation", "Regular reporting with recommendations"],
        "objectives": ["Reach relevant audiences quickly", "Generate enquiries and website visits", "Promote offers and launches", "Learn which messages and channels work best"],
        "note": "Advertising spend is paid to the platforms and is separate from our management fee, unless a specific quotation clearly states otherwise.",
    },
    {
        "slug": "lead-generation", "title": "Lead Generation", "icon": "funnel", "wa": "leads",
        "short": "Build a clear path from first click to enquiry, with forms, landing pages and lead tracking.",
        "intro": "More traffic only helps when visitors can easily become enquiries. We focus on that path.",
        "what": "We design the journey that turns interest into enquiries: campaign strategy, focused landing pages, simple enquiry forms and a way to track where each lead came from, then improve conversion step by step.",
        "who": "Businesses that depend on enquiries or appointments: clinics, real estate, solar and renewable energy, education, professional services and local service providers.",
        "deliverables": ["Lead-generation strategy", "Landing page recommendations or design", "Enquiry form and call-to-action set-up", "Lead tracking set-up", "Conversion improvement suggestions", "Enquiry reporting"],
        "objectives": ["Capture more qualified enquiries", "Understand which channels bring leads", "Reduce drop-off in the enquiry journey", "Support your sales follow-up process"],
        "note": "We do not guarantee lead volume, lead quality or sales. Results depend on your market, offer, budget and follow-up.",
    },
    {
        "slug": "reel-video-editing", "title": "Reel & Video Editing", "icon": "video", "wa": "video",
        "short": "Scroll-stopping short-form videos with clean edits, subtitles and platform-ready formats.",
        "intro": "Short video is now a core way customers discover brands. We make your footage look polished and purposeful.",
        "what": "You provide the footage; we turn it into edited reels, shorts and promotional videos with pacing, transitions, music suggestions and subtitles, formatted for each platform.",
        "who": "Restaurants and hotels, clinics, retailers, real estate agents, trainers, educators and any brand producing regular video content.",
        "deliverables": ["Short-form reel editing", "Subtitles and captions", "Transitions and basic motion graphics", "Promotional and explainer video edits", "Social media format versions (vertical, square)", "Thumbnail and cover suggestions"],
        "objectives": ["Higher engagement on social platforms", "Professional brand presentation", "Clear promotion of offers and services", "Repurposing one shoot into many posts"],
        "note": "",
    },
    {
        "slug": "graphic-design-flyers", "title": "Graphic Design & Flyer Design", "icon": "pen", "wa": "design",
        "short": "Promotional creatives, flyers, brochures and social designs that look consistent and professional.",
        "intro": "Good design makes your message quicker to understand and easier to trust.",
        "what": "We design promotional materials for print and digital use, keeping your brand colours, fonts and tone consistent so every piece looks like it comes from the same business.",
        "who": "Retail stores, restaurants, schools and coaching classes, events, real estate projects and any business running offers or campaigns.",
        "deliverables": ["Flyers and posters", "Brochures and catalogues", "Social media post and story designs", "Campaign and ad visuals", "Print-ready and web-ready files", "Editable template sets"],
        "objectives": ["Clear, attractive promotions", "Consistent brand look across channels", "Faster production of recurring creatives", "Materials ready for print and digital"],
        "note": "",
    },
    {
        "slug": "branding-logo-design", "title": "Branding & Logo Design", "icon": "palette", "wa": "branding",
        "short": "Logo concepts and brand identity systems that help your business look and feel distinct.",
        "intro": "A clear identity helps customers recognise, remember and trust your business.",
        "what": "We explore your positioning and audience, then develop logo concepts and a simple identity system: colours, typography and usage rules, so your brand stays consistent as you grow.",
        "who": "Startups, new businesses, businesses refreshing an outdated look and growing companies that need a more consistent identity.",
        "deliverables": ["Logo concepts and refinement", "Colour palette", "Typography selection", "Brand guideline document", "Social media profile and cover assets", "Logo files in common formats"],
        "objectives": ["A distinctive, memorable identity", "Consistency across print and digital", "Greater perceived credibility", "A foundation for future marketing"],
        "note": "",
    },
    {
        "slug": "digital-marketing-strategy", "title": "Digital Marketing Strategy & Consulting", "icon": "compass", "wa": "strategy",
        "short": "A clear, practical plan: audit, competitor insight, channel selection and performance review.",
        "intro": "Before spending on tools or ads, it helps to know where you stand and where to focus.",
        "what": "We audit your current digital presence, look at what competitors are doing, and recommend which channels and activities suit your goals and budget. We can also review performance and refine the plan.",
        "who": "Business owners unsure where to start, teams whose marketing feels scattered, and businesses planning a new launch or expansion.",
        "deliverables": ["Digital presence audit", "Competitor research", "Marketing plan with priorities", "Channel and budget recommendations", "Measurement framework", "Periodic performance review"],
        "objectives": ["Clarity on priorities", "Smarter use of marketing budget", "A roadmap your team can follow", "Better measurement of what works"],
        "note": "",
    },
]

PRINCIPLES = [
    ("compass", "Strategy Before Execution", "We start with your goals and audience, so activity is planned rather than random."),
    ("target", "Solutions Built Around Business Goals", "Every recommendation connects back to what your business actually needs to achieve."),
    ("chart", "Creative and Data-Informed Decisions", "Good creative ideas, checked against the data available to us."),
    ("chat", "Transparent Communication", "Clear scope, clear updates and honest answers about what is and isn't working."),
    ("refresh", "Consistent Optimization", "Marketing improves with attention. We review and refine rather than set and forget."),
    ("shield", "Focus on Qualified Enquiries and Sustainable Growth", "We aim for relevant enquiries and steady progress, not vanity numbers or empty promises."),
]

PROCESS = [
    ("01", "Discover", "Understand the business, target audience, goals, and challenges."),
    ("02", "Strategize", "Develop a practical marketing strategy based on the business's needs."),
    ("03", "Execute", "Implement the selected marketing activities and campaigns."),
    ("04", "Measure", "Track available performance indicators and identify opportunities."),
    ("05", "Improve", "Refine the strategy based on actual performance and feedback."),
]

INDUSTRIES = [
    {"slug": "hotels-restaurants", "title": "Hotels & Restaurants", "home": "Hospitality", "icon": "bed",
     "short": "Show up on Google Maps, share food and ambience through reels, and make enquiries and bookings easy.",
     "intro": "Guests choose where to eat and stay largely on what they see online: photos, reviews, menus and location details.",
     "opps": ["Keep Google Business Profile details, photos and menus current", "Short reels and photo content that show the experience", "Local ads for events, festivals and seasonal offers"],
     "services": ["Google Business Profile", "Social Media", "Reel & Video Editing", "Graphic Design", "Meta Ads"], "wa": "social"},
    {"slug": "doctors-clinics", "title": "Doctors & Clinics", "home": "Healthcare", "icon": "heart",
     "short": "Build trust with clear information, accurate listings and a simple way for patients to get in touch.",
     "intro": "Patients look for credibility and clarity. Marketing for healthcare should be informative, respectful and compliant with applicable advertising rules.",
     "opps": ["Accurate local listings with services, timings and directions", "Educational content that answers common patient questions", "A clean website with easy appointment enquiry"],
     "services": ["Google Business Profile", "SEO", "Website Design", "Social Media", "Lead Generation"], "wa": "gbp"},
    {"slug": "ca-professional-services", "title": "CA Firms & Professional Services", "home": "Professional Services", "icon": "briefcase",
     "short": "Position your expertise clearly with a credible website, local search presence and helpful content.",
     "intro": "Clients choose advisers they trust. Your online presence should reflect professionalism and make your services easy to understand.",
     "opps": ["A credible website explaining services and process", "Local SEO so nearby clients find you", "Helpful articles around tax, compliance and deadlines"],
     "services": ["Website Design", "SEO", "Google Business Profile", "Branding", "Content Strategy"], "wa": "website"},
    {"slug": "real-estate", "title": "Real Estate", "home": "Real Estate", "icon": "home",
     "short": "Present projects attractively and capture buyer enquiries through targeted campaigns and landing pages.",
     "intro": "Property decisions are high-value and research-heavy. Buyers compare many options online before they call.",
     "opps": ["Project landing pages with clear enquiry forms", "Targeted Google and Meta campaigns for specific locations", "Brochures, walkthrough reels and site-visit creatives"],
     "services": ["Lead Generation", "Google & Meta Ads", "Landing Pages", "Video Editing", "Graphic Design"], "wa": "leads"},
    {"slug": "solar-renewable-energy", "title": "Solar & Renewable Energy", "home": "Solar & Renewable Energy", "icon": "sun",
     "short": "Explain savings and installation clearly, and reach homeowners and businesses actively researching solar.",
     "intro": "Customers want to understand costs, subsidies and reliability before choosing an installer. Clear, trustworthy information helps.",
     "opps": ["Explainer content on how solar works and what to expect", "Search and social campaigns aimed at local enquiries", "Showcasing completed installations with permission"],
     "services": ["Lead Generation", "Google Ads", "SEO", "Website Design", "Social Media"], "wa": "ads"},
    {"slug": "retail", "title": "Retail Businesses", "home": "Retail & E-commerce", "icon": "store",
     "short": "Bring footfall and repeat customers with local visibility, offers and consistent social presence.",
     "intro": "Local retailers compete on visibility, trust and timely offers, in the store and on the phone screen.",
     "opps": ["Local listings with accurate stock categories and hours", "Festival and seasonal promotion creatives", "Consistent social content showcasing new arrivals"],
     "services": ["Google Business Profile", "Graphic Design", "Social Media", "Meta Ads", "Reel Editing"], "wa": "design"},
    {"slug": "ecommerce", "title": "E-commerce", "home": "", "icon": "cart",
     "short": "Improve product discovery and campaign performance for online stores.",
     "intro": "Online stores need steady traffic, strong product presentation and a smooth path to checkout.",
     "opps": ["Product and category page SEO recommendations", "Creative sets for Meta and Google campaigns", "Landing pages for launches and seasonal sales"],
     "services": ["SEO", "Google & Meta Ads", "Creative Design", "Landing Pages", "Strategy"], "wa": "ads"},
    {"slug": "education", "title": "Education", "home": "Education", "icon": "cap",
     "short": "Reach prospective students and parents with clear programme information and timely admission campaigns.",
     "intro": "Students and parents compare institutions online. Clear programme details, credibility and responsiveness matter.",
     "opps": ["Admission-season campaigns with dedicated landing pages", "Content that shows campus life, faculty and outcomes (verified)", "Local search presence for nearby families"],
     "services": ["Lead Generation", "Social Media", "Google Business Profile", "Video Editing", "Website Design"], "wa": "leads"},
    {"slug": "manufacturing", "title": "Manufacturing", "home": "Manufacturing", "icon": "factory",
     "short": "Make products and capabilities easy to find and understand for buyers, distributors and partners.",
     "intro": "B2B buyers search for suppliers and evaluate capability, quality and reliability before making contact.",
     "opps": ["A product-focused website with catalogue and specification pages", "SEO around product and industry terms", "Brochures and capability presentations"],
     "services": ["Website Design", "SEO", "Brochure Design", "Branding", "Lead Generation"], "wa": "website"},
    {"slug": "startups-smes", "title": "Startups & SMEs", "home": "Startups", "icon": "rocket",
     "short": "Establish a credible identity quickly and focus limited budgets on the channels that matter most.",
     "intro": "Early-stage and growing businesses need to look credible and prioritise carefully, because budgets and time are limited.",
     "opps": ["A clear brand identity and simple website", "A focused plan on one or two channels first", "Scalable content and creative templates"],
     "services": ["Branding", "Website Design", "Strategy & Consulting", "Social Media", "Google Business Profile"], "wa": "strategy"},
]
# Home page shows 10 industry cards using these labels
HOME_INDUSTRIES = [
    ("bed", "Hospitality", "Reels, local listings and offer campaigns that help guests discover and choose you.", "hotels-restaurants"),
    ("heart", "Healthcare", "Trustworthy information and accurate local presence for patients searching nearby.", "doctors-clinics"),
    ("briefcase", "Professional Services", "Credible websites and local SEO for CAs, consultants and advisers.", "ca-professional-services"),
    ("home", "Real Estate", "Project landing pages and targeted campaigns that capture buyer enquiries.", "real-estate"),
    ("sun", "Solar & Renewable Energy", "Educational content and local campaigns for customers researching solar.", "solar-renewable-energy"),
    ("bag", "Retail & E-commerce", "Offers, product creatives and search visibility for stores and online shops.", "retail"),
    ("cap", "Education", "Admission campaigns and clear programme information for students and parents.", "education"),
    ("factory", "Manufacturing", "Product-led websites and SEO that help buyers find and evaluate suppliers.", "manufacturing"),
    ("store", "Local Businesses", "Google Business Profile and social presence that bring nearby customers in.", "retail"),
    ("rocket", "Startups", "A credible identity and a focused plan that makes early budgets count.", "startups-smes"),
]

WHY_MATTERS = [
    ("Online visibility", "Customers look for businesses online first. Being easy to find is where marketing starts."),
    ("Brand credibility", "A professional website, accurate listings and consistent design build trust before a conversation begins."),
    ("Relevant website traffic", "Search, social and paid channels can bring people who are actually looking for what you offer."),
    ("Customer enquiries", "Clear calls to action and simple forms make it easy for interested people to get in touch."),
    ("Audience engagement", "Regular, useful content keeps your business familiar to customers and prospects."),
    ("Better marketing measurement", "Connected channels and tracking show what is working, so budgets can be directed with confidence."),
]

FAQS = [
    ("What services does BusinessLift offer?", "We offer Google Business Profile management, SEO, social media management, website design and management, Google Ads and Meta Ads management, lead generation, reel and video editing, graphic and flyer design, branding and logo design, and digital marketing strategy and consulting."),
    ("Which types of businesses do you work with?", "We work with small and medium-sized businesses, startups and growing companies across India, including hotels and restaurants, clinics, CA and professional firms, real estate, solar and renewable energy, retail and e-commerce, education, manufacturing and local service providers."),
    ("How can digital marketing help my business?", "A coordinated digital strategy can improve your visibility, strengthen credibility, bring relevant visitors to your website, encourage customer enquiries and make your marketing easier to measure. Results depend on your market, offer, budget and consistency, so we do not promise specific outcomes."),
    ("Do you manage Google Business Profiles?", "Yes. We can optimise your profile, keep business information current, create posts, manage photos, guide your review responses and monitor performance. Google controls how profiles are ranked and displayed, so we cannot promise a particular position."),
    ("Do you provide SEO services?", "Yes. SEO includes keyword research, on-page optimisation, technical checks, local SEO, content recommendations and performance monitoring. SEO is a gradual process, and we do not guarantee rankings."),
    ("Can you manage Google Ads and Meta Ads?", "Yes. We plan campaigns, research audiences, set up campaigns, coordinate ad creatives, optimise performance and report on results. Advertising spend is paid to the platforms and is separate from our management fee."),
    ("Do your packages include advertising spend?", "No, unless a particular quotation clearly says so. Advertising budgets, third-party subscriptions and applicable taxes are quoted separately where relevant."),
    ("How do you determine the right marketing strategy?", "We start with a discovery conversation about your business, audience, goals, competitors and current presence. From that, we recommend a practical set of priorities that fits your budget and capacity, then refine it as results come in."),
    ("How can I get a quotation?", "Share your requirements through the contact form, WhatsApp, email or phone. Final pricing depends on your goals, scope of work, deliverables and campaign requirements, so we prepare a proposal after understanding your needs."),
    ("How do I get started with BusinessLift?", "Get in touch for a free consultation. We discuss your business and goals, recommend a suitable approach, share a proposal and, once agreed, begin with onboarding and planning."),
]

VALUES = [
    ("Strategy", "We plan before we act, so effort is directed at the goals that matter."),
    ("Creativity", "Ideas and design that help your business stand out for the right reasons."),
    ("Transparency", "Clear scope, honest reporting and no hidden surprises."),
    ("Accountability", "We take ownership of our work and follow through on what we commit to."),
    ("Continuous Improvement", "We review, learn and refine as real results and feedback come in."),
    ("Client Partnership", "We work as an extension of your team, not a distant vendor."),
]

BLOG_CATEGORIES = ["SEO", "Google Business Profile", "Social Media Marketing", "Google Ads", "Meta Ads", "Lead Generation", "Branding", "Website Optimization", "Digital Marketing for Indian Businesses"]
BLOG_SAMPLES = [
    ("Getting More From Your Google Business Profile", "Google Business Profile", "A practical checklist for completing and maintaining a local profile that customers can trust."),
    ("SEO Basics for Small Businesses in India", "SEO", "The fundamentals of search visibility explained simply, without jargon or unrealistic promises."),
    ("Building a Social Media Content Calendar You Can Follow", "Social Media Marketing", "How to plan a month of posts around offers, festivals and customer questions."),
    ("Google Ads or Meta Ads: Choosing the Right Platform", "Google Ads", "How intent-based search ads and interest-based social ads differ, and when each fits."),
    ("What to Prepare Before Starting Meta Ads", "Meta Ads", "The assets, tracking and goals worth sorting out before you spend on social advertising."),
    ("From Enquiry to Customer: The Basics of Lead Tracking", "Lead Generation", "Why knowing where enquiries come from changes how you spend your marketing budget."),
    ("Why Consistent Branding Builds Trust", "Branding", "How colours, fonts and tone across channels make a business easier to recognise and remember."),
    ("What Your Website Needs Before You Run Ads", "Website Optimization", "A short list of fixes that make paid traffic more likely to turn into enquiries."),
    ("Digital Marketing for Indian Businesses: Where to Start", "Digital Marketing for Indian Businesses", "A simple order of priorities for businesses taking their first serious step online."),
]

PACKAGES = [
    {
        "name": "Basic", "tag": "Foundation", "blurb": "Core online visibility for businesses getting started.",
        "included": ["Google Business Profile management", "Social media management (limited scope)", "Graphic design for key promotions", "Basic monthly summary report"],
        "deliverables": "Number of posts, creatives and updates per month is defined in your proposal.",
        "excl": ["Advertising spend", "SEO and ad management", "Website design or development"],
        "featured": False,
    },
    {
        "name": "Growth", "tag": "For lead-focused businesses", "blurb": "Visibility plus active lead generation and optimisation.",
        "included": ["Everything in Basic, with a wider scope", "SEO (on-page and local)", "Google Ads and Meta Ads management", "Lead tracking and enquiry reporting", "Monthly performance report"],
        "deliverables": "Content volume, number of campaigns and reporting cadence are defined in your proposal.",
        "excl": ["Advertising spend", "Third-party tools and subscriptions", "Full website redesign"],
        "featured": True,
    },
    {
        "name": "Premium", "tag": "Full-service partnership", "blurb": "A broader, integrated programme for ambitious businesses.",
        "included": ["Everything in Growth, with a wider scope", "Reel and video editing", "Website updates and maintenance", "Branding support", "Strategy consulting and review calls"],
        "deliverables": "Scope, volumes and support level are tailored and defined in your proposal.",
        "excl": ["Advertising spend", "Third-party subscriptions and licensed assets", "Domain and hosting costs"],
        "featured": False,
    },
]

COMPARE = [
    ("Google Business Profile management", "Included", "Included", "Included"),
    ("Social media management", "Limited", "Included", "Included"),
    ("Graphic design & flyers", "Limited", "Included", "Included"),
    ("SEO (on-page & local)", "-", "Included", "Included"),
    ("Google Ads & Meta Ads management", "-", "Included", "Included"),
    ("Lead tracking & enquiry reporting", "-", "Included", "Included"),
    ("Reel & video editing", "-", "Limited", "Included"),
    ("Website updates & maintenance", "-", "Limited", "Included"),
    ("Branding support", "-", "-", "Included"),
    ("Strategy & consulting", "-", "Periodic review", "Included"),
    ("Reporting", "Basic summary", "Monthly report", "Monthly report + review call"),
]


# ----------------------------------------------------------------------------
# Layout helpers
# ----------------------------------------------------------------------------
def logo(light=False):
    # TEMPORARY text-based logo (BL monogram). Replace with the official logo when available.
    cls = "logo logo--light" if light else "logo"
    return ('<a class="%s" href="index.html" aria-label="BusinessLift, home">'
            '<span class="logo-mark" aria-hidden="true">BL</span>'
            '<span class="logo-text">Business<span>Lift</span></span></a>' % cls)


def head(title, desc, filename, schema=None, noindex=False):
    url = SITE["base"] + ("/" if filename == "index.html" else "/" + filename)
    og_img = SITE["base"] + "/assets/images/og-image.png"
    out = [
        '<!DOCTYPE html>',
        '<html lang="en-IN">',
        '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>%s</title>' % e(title),
        '<meta name="description" content="%s">' % e(desc),
        '<link rel="canonical" href="%s">' % e(url),
    ]
    if noindex:
        out.append('<meta name="robots" content="noindex, follow">')
    out += [
        '<meta name="theme-color" content="#071B49">',
        '<meta property="og:type" content="website">',
        '<meta property="og:site_name" content="BusinessLift">',
        '<meta property="og:locale" content="en_IN">',
        '<meta property="og:title" content="%s">' % e(title),
        '<meta property="og:description" content="%s">' % e(desc),
        '<meta property="og:url" content="%s">' % e(url),
        '<meta property="og:image" content="%s">' % e(og_img),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % e(title),
        '<meta name="twitter:description" content="%s">' % e(desc),
        '<meta name="twitter:image" content="%s">' % e(og_img),
        '<link rel="icon" href="assets/icons/favicon.svg" type="image/svg+xml">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&amp;display=swap">',
        '<link rel="stylesheet" href="css/styles.css">',
        '<link rel="stylesheet" href="css/responsive.css">',
        '<script>document.documentElement.classList.add("js");</script>',
    ]
    for s in (schema or []):
        out.append('<script type="application/ld+json">%s</script>' % json.dumps(s, ensure_ascii=False))
    out.append('</head>')
    return "\n".join(out)


def header(current):
    items = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == current else ""
        items.append('<li><a href="%s"%s>%s</a></li>' % (href, cur, label))
    return """<a class="skip-link" href="#main">Skip to main content</a>
<div class="announce"><p>Helping Indian Businesses Build Visibility, Generate Leads &amp; Grow.</p></div>
<header class="site-header" data-header>
  <div class="container header-inner">
    %s
    <nav id="site-nav" class="site-nav" aria-label="Primary">
      <ul>
        %s
      </ul>
      <a class="btn btn-primary nav-cta-mobile" href="contact.html">Get Free Consultation</a>
    </nav>
    <a class="btn btn-primary btn-sm header-cta" href="contact.html">Get Free Consultation</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span class="bars"></span></button>
  </div>
</header>""" % (logo(), "\n        ".join(items))


def footer(wa_key):
    svc_links = "\n".join('<li><a href="services.html#%s">%s</a></li>' % (s["slug"], e(s["title"])) for s in SERVICES)
    nav_links = "\n".join('<li><a href="%s">%s</a></li>' % (h, l) for h, l, _ in NAV)
    return """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        %s
        <p>BusinessLift helps businesses build their digital presence, generate qualified leads and achieve measurable growth through strategic digital marketing.</p>
        <div data-social-wrap hidden>
          <h2 class="sr-only">Social profiles</h2>
          <div class="social-list" data-social-list></div>
        </div>
      </div>
      <div>
        <h2>Services</h2>
        <ul>
        %s
        </ul>
      </div>
      <div>
        <h2>Quick Links</h2>
        <ul>
        %s
        <li><a href="case-studies.html">Case Studies</a></li>
        </ul>
      </div>
      <div>
        <h2>Contact</h2>
        <ul>
          <li><a href="tel:%s">%s</a></li>
          <li><a href="mailto:%s">%s</a></li>
          <li><a href="%s" data-wa="general" target="_blank" rel="noopener noreferrer">Chat on WhatsApp</a></li>
          <li>Serving businesses across India</li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; <span data-year>2026</span> BusinessLift. All rights reserved.</p>
      <ul>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
        <li><a href="terms.html">Terms &amp; Conditions</a></li>
      </ul>
    </div>
  </div>
</footer>
<a class="wa-float" href="%s" data-wa="%s" target="_blank" rel="noopener noreferrer" aria-label="Chat with BusinessLift on WhatsApp (opens in a new tab)">%s<span class="wa-label">WhatsApp</span></a>""" % (
        logo(light=True), svc_links, nav_links, SITE["tel"], SITE["phone"], SITE["email"], SITE["email"],
        SITE["wa"], SITE["wa"], wa_key, icon("chat", 26))


def breadcrumb(label):
    return ('<nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li>'
            '<li aria-current="page">%s</li></ol></nav>' % e(label))


def page_hero(label, h1, lead):
    return ('<section class="page-hero"><div class="container">%s<h1>%s</h1><p class="lead">%s</p></div></section>'
            % (breadcrumb(label), e(h1), e(lead)))


def crumb_schema(label, filename):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE["base"] + "/"},
        {"@type": "ListItem", "position": 2, "name": label, "item": SITE["base"] + "/" + filename}]}


def cta_band(title="Ready to Lift Your Business?", desc="Let's discuss your goals and identify practical opportunities to strengthen your digital presence.", wa="general", dark=True):
    return """<section class="section section--dark cta-band" aria-labelledby="cta-title">
  <div class="container reveal">
    <h2 id="cta-title">%s</h2>
    <p>%s</p>
    <div class="btn-row btn-row--center">
      <a class="btn btn-primary" href="contact.html">Get Free Consultation</a>
      <a class="btn btn-light" href="%s" data-wa="%s" target="_blank" rel="noopener noreferrer">%sChat on WhatsApp</a>
    </div>
  </div>
</section>""" % (e(title), e(desc), SITE["wa"], wa, icon("chat", 20))


def write_page(filename, current, title, desc, body, schema=None, noindex=False, wa="general", scripts=(), label=None):
    s = list(schema or [])
    if filename != "index.html" and label and not noindex:
        s.append(crumb_schema(label, filename))
    parts = [
        head(title, desc, filename, s, noindex), "<body>", header(current),
        '<main id="main">', body, "</main>", footer(wa),
        '<script src="js/main.js" defer></script>',
    ]
    for sc in scripts:
        parts.append('<script src="js/%s" defer></script>' % sc)
    parts += ["</body>", "</html>", ""]
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
    print("wrote", filename)


def section_head(eyebrow, title, desc="", center=False, tid=None):
    cls = "section-head section-head--center" if center else "section-head"
    idattr = ' id="%s"' % tid if tid else ""
    d = "<p>%s</p>" % e(desc) if desc else ""
    return '<div class="%s reveal"><p class="eyebrow">%s</p><h2%s>%s</h2>%s</div>' % (cls, e(eyebrow), idattr, e(title), d)


def faq_html(prefix="faq"):
    out = ['<div class="faq reveal">']
    for i, (q, a) in enumerate(FAQS, 1):
        out.append(
            '<div class="faq-item"><h3><button class="faq-q" type="button" aria-expanded="false" '
            'aria-controls="%s-a%d" id="%s-q%d"><span>%s</span><span class="faq-icon" aria-hidden="true"></span></button></h3>'
            '<div class="faq-a" id="%s-a%d" role="region" aria-labelledby="%s-q%d" hidden><p>%s</p></div></div>'
            % (prefix, i, prefix, i, e(q), prefix, i, prefix, i, e(a)))
    out.append("</div>")
    return "\n".join(out)


# ----------------------------------------------------------------------------
# Pages
# ----------------------------------------------------------------------------
HERO_SVG = """<svg viewBox="0 0 520 420" role="img" aria-label="Abstract illustration of rising bars and an upward arrow representing business growth" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#ffffff" stroke-opacity=".08"><path d="M30 80h460M30 160h460M30 240h460M30 320h460"/></g>
  <circle cx="440" cy="70" r="46" fill="#1D4F9C" fill-opacity=".35"/>
  <circle cx="70" cy="330" r="30" fill="#FFC928" fill-opacity=".18"/>
  <rect x="50" y="290" width="62" height="100" rx="8" fill="#1B3F82"/>
  <rect x="130" y="240" width="62" height="150" rx="8" fill="#21509E"/>
  <rect x="210" y="190" width="62" height="200" rx="8" fill="#2A63B8"/>
  <rect x="290" y="130" width="62" height="260" rx="8" fill="#3677CF"/>
  <rect x="370" y="60" width="62" height="330" rx="8" fill="#FFC928"/>
  <path d="M56 265 L150 205 L226 225 L316 120 L404 52" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M382 46 L410 42 L404 70" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="#ffffff"><circle cx="56" cy="265" r="6"/><circle cx="150" cy="205" r="6"/><circle cx="226" cy="225" r="6"/><circle cx="316" cy="120" r="6"/></g>
  <path d="M30 392h460" stroke="#ffffff" stroke-opacity=".25" stroke-width="2"/>
</svg>"""


def build_home():
    svc_cards = "\n".join(
        '<article class="card service-card reveal"><div class="icon-box">%s</div><div class="card-body"><h3>%s</h3><p>%s</p></div>'
        '<a class="link-arrow" href="services.html#%s" aria-label="Learn more about %s">Learn More%s</a></article>'
        % (icon(s["icon"]), e(s["title"]), e(s["short"]), s["slug"], e(s["title"]), icon("arrow", 18))
        for s in SERVICES)
    why = "\n".join(
        '<article class="card card--dark reveal"><div class="icon-box">%s</div><h3>%s</h3><p>%s</p></article>' % (icon(i), e(t), e(d))
        for i, t, d in PRINCIPLES)
    process = "\n".join(
        '<li class="reveal"><span class="step-num" aria-hidden="true">%s</span><h3><span class="sr-only">Step %s: </span>%s</h3><p>%s</p></li>' % (n, n, e(t), e(d))
        for n, t, d in PROCESS)
    inds = "\n".join(
        '<article class="card industry-card reveal"><div class="icon-box">%s</div><h3>%s</h3><p>%s</p></article>' % (icon(i), e(t), e(d))
        for i, t, d, _ in HOME_INDUSTRIES)
    work_tiles = [
        ("layout", "Website projects", "Responsive layouts and landing pages, shown here as sample concepts."),
        ("share", "Social media creatives", "Post and story design concepts that keep brand and message consistent."),
        ("pin", "Google Business Profile optimisation", "Example profile audit formats and update plans."),
        ("palette", "Branding & logo design", "Logo directions, palettes and typography concepts."),
        ("target", "Advertising campaigns", "Sample campaign structures and creative sets."),
        ("compass", "Marketing strategy", "Sample audit and planning formats."),
    ]
    tiles = "\n".join(
        '<article class="card work-card reveal"><div class="thumb">%s<span class="badge">Sample concept</span></div>'
        '<div class="work-body"><h3>%s</h3><p>%s</p></div></article>' % (icon(i, 44), e(t), e(d))
        for i, t, d in work_tiles)
    matters = "\n".join(
        '<li><span class="tick">%s</span><div><strong>%s</strong><span class="desc">%s</span></div></li>' % (icon("check", 16), e(t), e(d))
        for t, d in WHY_MATTERS)

    body = """
<section class="hero" aria-labelledby="hero-title">
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="eyebrow eyebrow--light">Digital Marketing &amp; Growth Agency</p>
      <h1 id="hero-title">Lift Your Business. <span class="accent">Grow Your Brand.</span></h1>
      <p class="hero-sub">Digital Marketing That Moves Your Business Forward.</p>
      <p class="hero-desc">BusinessLift helps businesses strengthen their online presence, reach the right audience, generate qualified enquiries, and build sustainable growth through strategic digital marketing.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contact.html">Get Free Consultation</a>
        <a class="btn btn-light" href="services.html">Explore Our Services</a>
      </div>
      <p class="hero-trust">Strategy. Visibility. Leads. Growth.</p>
    </div>
    <div class="hero-visual">
      %s
      <span class="hero-chip hero-chip--1" aria-hidden="true">%sVisibility</span>
      <span class="hero-chip hero-chip--2" aria-hidden="true">%sQualified enquiries</span>
      <span class="hero-chip hero-chip--3" aria-hidden="true">%sGrowth</span>
    </div>
  </div>
</section>

<section class="section" id="services" aria-labelledby="services-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--3 grid--services">
      %s
    </div>
  </div>
</section>

<section class="section section--dark" aria-labelledby="why-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--3">
      %s
    </div>
  </div>
</section>

<section class="section" aria-labelledby="process-title">
  <div class="container">
    %s
    <ol class="process">
      %s
    </ol>
  </div>
</section>

<section class="section section--alt" aria-labelledby="industries-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--5">
      %s
    </div>
    <p class="reveal" style="margin-top:1.75rem"><a class="link-arrow" href="industries.html">See All Industries We Serve%s</a></p>
  </div>
</section>

<section class="section" aria-labelledby="work-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--3">
      %s
    </div>
    <div class="btn-row reveal" style="margin-top:2rem"><a class="btn btn-primary" href="portfolio.html">Explore Our Work</a></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="matters-title">
  <div class="container split split--wide-left">
    <div class="reveal">
      <p class="eyebrow">Why It Matters</p>
      <h2 id="matters-title">Why Digital Marketing Matters</h2>
      <p>Today, most customers research online before they call, visit or buy. A coordinated digital strategy connects the pieces (your listings, website, content and campaigns) so they support each other rather than work in isolation.</p>
      <p>It is not a shortcut, and no one can promise guaranteed outcomes. But done consistently and measured honestly, it gives your business a better chance of being found, trusted and contacted.</p>
    </div>
    <ul class="checklist reveal">
      %s
    </ul>
  </div>
</section>

<section class="section" aria-labelledby="testimonials-title">
  <div class="container">
    <div class="empty-state reveal">
      <div class="icon-box">%s</div>
      <p class="eyebrow">Client Stories</p>
      <h2 id="testimonials-title">Let's Talk About Your Business First</h2>
      <p>We would rather earn your trust with a clear conversation than with placeholder quotes. Verified client stories will appear here as projects are completed. Until then, tell us about your business and goals and we will share how we would approach them.</p>
      <div class="btn-row btn-row--center"><a class="btn btn-primary" href="contact.html">Discuss Your Requirements</a></div>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="faq-title">
  <div class="container">
    %s
    %s
  </div>
</section>

%s
""" % (
        HERO_SVG, icon("search", 18), icon("funnel", 18), icon("chart", 18),
        section_head("What We Do", "Everything Your Business Needs to Grow Online", "From building your online presence to generating enquiries, we help connect your business with the right digital opportunities.", True, "services-title"),
        svc_cards,
        section_head("Why BusinessLift", "Marketing With a Clear Business Purpose", "", True, "why-title"), why,
        section_head("How We Work", "Our Process", "A simple, repeatable five-step approach.", True, "process-title"), process,
        section_head("Industries", "Industries We Serve", "Every sector has its own marketing opportunities. Here is where we focus.", True, "industries-title"), inds, icon("arrow", 18),
        section_head("Featured Work", "A Preview of Our Work", "These are clearly labelled sample concepts that show the kind of work we do. Genuine client projects will replace them as they are delivered.", True, "work-title"), tiles,
        matters, icon("chat", 26),
        section_head("FAQ", "Frequently Asked Questions", "", True, "faq-title"), faq_html(),
        cta_band(),
    )
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    org = {"@context": "https://schema.org", "@type": ["Organization", "ProfessionalService"], "name": "BusinessLift",
           "url": SITE["base"] + "/", "slogan": SITE["tagline"], "telephone": SITE["phone"], "email": SITE["email"],
           "description": "BusinessLift helps businesses build their digital presence, generate qualified leads and achieve measurable growth through strategic digital marketing.",
           "areaServed": {"@type": "Country", "name": "India"}}
    write_page("index.html", "home", "BusinessLift | Digital Marketing & Growth Agency for Indian Businesses",
               "BusinessLift helps businesses build visibility, generate qualified enquiries and grow through SEO, social media, ads, websites and branding. Lift Your Business. Grow Your Brand.",
               body, [org, faq_schema])


def build_about():
    vals = "\n".join('<article class="card reveal"><h3>%s</h3><p>%s</p></article>' % (e(t), e(d)) for t, d in VALUES)
    body = page_hero("About", "About BusinessLift", "A digital marketing and growth agency helping businesses across India build visibility, generate qualified enquiries and grow.") + """
<section class="section" aria-labelledby="intro-title">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Who We Are</p>
      <h2 id="intro-title">A Practical Growth Partner for Your Business</h2>
      <p>BusinessLift helps businesses build their digital presence, generate qualified leads and achieve measurable growth through strategic digital marketing.</p>
      <p>We work with small and medium-sized businesses, startups and growing companies that want a clear plan instead of scattered activity: from Google Business Profile and SEO to social media, advertising, websites and branding.</p>
    </div>
    <div class="grid reveal">
      <div class="card"><div class="icon-box">%s</div><h3>Our Mission</h3><p>To help businesses grow through practical, strategic, and results-oriented digital marketing solutions.</p></div>
      <div class="card"><div class="icon-box">%s</div><h3>Our Vision</h3><p>To become a trusted digital growth partner for businesses across India.</p></div>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="values-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--3">%s</div>
  </div>
</section>

<section class="section" aria-labelledby="approach-title">
  <div class="container split">
    <div class="reveal">
      <p class="eyebrow">Our Approach</p>
      <h2 id="approach-title">Strategy First, Then Execution</h2>
      <p>Good marketing is rarely about doing everything; it is about doing the right things in the right order. We begin by understanding your business, customers and competitors, then recommend a focused plan that fits your goals and budget.</p>
      <p>We use the data that is available to guide decisions, are open about what is working and what is not, and adjust as real results come in. We do not promise rankings, lead volumes or revenue; we promise careful work and honest communication.</p>
    </div>
    <div class="reveal">
      <h3>How We Work With Clients</h3>
      <ol class="plain-list">
        <li><strong>Discovery conversation.</strong> We learn about your business, audience and goals.</li>
        <li><strong>Proposal.</strong> You receive a clear scope, deliverables and pricing.</li>
        <li><strong>Onboarding.</strong> We gather access, assets and brand details.</li>
        <li><strong>Execution.</strong> We deliver the agreed activities and keep you updated.</li>
        <li><strong>Review.</strong> We share performance and refine the plan together.</li>
      </ol>
    </div>
  </div>
</section>

%s
""" % (icon("target", 26), icon("compass", 26),
       section_head("Core Values", "What Guides Our Work", "", True, "values-title"), vals,
       cta_band("Book a Free Consultation", "Tell us about your business and goals. We will suggest practical next steps, with no obligation."))
    write_page("about.html", "about", "About BusinessLift | Digital Marketing & Growth Agency in India",
               "Learn about BusinessLift's mission, vision, values and approach to practical, strategic digital marketing for businesses across India.", body, label="About")


def build_services():
    chips = "\n".join('<li><a href="#%s">%s</a></li>' % (s["slug"], e(s["title"])) for s in SERVICES)
    blocks = []
    for s in SERVICES:
        note = '<div class="notice"><p><strong>Please note:</strong> %s</p></div>' % e(s["note"]) if s["note"] else ""
        extra = ""
        if s.get("extra") == "web":
            extra = """<div class="detail-grid">
  <div class="panel"><h3>Website design project</h3><p>A one-time project covering planning, design, build and launch of a new website or landing page. Scoped and quoted per project.</p></div>
  <div class="panel"><h3>Ongoing website management</h3><p>A separate, recurring service for content updates, small improvements, monitoring and maintenance after launch. Quoted monthly or as agreed.</p></div>
</div>"""
        blocks.append("""<article class="service-block reveal" id="%(slug)s" aria-labelledby="%(slug)s-title">
  <div class="service-block-head"><div class="icon-box">%(icon)s</div><div><h2 id="%(slug)s-title">%(title)s</h2><p>%(intro)s</p></div></div>
  <div class="detail-grid">
    <div class="panel"><h3>What it involves</h3><p>%(what)s</p></div>
    <div class="panel"><h3>Who can benefit</h3><p>%(who)s</p></div>
    <div class="panel"><h3>Key deliverables</h3><ul class="plain-list">%(deliv)s</ul></div>
    <div class="panel"><h3>Objectives it can support</h3><ul class="plain-list">%(obj)s</ul></div>
  </div>
  %(extra)s%(note)s
  <div class="btn-row">
    <a class="btn btn-primary" href="%(wa)s" data-wa="%(wakey)s" target="_blank" rel="noopener noreferrer">Enquire About This Service</a>
    <a class="btn btn-secondary" href="contact.html">Get Free Consultation</a>
  </div>
</article>""" % {
            "slug": s["slug"], "icon": icon(s["icon"]), "title": e(s["title"]), "intro": e(s["intro"]), "what": e(s["what"]), "who": e(s["who"]),
            "deliv": "".join("<li>%s</li>" % e(x) for x in s["deliverables"]),
            "obj": "".join("<li>%s</li>" % e(x) for x in s["objectives"]), "extra": extra, "note": note,
            "wa": SITE["wa"], "wakey": s["wa"]})
    body = page_hero("Services", "Digital Marketing Services", "Ten focused services that work on their own or together, built around your business goals.") + """
<section class="section" aria-label="Service details">
  <div class="container">
    <nav aria-label="Jump to a service"><ul class="chip-list">%s</ul></nav>
    %s
  </div>
</section>
%s
""" % (chips, "\n".join(blocks), cta_band("Not Sure Which Service You Need?", "A short conversation is usually enough to identify the right starting point for your business."))
    svc_schema = {"@context": "https://schema.org", "@type": "ItemList", "name": "BusinessLift services", "itemListElement": [
        {"@type": "ListItem", "position": i, "item": {"@type": "Service", "name": s["title"], "description": s["short"],
                                                      "provider": {"@type": "Organization", "name": "BusinessLift"}, "areaServed": {"@type": "Country", "name": "India"}}}
        for i, s in enumerate(SERVICES, 1)]}
    write_page("services.html", "services", "Digital Marketing Services | SEO, Ads, Social Media, Websites | BusinessLift",
               "Explore BusinessLift's services: Google Business Profile, SEO, social media, websites, Google and Meta Ads, lead generation, video editing, design, branding and strategy.",
               body, [svc_schema], label="Services")


def build_industries():
    blocks = []
    for ind in INDUSTRIES:
        blocks.append("""<article class="service-block reveal" id="%s" aria-labelledby="%s-title">
  <div class="service-block-head"><div class="icon-box">%s</div><div><h2 id="%s-title">%s</h2><p>%s</p></div></div>
  <div class="detail-grid">
    <div class="panel"><h3>Marketing opportunities</h3><ul class="plain-list">%s</ul></div>
    <div class="panel"><h3>Relevant services</h3><ul class="tag-list">%s</ul><p>Outcomes depend on your market, offer, budget and consistency. We do not guarantee specific results.</p></div>
  </div>
  <div class="btn-row"><a class="btn btn-primary" href="%s" data-wa="%s" target="_blank" rel="noopener noreferrer">Enquire for %s</a></div>
</article>""" % (ind["slug"], ind["slug"], icon(ind["icon"]), ind["slug"], e(ind["title"]), e(ind["intro"]),
                 "".join("<li>%s</li>" % e(x) for x in ind["opps"]), "".join("<li>%s</li>" % e(x) for x in ind["services"]),
                 SITE["wa"], ind["wa"], e(ind["title"])))
    chips = "\n".join('<li><a href="#%s">%s</a></li>' % (i["slug"], e(i["title"])) for i in INDUSTRIES)
    body = page_hero("Industries", "Industries We Serve", "Every sector has its own customers, competitors and opportunities. Here is how we approach each.") + """
<section class="section" aria-label="Industry details">
  <div class="container">
    <nav aria-label="Jump to an industry"><ul class="chip-list">%s</ul></nav>
    %s
  </div>
</section>
%s
""" % (chips, "\n".join(blocks), cta_band("Don't See Your Industry?", "We work with many kinds of businesses. Tell us about yours and we will tell you honestly how we can help."))
    write_page("industries.html", "industries", "Industries We Serve | Digital Marketing for Indian Businesses | BusinessLift",
               "Digital marketing for hotels and restaurants, clinics, CA firms, real estate, solar, retail, e-commerce, education, manufacturing, startups and SMEs.", body, label="Industries")


def build_portfolio():
    body = page_hero("Our Work", "Our Work", "A filterable gallery of work and concepts across branding, design, social media, websites, SEO and advertising.") + """
<section class="section" aria-labelledby="gallery-title">
  <div class="container">
    <div class="notice reveal"><p><strong>About these projects:</strong> The items below are sample concepts that illustrate the kinds of work BusinessLift offers. They are demonstrations, not completed client projects, and carry no client results. Genuine work will replace them as projects are delivered.</p></div>
    <h2 id="gallery-title" class="sr-only">Portfolio gallery</h2>
    <div id="portfolio-filters" class="filter-bar" role="group" aria-label="Filter projects by category"></div>
    <p id="portfolio-count" class="result-count" role="status" aria-live="polite"></p>
    <ul id="portfolio-grid" class="grid grid--2 grid--3" style="list-style:none;padding:0;margin:0"></ul>
    <noscript><p class="notice">The portfolio filter needs JavaScript. Please enable it, or <a href="contact.html">contact us</a> to see examples of our work.</p></noscript>
  </div>
</section>
%s
""" % cta_band("Want Something Like This for Your Business?", "Tell us what you have in mind and we will suggest an approach.")
    write_page("portfolio.html", "portfolio", "Our Work | Portfolio | BusinessLift Digital Marketing Agency",
               "Browse BusinessLift sample concepts across branding, graphic design, social media, websites, SEO and advertising. Filter by category.", body,
               scripts=("portfolio.js",), label="Our Work")


def build_case_studies():
    fields = [("Client or project name", "users"), ("Industry", "briefcase"), ("Initial challenge", "target"), ("Strategy", "compass"),
              ("Activities completed", "check"), ("Results (verified only)", "chart"), ("Lessons learned", "refresh")]
    cards = "\n".join('<article class="card reveal"><div class="icon-box">%s</div><h3>%s</h3></article>' % (icon(i), e(t)) for t, i in fields)
    body = page_hero("Case Studies", "Case Studies", "Detailed, honest project write-ups, published once real results can be shared.") + """
<section class="section" aria-labelledby="empty-title">
  <div class="container">
    <div class="empty-state reveal">
      <div class="icon-box">%s</div>
      <h2 id="empty-title">Case Studies Are Coming Soon</h2>
      <p>Detailed case studies will be added as projects are completed and clients approve sharing their results. We do not publish invented numbers or placeholder success stories.</p>
      <div class="btn-row btn-row--center"><a class="btn btn-primary" href="contact.html">Discuss Your Project</a><a class="btn btn-secondary" href="portfolio.html">View Our Work</a></div>
    </div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="structure-title">
  <div class="container">
    %s
    <div class="grid grid--2 grid--4">%s</div>
  </div>
</section>

<!-- REUSABLE CASE STUDY TEMPLATE
     Copy the contents of this <template> into a new <article> inside the first section above,
     replace the bracketed text with VERIFIED information, and remove the empty state. -->
<template id="case-study-template">
  <article class="card case-study">
    <p class="cat-label">[Industry]</p>
    <h3>[Client or project name]</h3>
    <h4>Initial challenge</h4><p>[What problem did the client face?]</p>
    <h4>Strategy</h4><p>[What approach was agreed?]</p>
    <h4>Activities completed</h4><ul class="plain-list"><li>[Activity]</li></ul>
    <h4>Results</h4><p class="result-box">[Verified results only, with the time period]</p>
    <h4>Lessons learned</h4><p>[What worked, what we would change]</p>
  </article>
</template>
%s
""" % (icon("doc", 28), section_head("Layout", "How Each Case Study Will Be Structured", "Every write-up will follow the same transparent format.", True, "structure-title"), cards,
       cta_band("Be One of Our First Success Stories", "Let's discuss your goals and plan a campaign you can measure."))
    write_page("case-studies.html", "portfolio", "Case Studies | BusinessLift Digital Marketing Agency",
               "BusinessLift will publish detailed, verified case studies as projects are completed. See how each case study will be structured.", body, label="Case Studies")


def build_pricing():
    cards = []
    for p in PACKAGES:
        cards.append("""<article class="card price-card reveal%s">
  %s
  <h3>%s</h3>
  <p>%s</p>
  <p class="price"><span class="price-value" data-package-price>Custom quote</span><span class="price-unit">per month</span></p>
  <h4>Included services</h4><ul>%s</ul>
  <h4>Deliverables &amp; quantities</h4><p>%s</p>
  <h4>Exclusions</h4><ul>%s</ul>
  <div class="push"><a class="btn %s" href="contact.html?plan=%s" style="width:100%%">Request a Quotation</a></div>
</article>""" % (" price-card--featured" if p["featured"] else "", '<span class="badge">%s</span>' % e(p["tag"]), e(p["name"]), e(p["blurb"]),
                 "".join("<li>%s</li>" % e(x) for x in p["included"]), e(p["deliverables"]), "".join("<li>%s</li>" % e(x) for x in p["excl"]),
                 "btn-primary" if p["featured"] else "btn-secondary", p["name"]))
    def cell(v):
        if v == "-":
            return '<td><span class="no" aria-hidden="true">&mdash;</span><span class="sr-only">Not included</span></td>'
        cls = "yes" if v == "Included" else ""
        return '<td class="%s">%s</td>' % (cls, e(v))
    rows = "\n".join("<tr><th scope=\"row\">%s</th>%s%s%s</tr>" % (e(r[0]), cell(r[1]), cell(r[2]), cell(r[3])) for r in COMPARE)
    body = page_hero("Pricing", "Pricing & Packages", "Flexible packages shaped around your goals. Pricing is customised, not one-size-fits-all.") + """
<section class="section" aria-labelledby="packages-title">
  <div class="container">
    %s
    <div class="grid grid--pricing">%s</div>
    <div class="notice reveal" style="margin-top:2rem"><p>Final pricing depends on your business goals, scope of work, deliverables, and campaign requirements. Advertising spend, third-party subscriptions, and applicable taxes are quoted separately where relevant.</p></div>
  </div>
</section>

<section class="section section--alt" aria-labelledby="compare-title">
  <div class="container">
    %s
    <div class="table-wrap reveal" role="region" aria-labelledby="compare-title" tabindex="0">
      <table class="compare">
        <caption class="sr-only">Comparison of the Basic, Growth and Premium packages</caption>
        <thead><tr><th scope="col">Service</th><th scope="col">Basic</th><th scope="col">Growth</th><th scope="col">Premium</th></tr></thead>
        <tbody>%s</tbody>
      </table>
    </div>
    <p class="table-hint">Scroll sideways on small screens to see every column. This table shows the indicative structure; exact inclusions and quantities are confirmed in your proposal.</p>
  </div>
</section>
%s
""" % (section_head("Packages", "Choose a Starting Point", "Each package can be adjusted. Tell us what you need and we will tailor it.", True, "packages-title"), "\n".join(cards),
       section_head("Compare", "Package Comparison", "", True, "compare-title"), rows,
       cta_band("Request a Custom Proposal", "Share your goals and we will recommend the right scope, and a price that fits it.", "pricing"))
    write_page("pricing.html", "pricing", "Pricing & Packages | Digital Marketing Plans | BusinessLift",
               "Explore BusinessLift's Basic, Growth and Premium digital marketing packages. Pricing is customised to your goals and scope. Request a custom proposal.",
               body, wa="pricing", label="Pricing")


def build_blog():
    chips = "".join('<li><span class="tag">%s</span></li>' % e(c) for c in BLOG_CATEGORIES)
    cards = "\n".join("""<article class="card blog-card reveal">
  <p class="cat-label">%s</p>
  <h3>%s</h3>
  <p class="meta"><span>Publication date: to be added</span><span>Reading time: 5 min read</span></p>
  <p>%s</p>
  <span class="badge" style="align-self:flex-start;margin-bottom:1rem">Sample article structure</span>
  <a class="link-arrow" href="blog-post-template.html">View Article Template%s</a>
</article>""" % (e(c), e(t), e(s), icon("arrow", 18)) for t, c, s in BLOG_SAMPLES)
    body = page_hero("Blog", "Insights for Growing Businesses", "Practical guides on SEO, social media, ads, websites and branding for Indian businesses.") + """
<section class="section" aria-labelledby="blog-title">
  <div class="container">
    <div class="notice reveal"><p><strong>Articles coming soon.</strong> The cards below are sample article structures with topics we plan to cover. Publication dates and authors will be added when real articles are published.</p></div>
    <h2 id="blog-title" class="sr-only">Article topics</h2>
    <ul class="chip-list reveal" aria-label="Blog categories" style="margin-bottom:1.75rem">%s</ul>
    <div class="grid grid--2 grid--3">%s</div>
  </div>
</section>
%s
""" % (chips, cards, cta_band("Have a Marketing Question?", "Ask us directly and we will point you in the right direction."))
    write_page("blog.html", "blog", "Blog | Digital Marketing Insights for Indian Businesses | BusinessLift",
               "Practical digital marketing guides on SEO, Google Business Profile, social media, Google Ads, Meta Ads, lead generation, branding and websites.", body, label="Blog")


def build_blog_template():
    body = """
<section class="page-hero"><div class="container">
  <nav class="breadcrumb" aria-label="Breadcrumb"><ol><li><a href="index.html">Home</a></li><li><a href="blog.html">Blog</a></li><li aria-current="page">Article Template</li></ol></nav>
  <p class="cat-label" style="color:var(--yellow)">[Category]</p>
  <h1>[Article headline goes here]</h1>
  <p class="lead">[One-sentence summary that explains what the reader will learn.]</p>
</div></section>
<section class="section"><div class="container">
  <article class="article">
    <div class="notice"><p><strong>Template page.</strong> Duplicate this file (e.g. <code>blog-your-topic.html</code>), replace the placeholders, add the real date and author, and link it from <code>blog.html</code>. This template is set to noindex so it is not shown in search results.</p></div>
    <p class="article-meta">By [Author name] &middot; Published [date] &middot; [X] min read</p>
    <h2>Introduction</h2><p>[State the problem the reader has and what this article will help them do.]</p>
    <h2>Key point one</h2><p>[Explain clearly, with a practical example.]</p>
    <h2>Key point two</h2><ul class="plain-list"><li>[Step or tip]</li><li>[Step or tip]</li><li>[Step or tip]</li></ul>
    <h2>Common mistakes</h2><p>[What to avoid.]</p>
    <h2>Next steps</h2><p>[Summarise and invite the reader to get in touch.]</p>
    <!-- Add Article structured data when publishing:
    {"@context":"https://schema.org","@type":"Article","headline":"[Headline]","datePublished":"[YYYY-MM-DD]",
     "author":{"@type":"Person","name":"[Author]"},"publisher":{"@type":"Organization","name":"BusinessLift"}} -->
  </article>
</div></section>
""" + cta_band("Want Help Applying This?", "Talk to us about your business and goals.")
    write_page("blog-post-template.html", "blog", "Article Template | BusinessLift Blog", "Template for BusinessLift blog articles.", body, noindex=True)


def build_contact():
    industries = ["Hotels & Restaurants", "Doctors & Clinics", "CA Firms & Professional Services", "Real Estate", "Solar & Renewable Energy",
                  "Retail", "E-commerce", "Education", "Manufacturing", "Startup / SME", "Other"]
    svc_opts = [s["title"] for s in SERVICES]
    budgets = ["Not sure yet", "Under ₹10,000 per month", "₹10,000 – ₹25,000 per month", "₹25,000 – ₹50,000 per month", "₹50,000 – ₹1,00,000 per month", "Above ₹1,00,000 per month"]
    ind_html = '<option value="">Select your industry</option>' + "".join('<option>%s</option>' % e(i) for i in industries)
    bud_html = '<option value="">Select a range (optional)</option>' + "".join('<option>%s</option>' % e(b) for b in budgets)
    svc_html = "".join('<div class="check"><input type="checkbox" id="svc-%d" name="services" value="%s"><label for="svc-%d">%s</label></div>' % (i, e(s), i, e(s)) for i, s in enumerate(svc_opts))
    body = page_hero("Contact", "Contact BusinessLift", "Tell us about your business and goals. We'll suggest practical next steps.") + """
<section class="section" aria-labelledby="form-title">
  <div class="container split split--wide-left">
    <div class="reveal">
      <h2 id="form-title">Let's Discuss Your Business Goals</h2>
      <p>Fill in the form and we'll prepare your enquiry. Fields marked <span class="req">*</span> are required.</p>
      <p class="notice" data-form-mode-note>This website is not yet connected to an automatic submission service. After you submit, you'll be able to send your enquiry through WhatsApp or email. Nothing is sent until you press Send there.</p>
      <form id="contact-form" class="form" novalidate>
        <div class="form-alert" role="alert" hidden></div>
        <div class="form-grid">
          <div class="field"><label for="name">Full name <span class="req" aria-hidden="true">*</span></label>
            <input type="text" id="name" name="name" autocomplete="name" required aria-describedby="err-name"><p class="field-error" id="err-name"></p></div>
          <div class="field"><label for="business">Business name</label>
            <input type="text" id="business" name="business" autocomplete="organization"></div>
          <div class="field"><label for="phone">Phone number <span class="req" aria-hidden="true">*</span></label>
            <input type="tel" id="phone" name="phone" autocomplete="tel" inputmode="tel" required aria-describedby="err-phone hint-phone" placeholder="e.g. 98765 43210">
            <p class="field-hint" id="hint-phone">10-digit mobile number, or include a country code.</p><p class="field-error" id="err-phone"></p></div>
          <div class="field"><label for="email">Email <span class="req" aria-hidden="true">*</span></label>
            <input type="email" id="email" name="email" autocomplete="email" required aria-describedby="err-email"><p class="field-error" id="err-email"></p></div>
          <div class="field"><label for="industry">Industry</label><select id="industry" name="industry">%s</select></div>
          <div class="field"><label for="budget">Estimated budget</label><select id="budget" name="budget">%s</select></div>
          <fieldset class="field field--full"><legend>Services required</legend><div class="check-grid">%s</div></fieldset>
          <div class="field field--full"><label for="message">Message</label>
            <textarea id="message" name="message" rows="5" placeholder="Tell us about your business and what you want to achieve."></textarea></div>
          <div class="hp" aria-hidden="true"><label>Leave this field empty<input type="text" name="website" tabindex="-1" autocomplete="off"></label></div>
          <div class="field field--full"><div class="check"><input type="checkbox" id="consent" name="consent" required aria-describedby="err-consent">
            <label for="consent">I agree to be contacted by BusinessLift about my enquiry and have read the <a href="privacy-policy.html">Privacy Policy</a>. <span class="req" aria-hidden="true">*</span></label></div>
            <p class="field-error" id="err-consent"></p></div>
        </div>
        <div class="btn-row" style="margin-top:1.25rem"><button class="btn btn-primary" type="submit">Prepare My Enquiry</button></div>
      </form>
      <div id="form-result" class="form-result" role="status" hidden></div>
    </div>
    <aside class="stack reveal" aria-label="Contact details">
      <div class="card contact-card"><div class="icon-box">%s</div><div><h3>Phone</h3><p><a href="tel:%s">%s</a></p></div></div>
      <div class="card contact-card"><div class="icon-box">%s</div><div><h3>Email</h3><p><a href="mailto:%s">%s</a></p></div></div>
      <div class="card contact-card"><div class="icon-box">%s</div><div><h3>WhatsApp</h3><p><a href="%s" data-wa="general" target="_blank" rel="noopener noreferrer">Start a WhatsApp chat</a></p></div></div>
      <div class="card"><h3>What happens next?</h3><ol class="plain-list"><li>We review your enquiry.</li><li>We contact you to understand your goals.</li><li>You receive a clear proposal.</li></ol></div>
    </aside>
  </div>
</section>
""" % (ind_html, bud_html, svc_html, icon("phone"), SITE["tel"], SITE["phone"], icon("mail"), SITE["email"], SITE["email"], icon("chat"), SITE["wa"])
    write_page("contact.html", "contact", "Contact BusinessLift | Get a Free Digital Marketing Consultation",
               "Contact BusinessLift by phone, email, WhatsApp or the enquiry form to discuss your business goals and get a free consultation.",
               body, scripts=("forms.js",), label="Contact")


def legal_page(filename, label, title, desc, intro, sections):
    secs = "\n".join("<h2>%s</h2>%s" % (e(h), t) for h, t in sections)
    body = page_hero(label, title, "Starter document for BusinessLift. Review and edit before publishing.") + """
<section class="section"><div class="container">
  <div class="notice"><p><strong>Starter template, not legal advice.</strong> This page is an editable starting point and does not constitute legal advice. Have it reviewed against BusinessLift's actual practices, and by a qualified professional, before relying on it.</p></div>
  <div class="prose">
    <p><strong>Last updated:</strong> [add date]</p>
    <p>%s</p>
    %s
    <h2>Contact</h2>
    <p>Questions about this page? Email <a href="mailto:%s">%s</a> or call <a href="tel:%s">%s</a>.</p>
  </div>
</div></section>
""" % (e(intro), secs, SITE["email"], SITE["email"], SITE["tel"], SITE["phone"])
    write_page(filename, "", title + " | BusinessLift", desc, body, label=label)


def build_legal():
    legal_page("privacy-policy.html", "Privacy Policy", "Privacy Policy", "BusinessLift's privacy policy: what information is collected and how enquiries, WhatsApp and email communication are handled.",
               "This Privacy Policy explains how BusinessLift (&ldquo;we&rdquo;) handles information when you use this website or contact us. [Edit to match your real practices.]".replace("&ldquo;", "“").replace("&rdquo;", "”"),
               [("Information we collect", "<p>We collect information you choose to give us, such as your name, business name, phone number, email address, industry, services of interest, budget range and message. [Add any other data you collect.]</p>"),
                ("How contact-form enquiries are processed", "<p>[Choose one and delete the other.] <em>Option A, without a connected service:</em> the form prepares a message that you send yourself by WhatsApp or email; the website does not transmit your details to a server. <em>Option B, with a form service:</em> your details are sent to [provider name] and delivered to BusinessLift so we can respond.</p>"),
                ("Communication through WhatsApp or email", "<p>If you contact us by WhatsApp or email, we receive the information you send and use it to reply. Those services have their own privacy practices that we do not control.</p>"),
                ("Analytics", "<p>[If enabled] We may use analytics tools to understand how the website is used. [Name the tool, what it collects and how to opt out. If none is used, say so.]</p>"),
                ("Third-party services", "<p>This site loads fonts from Google Fonts. [List any other third-party services, such as analytics, form providers or embedded content.]</p>"),
                ("How we use your information", "<p>We use enquiry information to respond to you, prepare proposals and provide requested services. [Add other uses.]</p>"),
                ("Data retention", "<p>We keep enquiry information only as long as needed for the purposes above or as required by law. [State your actual retention period.]</p>"),
                ("Your requests", "<p>You may ask us to access, correct or delete the information you have shared by contacting us using the details below. [Review against applicable Indian law and your practices.]</p>")])
    legal_page("terms.html", "Terms & Conditions", "Terms & Conditions", "BusinessLift's website terms and conditions covering services, quotations, intellectual property and limitation of liability.",
               "These Terms &amp; Conditions describe the basis on which BusinessLift provides information and services through this website. [Edit to match your real practices.]".replace("&amp;", "&"),
               [("Terms of service", "<p>Use of this website and engagement of BusinessLift's services are subject to these terms and to any written proposal or agreement we sign with you. [Add details.]</p>"),
                ("Services and scope", "<p>The scope, deliverables, timelines and fees for each engagement are set out in a written quotation or agreement. Anything outside that scope is quoted separately.</p>"),
                ("Quotations and payments", "<p>Pricing depends on goals, scope, deliverables and campaign requirements. Advertising spend, third-party subscriptions and applicable taxes are quoted separately where relevant. [Add payment terms.]</p>"),
                ("No guarantee of results", "<p>Digital marketing outcomes depend on many factors outside our control, including competition, platform policies and market conditions. We do not guarantee rankings, lead volumes, sales or revenue.</p>"),
                ("Client responsibilities", "<p>Clients are responsible for providing accurate information, timely approvals and the rights to any materials they supply.</p>"),
                ("Intellectual property", "<p>[Define ownership of deliverables, when it transfers, and any licensing of third-party assets.] The BusinessLift name, logo and website content remain our property.</p>"),
                ("Third-party platforms", "<p>Services may rely on third-party platforms (such as Google and Meta) whose terms and policies we do not control.</p>"),
                ("Limitation of liability", "<p>[Add a limitation of liability clause reviewed by a qualified professional.]</p>"),
                ("Governing law", "<p>[State the governing law and jurisdiction after professional review.]</p>"),
                ("Changes to these terms", "<p>We may update these terms from time to time. The date at the top shows when they were last updated.</p>")])


def write_sitemap_robots():
    today = date.today().isoformat()
    urls = ["index.html", "about.html", "services.html", "industries.html", "portfolio.html", "case-studies.html",
            "pricing.html", "blog.html", "contact.html", "privacy-policy.html", "terms.html"]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        loc = SITE["base"] + ("/" if u == "index.html" else "/" + u)
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod></url>" % (loc, today))
    lines.append("</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE["base"])
    print("wrote sitemap.xml, robots.txt")


if __name__ == "__main__":
    build_home(); build_about(); build_services(); build_industries(); build_portfolio(); build_case_studies()
    build_pricing(); build_blog(); build_blog_template(); build_contact(); build_legal(); write_sitemap_robots()
