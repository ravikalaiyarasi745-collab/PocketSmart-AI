from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Income, Expense, Budget


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("/health")
def recommendations_health():
    return {
        "status": "ok",
        "service": "PocketSmart AI Recommendation Engine"
    }


@router.get("/", response_class=HTMLResponse)
def recommendations_page(db: Session = Depends(get_db)):

    user_id = 1

    incomes = (
        db.query(Income)
        .filter(Income.user_id == user_id)
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == user_id)
        .all()
    )

    budget = (
        db.query(Budget)
        .filter(Budget.user_id == user_id)
        .order_by(Budget.id.desc())
        .first()
    )

    total_income = sum(item.amount for item in incomes)
    total_expenses = sum(item.amount for item in expenses)

    balance = total_income - total_expenses

    budget_amount = budget.amount if budget else 0

    if budget_amount > 0:
        budget_remaining = budget_amount - total_expenses
        spending_percentage = (
            total_expenses / budget_amount
        ) * 100
    else:
        budget_remaining = 0
        spending_percentage = 0

    recommendations = []

    # Budget analysis
    if budget_amount == 0:

        recommendations.append(
            "💰 Set a monthly budget to track your spending more effectively."
        )

    elif spending_percentage >= 90:

        recommendations.append(
            "🚨 You have used more than 90% of your monthly budget. "
            "Consider reducing non-essential expenses."
        )

    elif spending_percentage >= 70:

        recommendations.append(
            "⚠️ You have used more than 70% of your monthly budget. "
            "Keep an eye on your remaining expenses."
        )

    else:

        recommendations.append(
            "✅ Your current spending is within your monthly budget."
        )

    # Saving recommendation
    if total_income > 0:

        savings_rate = (
            balance / total_income
        ) * 100

        if savings_rate >= 30:

            recommendations.append(
                "🌟 Your current balance is relatively high compared "
                "with your income. Consider saving or investing a portion "
                "of your remaining money."
            )

        elif savings_rate >= 10:

            recommendations.append(
                "👍 You are keeping some money after expenses. "
                "Try to increase your savings gradually."
            )

        else:

            recommendations.append(
                "💡 Your remaining balance is relatively low compared "
                "with your income. Review non-essential spending."
            )

    # Category analysis
    category_totals = {}

    for expense in expenses:

        category = expense.category

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense.amount
        )

    if category_totals:

        highest_category = max(
            category_totals,
            key=category_totals.get
        )

        highest_amount = category_totals[highest_category]

        recommendations.append(
            f"📊 Your highest spending category is "
            f"<strong>{highest_category}</strong> "
            f"with ₹{highest_amount:.2f} spent."
        )

    # General recommendation
    recommendations.append(
        "🤖 PocketSmart AI recommends reviewing your transactions "
        "regularly and setting realistic monthly spending limits."
    )

    recommendation_items = ""

    for recommendation in recommendations:

        recommendation_items += f"""
        <li>
            {recommendation}
        </li>
        """

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>PocketSmart AI - AI Recommendations</title>

        <style>

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
            }}

            .header {{
                background: #2563eb;
                color: white;
                padding: 25px 40px;
            }}

            .container {{
                max-width: 1000px;
                margin: auto;
                padding: 40px 20px;
            }}

            .card {{
                background: white;
                padding: 25px;
                margin-bottom: 25px;
                border-radius: 15px;
                box-shadow:
                    0 5px 20px rgba(0,0,0,0.08);
            }}

            .stats {{
                display: grid;
                grid-template-columns:
                    repeat(4, 1fr);
                gap: 15px;
            }}

            .stat {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 12px;
            }}

            .stat h3 {{
                margin-top: 0;
                color: #555;
            }}

            .amount {{
                font-size: 24px;
                font-weight: bold;
            }}

            .recommendations {{
                list-style: none;
                padding: 0;
            }}

            .recommendations li {{
                background: #f8fafc;
                margin-bottom: 12px;
                padding: 16px;
                border-radius: 10px;
                line-height: 1.5;
            }}

            .button {{
                display: inline-block;
                margin-top: 10px;
                padding: 12px 20px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}

            @media (max-width: 800px) {{

                .stats {{
                    grid-template-columns: 1fr 1fr;
                }}

            }}

            @media (max-width: 500px) {{

                .stats {{
                    grid-template-columns: 1fr;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🤖 PocketSmart AI</h1>

            <p>AI Financial Recommendations</p>

        </div>


        <div class="container">


            <div class="card">

                <h2>📊 Your Financial Summary</h2>

                <div class="stats">

                    <div class="stat">

                        <h3>Income</h3>

                        <div class="amount">
                            ₹{total_income:.2f}
                        </div>

                    </div>


                    <div class="stat">

                        <h3>Expenses</h3>

                        <div class="amount">
                            ₹{total_expenses:.2f}
                        </div>

                    </div>


                    <div class="stat">

                        <h3>Balance</h3>

                        <div class="amount">
                            ₹{balance:.2f}
                        </div>

                    </div>


                    <div class="stat">

                        <h3>Budget Used</h3>

                        <div class="amount">
                            {spending_percentage:.1f}%
                        </div>

                    </div>

                </div>

            </div>


            <div class="card">

                <h2>💡 AI Recommendations</h2>

                <ul class="recommendations">

                    {recommendation_items}

                </ul>

            </div>


            <a
                href="/dashboard/"
                class="button"
            >
                ← Back to Dashboard
            </a>


        </div>

    </body>

    </html>
    """