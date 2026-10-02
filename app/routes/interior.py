from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix="/interior",
    tags=["Home Interior Planner"],
)


@router.get("/", response_class=HTMLResponse)
def interior_planner():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>PocketSmart AI - Home Interior Planner</title>

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
                background: #111827;
                color: white;
                padding: 22px 40px;
            }

            .header h1 {
                margin: 0;
                font-size: 28px;
            }

            .header p {
                margin: 6px 0 0;
                color: #d1d5db;
            }

            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
            }

            h2 {
                margin-top: 0;
                color: #111827;
            }

            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }

            .field {
                display: flex;
                flex-direction: column;
            }

            .field.full {
                grid-column: 1 / -1;
            }

            label {
                font-weight: bold;
                margin-bottom: 8px;
            }

            input,
            select,
            textarea {
                width: 100%;
                padding: 12px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 15px;
            }

            textarea {
                min-height: 110px;
                resize: vertical;
            }

            .button {
                margin-top: 25px;
                width: 100%;
                border: none;
                padding: 14px;
                background: #2563eb;
                color: white;
                border-radius: 9px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }

            .button:hover {
                background: #1d4ed8;
            }

            .result {
                margin-top: 30px;
                display: none;
            }

            .recommendation {
                background: #f8fafc;
                border-left: 5px solid #2563eb;
                padding: 18px;
                margin-bottom: 15px;
                border-radius: 8px;
            }

            .recommendation h3 {
                margin-top: 0;
            }

            .back {
                display: inline-block;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }

            @media (max-width: 700px) {
                .grid {
                    grid-template-columns: 1fr;
                }

                .field.full {
                    grid-column: auto;
                }

                .header {
                    padding: 20px;
                }
            }
        </style>
    </head>

    <body>

        <header class="header">
            <h1>🏠 PocketSmart AI</h1>
            <p>Home Interior Budget Planner</p>
        </header>

        <main class="container">

            <div class="card">

                <h2>Plan Your Home Interior</h2>

                <p>
                    Enter your budget and preferences to get
                    budget-friendly interior recommendations.
                </p>

                <form id="interiorForm">

                    <div class="grid">

                        <div class="field">
                            <label for="budget">
                                Budget (₹)
                            </label>

                            <input
                                type="number"
                                id="budget"
                                min="1"
                                placeholder="Example: 100000"
                                required
                            >
                        </div>

                        <div class="field">
                            <label for="room">
                                Room Type
                            </label>

                            <select id="room" required>
                                <option value="">Select room</option>
                                <option value="Living Room">
                                    Living Room
                                </option>
                                <option value="Bedroom">
                                    Bedroom
                                </option>
                                <option value="Kitchen">
                                    Kitchen
                                </option>
                                <option value="Home Office">
                                    Home Office
                                </option>
                                <option value="Full Home">
                                    Full Home
                                </option>
                            </select>
                        </div>

                        <div class="field">
                            <label for="style">
                                Interior Style
                            </label>

                            <select id="style" required>
                                <option value="">Select style</option>
                                <option value="Modern">
                                    Modern
                                </option>
                                <option value="Minimalist">
                                    Minimalist
                                </option>
                                <option value="Traditional">
                                    Traditional
                                </option>
                                <option value="Luxury">
                                    Luxury
                                </option>
                                <option value="Scandinavian">
                                    Scandinavian
                                </option>
                            </select>
                        </div>

                        <div class="field">
                            <label for="platform">
                                Preferred Platform
                            </label>

                            <select id="platform">
                                <option value="Any">
                                    Any
                                </option>
                                <option value="IKEA">
                                    IKEA
                                </option>
                                <option value="Amazon">
                                    Amazon
                                </option>
                            </select>
                        </div>

                        <div class="field full">

                            <label for="requirements">
                                Additional Requirements
                            </label>

                            <textarea
                                id="requirements"
                                placeholder="Example: Need sofa, TV unit and storage with a modern look."
                            ></textarea>

                        </div>

                    </div>

                    <button
                        type="submit"
                        class="button"
                    >
                        Generate Recommendations
                    </button>

                </form>

                <div
                    id="result"
                    class="result"
                ></div>

                <a
                    href="/"
                    class="back"
                >
                    ← Back to PocketSmart AI
                </a>

            </div>

        </main>

        <script>

            const form = document.getElementById("interiorForm");
            const result = document.getElementById("result");

            form.addEventListener("submit", function(event) {

                event.preventDefault();

                const budget = Number(
                    document.getElementById("budget").value
                );

                const room =
                    document.getElementById("room").value;

                const style =
                    document.getElementById("style").value;

                const platform =
                    document.getElementById("platform").value;

                const requirements =
                    document.getElementById("requirements").value;

                if (!budget || budget <= 0) {
                    alert("Please enter a valid budget.");
                    return;
                }

                let sofaBudget = budget * 0.30;
                let storageBudget = budget * 0.20;
                let lightingBudget = budget * 0.15;
                let decorBudget = budget * 0.15;
                let remainingBudget = budget * 0.20;

                result.style.display = "block";

                result.innerHTML = `

                    <h2>🏠 Interior Recommendations</h2>

                    <div class="recommendation">

                        <h3>Room & Style</h3>

                        <p>
                            <strong>Room:</strong> ${room}
                        </p>

                        <p>
                            <strong>Style:</strong> ${style}
                        </p>

                        <p>
                            <strong>Preferred Platform:</strong>
                            ${platform}
                        </p>

                    </div>

                    <div class="recommendation">

                        <h3>💰 Suggested Budget Allocation</h3>

                        <p>
                            Sofa / Main Furniture:
                            ₹${sofaBudget.toFixed(0)}
                        </p>

                        <p>
                            Storage:
                            ₹${storageBudget.toFixed(0)}
                        </p>

                        <p>
                            Lighting:
                            ₹${lightingBudget.toFixed(0)}
                        </p>

                        <p>
                            Decor:
                            ₹${decorBudget.toFixed(0)}
                        </p>

                        <p>
                            Remaining / Contingency:
                            ₹${remainingBudget.toFixed(0)}
                        </p>

                    </div>

                    <div class="recommendation">

                        <h3>🤖 PocketSmart AI Suggestion</h3>

                        <p>
                            For a ${style.toLowerCase()} ${room.toLowerCase()},
                            prioritize essential furniture first and keep
                            approximately 20% of your budget as a contingency
                            amount.
                        </p>

                        ${
                            requirements
                            ? `<p><strong>Your requirement:</strong>
                               ${requirements}</p>`
                            : ""
                        }

                    </div>

                `;

                result.scrollIntoView({
                    behavior: "smooth"
                });

            });

        </script>

    </body>
    </html>
    """