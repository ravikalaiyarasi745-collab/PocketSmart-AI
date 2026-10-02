from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Pages"])


@router.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSmart AI</title>

        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: Arial, sans-serif;
            }

            body {
                background: #f5f7fb;
                color: #222;
            }

            .navbar {
                background: #111827;
                color: white;
                padding: 18px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .logo {
                font-size: 24px;
                font-weight: bold;
            }

            .hero {
                min-height: 80vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                padding: 40px 20px;
            }

            .hero h1 {
                font-size: 52px;
                margin-bottom: 20px;
            }

            .hero p {
                font-size: 20px;
                color: #666;
                max-width: 650px;
                margin-bottom: 30px;
            }

            .button {
                display: inline-block;
                background: #2563eb;
                color: white;
                padding: 14px 28px;
                border-radius: 10px;
                text-decoration: none;
                font-size: 17px;
                font-weight: bold;
            }

            .button:hover {
                background: #1d4ed8;
            }

            .features {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                justify-content: center;
                padding: 30px;
            }

            .card {
                background: white;
                width: 280px;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }

            .card h3 {
                margin-bottom: 10px;
            }

            .card p {
                color: #666;
                line-height: 1.5;
            }
        </style>
    </head>

    <body>

        <nav class="navbar">
            <div class="logo">💰 PocketSmart AI</div>
            <div>AI Budget Assistant</div>
        </nav>

        <section class="hero">
            <h1>Smart Money Decisions with AI 🤖</h1>

            <p>
                PocketSmart AI helps you make smarter spending decisions,
                manage your budget and get personalized recommendations.
            </p>

            <a href="/docs" class="button">
                Get Started
            </a>
        </section>

        <section class="features">

            <div class="card">
                <h3>💰 Budget Planning</h3>
                <p>
                    Plan your spending and understand where your money goes.
                </p>
            </div>

            <div class="card">
                <h3>🤖 AI Recommendations</h3>
                <p>
                    Get intelligent recommendations based on your budget.
                </p>
            </div>

            <div class="card">
                <h3>📊 Smart Insights</h3>
                <p>
                    Understand your spending patterns with simple insights.
                </p>
            </div>

        </section>

    </body>
    </html>
    """