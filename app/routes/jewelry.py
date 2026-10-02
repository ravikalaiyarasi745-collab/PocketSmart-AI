from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/jewelry",
    tags=["Jewelry Budget Planner"],
)


@router.get("/", response_class=HTMLResponse)
def jewelry_planner():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSmart AI - Jewelry Budget Planner</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f8f5ff;
                color: #222;
            }

            .header {
                background: linear-gradient(135deg, #6a1b9a, #8e24aa);
                color: white;
                text-align: center;
                padding: 30px 20px;
            }

            .header h1 {
                margin: 0 0 8px;
                font-size: 32px;
            }

            .header p {
                margin: 0;
                font-size: 16px;
            }

            .container {
                max-width: 900px;
                margin: 30px auto;
                padding: 0 20px;
            }

            .card {
                background: white;
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 25px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }

            .card h2 {
                margin-top: 0;
                color: #6a1b9a;
            }

            .form-group {
                margin-bottom: 18px;
            }

            label {
                display: block;
                font-weight: bold;
                margin-bottom: 7px;
            }

            input,
            select,
            textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 15px;
            }

            textarea {
                min-height: 100px;
                resize: vertical;
            }

            button {
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 8px;
                background: #6a1b9a;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #4a148c;
            }

            .result {
                display: none;
            }

            .summary {
                background: #f3e5f5;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            .recommendation {
                background: #fafafa;
                border-left: 5px solid #6a1b9a;
                padding: 15px;
                margin: 12px 0;
                border-radius: 6px;
            }

            .recommendation h3 {
                margin-top: 0;
                color: #6a1b9a;
            }

            .back {
                display: inline-block;
                margin-top: 10px;
                text-decoration: none;
                color: #6a1b9a;
                font-weight: bold;
            }

            .note {
                background: #fff8e1;
                border-left: 5px solid #ffb300;
                padding: 15px;
                margin-top: 15px;
                border-radius: 6px;
            }
        </style>
    </head>

    <body>

        <header class="header">
            <h1>💎 PocketSmart AI</h1>
            <p>Jewelry Budget Planner & Recommendations</p>
        </header>

        <div class="container">

            <div class="card">
                <h2>💎 Plan Your Jewelry Purchase</h2>

                <form id="jewelryForm">

                    <div class="form-group">
                        <label for="budget">Budget (₹)</label>
                        <input
                            type="number"
                            id="budget"
                            min="1000"
                            placeholder="Example: 50000"
                            required
                        >
                    </div>

                    <div class="form-group">
                        <label for="occasion">Occasion</label>
                        <select id="occasion">
                            <option>Wedding</option>
                            <option>Engagement</option>
                            <option>Birthday</option>
                            <option>Anniversary</option>
                            <option>Festival</option>
                            <option>Daily Wear</option>
                            <option>Party</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="jewelryType">Jewelry Type</label>
                        <select id="jewelryType">
                            <option>Necklace</option>
                            <option>Earrings</option>
                            <option>Ring</option>
                            <option>Bangles</option>
                            <option>Chain</option>
                            <option>Bracelet</option>
                            <option>Complete Set</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="material">Preferred Material</label>
                        <select id="material">
                            <option>Gold</option>
                            <option>Silver</option>
                            <option>Diamond</option>
                            <option>Platinum</option>
                            <option>Artificial / Fashion Jewelry</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="style">Style</label>
                        <select id="style">
                            <option>Traditional</option>
                            <option>Modern</option>
                            <option>Minimalist</option>
                            <option>Bridal</option>
                            <option>Party Wear</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="outfit">Outfit / Dress Style</label>
                        <input
                            type="text"
                            id="outfit"
                            placeholder="Example: Red silk saree"
                        >
                    </div>

                    <div class="form-group">
                        <label for="requirements">Additional Requirements</label>
                        <textarea
                            id="requirements"
                            placeholder="Example: Matching earrings, lightweight design, elegant look"
                        ></textarea>
                    </div>

                    <button type="submit">
                        💎 Generate Jewelry Recommendations
                    </button>

                </form>
            </div>

            <div class="card result" id="result">

                <h2>✨ Your Jewelry Plan</h2>

                <div class="summary" id="summary"></div>

                <div id="recommendations"></div>

                <div class="note">
                    💡 Prices for jewelry can vary based on material,
                    weight, making charges, taxes, gemstones and seller.
                    Use this planner as a budgeting guide.
                </div>

                <a href="/" class="back">
                    ← Back to PocketSmart AI
                </a>

            </div>

        </div>

        <script>
            document
                .getElementById("jewelryForm")
                .addEventListener("submit", function(event) {

                    event.preventDefault();

                    const budget = Number(
                        document.getElementById("budget").value
                    );

                    const occasion =
                        document.getElementById("occasion").value;

                    const jewelryType =
                        document.getElementById("jewelryType").value;

                    const material =
                        document.getElementById("material").value;

                    const style =
                        document.getElementById("style").value;

                    const outfit =
                        document.getElementById("outfit").value;

                    const requirements =
                        document.getElementById("requirements").value;

                    if (!budget || budget < 1000) {
                        alert("Please enter a valid budget of at least ₹1,000.");
                        return;
                    }

                    const jewelryBudget = budget * 0.75;
                    const matchingBudget = budget * 0.10;
                    const reserveBudget = budget * 0.15;

                    let recommendations = [];

                    if (material === "Gold") {
                        recommendations.push(
                            "Consider a lightweight gold design to keep the purchase within budget."
                        );
                    } else if (material === "Diamond") {
                        recommendations.push(
                            "Consider smaller diamond pieces or diamond-accented designs for better budget control."
                        );
                    } else if (material === "Silver") {
                        recommendations.push(
                            "Silver jewelry can provide a wider range of designs within the available budget."
                        );
                    } else if (material === "Platinum") {
                        recommendations.push(
                            "For platinum, prioritize a simple design and compare making charges carefully."
                        );
                    } else {
                        recommendations.push(
                            "Fashion jewelry can provide more variety while keeping most of the budget available."
                        );
                    }

                    if (occasion === "Wedding" ||
                        occasion === "Engagement") {
                        recommendations.push(
                            "Choose a design that complements the occasion while keeping matching accessories within the planned budget."
                        );
                    } else if (occasion === "Daily Wear") {
                        recommendations.push(
                            "For daily wear, prioritize lightweight, comfortable and durable designs."
                        );
                    } else {
                        recommendations.push(
                            "Select a design that matches the occasion and can also be reused for similar events."
                        );
                    }

                    if (style === "Traditional" ||
                        style === "Bridal") {
                        recommendations.push(
                            "Traditional designs can pair well with sarees and ethnic outfits."
                        );
                    } else if (style === "Minimalist") {
                        recommendations.push(
                            "Minimal designs can work well for both casual and formal outfits."
                        );
                    } else {
                        recommendations.push(
                            "Modern and party-wear designs can be matched with contemporary outfits."
                        );
                    }

                    if (outfit.trim() !== "") {
                        recommendations.push(
                            "Outfit considered: " + outfit
                        );
                    }

                    if (requirements.trim() !== "") {
                        recommendations.push(
                            "Your requirements: " + requirements
                        );
                    }

                    document.getElementById("summary").innerHTML = `
                        <strong>Budget:</strong> ₹${budget.toFixed(2)}<br>
                        <strong>Occasion:</strong> ${occasion}<br>
                        <strong>Jewelry:</strong> ${jewelryType}<br>
                        <strong>Material:</strong> ${material}<br>
                        <strong>Style:</strong> ${style}<br><br>

                        <strong>Suggested Jewelry Budget:</strong>
                        ₹${jewelryBudget.toFixed(2)}<br>

                        <strong>Matching Accessories:</strong>
                        ₹${matchingBudget.toFixed(2)}<br>

                        <strong>Reserve:</strong>
                        ₹${reserveBudget.toFixed(2)}
                    `;

                    const recommendationHTML =
                        recommendations
                            .map((item, index) => `
                                <div class="recommendation">
                                    <h3>Recommendation ${index + 1}</h3>
                                    <p>${item}</p>
                                </div>
                            `)
                            .join("");

                    document.getElementById("recommendations").innerHTML =
                        recommendationHTML;

                    document.getElementById("result").style.display = "block";

                    document.getElementById("result")
                        .scrollIntoView({
                            behavior: "smooth"
                        });
                });
        </script>

    </body>
    </html>
    """