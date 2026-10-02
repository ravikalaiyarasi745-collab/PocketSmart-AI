from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/party",
    tags=["Party Budget Planner"],
)


@router.get("/", response_class=HTMLResponse)
def party_planner():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PocketSmart AI - Party Budget Planner</title>

        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                color: #1f2937;
            }

            .header {
                background: linear-gradient(135deg, #7c3aed, #ec4899);
                color: white;
                padding: 35px 20px;
                text-align: center;
            }

            .header h1 {
                margin: 0 0 8px;
                font-size: 32px;
            }

            .header p {
                margin: 0;
                font-size: 17px;
            }

            .container {
                max-width: 900px;
                margin: 35px auto;
                padding: 0 20px;
            }

            .card {
                background: white;
                border-radius: 16px;
                padding: 28px;
                margin-bottom: 25px;
                box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
            }

            .card h2 {
                margin-top: 0;
                color: #7c3aed;
            }

            label {
                display: block;
                font-weight: bold;
                margin-top: 18px;
                margin-bottom: 7px;
            }

            input,
            select,
            textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #d1d5db;
                border-radius: 9px;
                font-size: 15px;
            }

            textarea {
                min-height: 100px;
                resize: vertical;
            }

            button {
                width: 100%;
                margin-top: 24px;
                padding: 14px;
                border: none;
                border-radius: 10px;
                background: #7c3aed;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }

            button:hover {
                background: #6d28d9;
            }

            .results {
                display: none;
            }

            .summary {
                background: #f5f3ff;
                border-left: 5px solid #7c3aed;
                padding: 18px;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            .budget-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 15px;
            }

            .budget-item {
                background: #f9fafb;
                border-radius: 12px;
                padding: 18px;
                border: 1px solid #e5e7eb;
            }

            .budget-item h3 {
                margin: 0 0 8px;
                font-size: 16px;
                color: #374151;
            }

            .budget-item p {
                margin: 0;
                font-size: 22px;
                font-weight: bold;
                color: #7c3aed;
            }

            .recommendation {
                background: #ecfdf5;
                border-left: 5px solid #10b981;
                padding: 16px;
                border-radius: 10px;
                margin-top: 15px;
            }

            .warning {
                background: #fff7ed;
                border-left: 5px solid #f97316;
                padding: 16px;
                border-radius: 10px;
                margin-top: 15px;
            }

            .back {
                display: inline-block;
                margin-top: 10px;
                color: #7c3aed;
                text-decoration: none;
                font-weight: bold;
            }

            @media (max-width: 600px) {
                .header h1 {
                    font-size: 25px;
                }

                .card {
                    padding: 20px;
                }
            }
        </style>
    </head>

    <body>

        <div class="header">
            <h1>🎉 PocketSmart AI</h1>
            <p>Party Budget Planner & Recommendations</p>
        </div>

        <div class="container">

            <div class="card">
                <h2>🎊 Plan Your Party</h2>

                <form id="partyForm">

                    <label for="budget">Total Budget (₹)</label>
                    <input
                        type="number"
                        id="budget"
                        min="1"
                        placeholder="Example: 50000"
                        required
                    >

                    <label for="guests">Number of Guests</label>
                    <input
                        type="number"
                        id="guests"
                        min="1"
                        placeholder="Example: 50"
                        required
                    >

                    <label for="occasion">Occasion</label>
                    <select id="occasion">
                        <option>Birthday Party</option>
                        <option>Wedding Reception</option>
                        <option>Engagement</option>
                        <option>Anniversary</option>
                        <option>Corporate Event</option>
                        <option>Family Function</option>
                    </select>

                    <label for="food">Food Preference</label>
                    <select id="food">
                        <option>Vegetarian</option>
                        <option>Non-Vegetarian</option>
                        <option>Mixed</option>
                    </select>

                    <label for="venue">Venue Preference</label>
                    <select id="venue">
                        <option>Home</option>
                        <option>Restaurant</option>
                        <option>Hotel</option>
                        <option>Party Hall</option>
                        <option>Outdoor Venue</option>
                    </select>

                    <label for="requirements">Special Requirements</label>
                    <textarea
                        id="requirements"
                        placeholder="Example: Cake, DJ, decorations, photography..."
                    ></textarea>

                    <button type="submit">
                        Generate Party Recommendations 🎉
                    </button>

                </form>
            </div>

            <div class="card results" id="results">

                <h2>🤖 AI-Style Party Recommendations</h2>

                <div class="summary" id="summary"></div>

                <div class="budget-grid">

                    <div class="budget-item">
                        <h3>🍽️ Food</h3>
                        <p id="foodBudget"></p>
                    </div>

                    <div class="budget-item">
                        <h3>🏨 Venue</h3>
                        <p id="venueBudget"></p>
                    </div>

                    <div class="budget-item">
                        <h3>🎈 Decorations</h3>
                        <p id="decorBudget"></p>
                    </div>

                    <div class="budget-item">
                        <h3>🎵 Entertainment</h3>
                        <p id="entertainmentBudget"></p>
                    </div>

                    <div class="budget-item">
                        <h3>📸 Photography</h3>
                        <p id="photoBudget"></p>
                    </div>

                    <div class="budget-item">
                        <h3>💰 Emergency Reserve</h3>
                        <p id="reserveBudget"></p>
                    </div>

                </div>

                <div class="recommendation" id="recommendation"></div>

                <div class="warning" id="guestAdvice"></div>

                <a href="/" class="back">← Back to PocketSmart AI</a>

            </div>

        </div>

        <script>
            document
                .getElementById("partyForm")
                .addEventListener("submit", function(event) {

                    event.preventDefault();

                    const budget =
                        Number(document.getElementById("budget").value);

                    const guests =
                        Number(document.getElementById("guests").value);

                    const occasion =
                        document.getElementById("occasion").value;

                    const food =
                        document.getElementById("food").value;

                    const venue =
                        document.getElementById("venue").value;

                    const requirements =
                        document.getElementById("requirements").value.trim();

                    if (budget <= 0 || guests <= 0) {
                        alert("Please enter a valid budget and guest count.");
                        return;
                    }

                    const foodBudget = budget * 0.35;
                    const venueBudget = budget * 0.20;
                    const decorBudget = budget * 0.12;
                    const entertainmentBudget = budget * 0.10;
                    const photoBudget = budget * 0.08;
                    const reserveBudget = budget * 0.15;

                    const perGuest =
                        budget / guests;

                    document.getElementById("summary").innerHTML =
                        "<strong>Party Summary</strong><br>" +
                        occasion +
                        " for " +
                        guests +
                        " guests with a total budget of ₹" +
                        budget.toLocaleString("en-IN") +
                        ". Food preference: " +
                        food +
                        ". Venue: " +
                        venue +
                        ".";

                    document.getElementById("foodBudget").textContent =
                        "₹" + Math.round(foodBudget).toLocaleString("en-IN");

                    document.getElementById("venueBudget").textContent =
                        "₹" + Math.round(venueBudget).toLocaleString("en-IN");

                    document.getElementById("decorBudget").textContent =
                        "₹" + Math.round(decorBudget).toLocaleString("en-IN");

                    document.getElementById("entertainmentBudget").textContent =
                        "₹" + Math.round(entertainmentBudget).toLocaleString("en-IN");

                    document.getElementById("photoBudget").textContent =
                        "₹" + Math.round(photoBudget).toLocaleString("en-IN");

                    document.getElementById("reserveBudget").textContent =
                        "₹" + Math.round(reserveBudget).toLocaleString("en-IN");

                    let recommendationText =
                        "Keep food within ₹" +
                        Math.round(foodBudget).toLocaleString("en-IN") +
                        " and compare catering options before confirming. " +
                        "Reserve around ₹" +
                        Math.round(reserveBudget).toLocaleString("en-IN") +
                        " for unexpected expenses.";

                    if (venue === "Home") {
                        recommendationText +=
                            " Since you selected a home venue, you can redirect some venue savings toward food or decorations.";
                    }

                    if (venue === "Hotel" || venue === "Party Hall") {
                        recommendationText +=
                            " Venue costs can increase quickly, so confirm package inclusions such as food, seating, decoration and service charges.";
                    }

                    if (requirements) {
                        recommendationText +=
                            " Your special requirements: " +
                            requirements +
                            ".";
                    }

                    document.getElementById("recommendation").innerHTML =
                        "<strong>💡 Recommendation</strong><br>" +
                        recommendationText;

                    let guestMessage =
                        "Your estimated budget per guest is ₹" +
                        Math.round(perGuest).toLocaleString("en-IN") +
                        ".";

                    if (perGuest < 500) {
                        guestMessage +=
                            " Consider a simple menu and low-cost decorations to stay within budget.";
                    } else if (perGuest < 1500) {
                        guestMessage +=
                            " You have a moderate per-guest budget with room for a balanced food and decoration plan.";
                    } else {
                        guestMessage +=
                            " You have a higher per-guest budget, allowing more flexibility for venue, food and entertainment.";
                    }

                    document.getElementById("guestAdvice").innerHTML =
                        "<strong>👥 Guest Budget Insight</strong><br>" +
                        guestMessage;

                    document.getElementById("results").style.display = "block";

                    document.getElementById("results")
                        .scrollIntoView({
                            behavior: "smooth"
                        });
                });
        </script>

    </body>
    </html>
    """