from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Income, Expense, Budget


router = APIRouter(
    prefix="/assistant",
    tags=["AI Assistant"],
)


def generate_answer(question, total_income, total_expenses, balance,
                    budget_amount, category_totals):

    question = question.lower().strip()

    if "income" in question or "earn" in question:
        return (
            f"💰 Your total recorded income is "
            f"₹{total_income:.2f}."
        )

    if (
        "expense" in question
        or "spend" in question
        or "spent" in question
    ):
        return (
            f"💸 Your total recorded expenses are "
            f"₹{total_expenses:.2f}."
        )

    if (
        "balance" in question
        or "left" in question
        or "remaining" in question
        or "money" in question
    ):
        return (
            f"💵 Your current remaining balance is "
            f"₹{balance:.2f}."
        )

    if (
        "budget" in question
        or "limit" in question
    ):
        if budget_amount > 0:
            remaining_budget = budget_amount - total_expenses

            return (
                f"📊 Your monthly budget is "
                f"₹{budget_amount:.2f}. "
                f"You have ₹{remaining_budget:.2f} "
                f"remaining in your budget."
            )

        return (
            "💡 You haven't set a monthly budget yet. "
            "Set one from the Budget Management page."
        )

    if (
        "highest" in question
        or "most" in question
        or "category" in question
    ):
        if category_totals:

            highest_category = max(
                category_totals,
                key=category_totals.get
            )

            highest_amount = category_totals[
                highest_category
            ]

            return (
                f"📊 Your highest spending category is "
                f"{highest_category}, with "
                f"₹{highest_amount:.2f} spent."
            )

        return (
            "📊 You don't have any expense records yet."
        )

    if (
        "save" in question
        or "saving" in question
    ):
        suggested_saving = balance * 0.20

        return (
            f"💡 Based on your current balance of "
            f"₹{balance:.2f}, a simple starting point "
            f"could be saving around ₹{suggested_saving:.2f} "
            f"(20% of your current balance)."
        )

    if "hello" in question or "hi" in question:
        return (
            "👋 Hello! I'm your PocketSmart AI Assistant. "
            "Ask me about your income, expenses, balance, "
            "budget, spending categories, or savings."
        )

    return (
        "🤖 I can help with your finances. Try asking: "
        "\"How much income do I have?\", "
        "\"How much did I spend?\", "
        "\"What is my balance?\", "
        "\"What is my budget?\", or "
        "\"Where am I spending the most?\""
    )


@router.get("/", response_class=HTMLResponse)
def assistant_page():

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>PocketSmart AI Assistant</title>

        <style>

            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
            }

            .header {
                background: #2563eb;
                color: white;
                padding: 25px 40px;
            }

            .container {
                max-width: 800px;
                margin: auto;
                padding: 40px 20px;
            }

            .card {
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow:
                    0 5px 20px rgba(0,0,0,0.08);
            }

            input {
                width: 100%;
                padding: 14px;
                box-sizing: border-box;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 15px 0;
            }

            button {
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }

            .examples {
                background: #f8fafc;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }

            .back {
                display: inline-block;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🤖 PocketSmart AI</h1>

            <p>Personal Financial Assistant</p>

        </div>

        <div class="container">

            <div class="card">

                <h2>💬 Ask your financial assistant</h2>

                <div class="examples">

                    <strong>Try asking:</strong>

                    <ul>

                        <li>How much income do I have?</li>
                        <li>How much did I spend?</li>
                        <li>What is my balance?</li>
                        <li>What is my budget?</li>
                        <li>Where am I spending the most?</li>
                        <li>How much should I save?</li>

                    </ul>

                </div>

                <form method="post" action="/assistant/ask">

                    <input
                        type="text"
                        name="question"
                        placeholder="Ask something about your finances..."
                        required
                    >

                    <button type="submit">
                        🤖 Ask AI
                    </button>

                </form>

                <a
                    class="back"
                    href="/dashboard/"
                >
                    ← Back to Dashboard
                </a>

            </div>

        </div>

    </body>

    </html>
    """


@router.post("/ask", response_class=HTMLResponse)
def ask_assistant(
    question: str = Form(...),
    db: Session = Depends(get_db),
):

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

    total_income = sum(
        item.amount for item in incomes
    )

    total_expenses = sum(
        item.amount for item in expenses
    )

    balance = total_income - total_expenses

    budget_amount = (
        budget.amount if budget else 0
    )

    category_totals = {}

    for expense in expenses:

        category = expense.category

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense.amount
        )

    answer = generate_answer(
        question,
        total_income,
        total_expenses,
        balance,
        budget_amount,
        category_totals,
    )

    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>PocketSmart AI Assistant</title>

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
                max-width: 800px;
                margin: auto;
                padding: 40px 20px;
            }}

            .card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow:
                    0 5px 20px rgba(0,0,0,0.08);
            }}

            .question {{
                background: #eff6ff;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
            }}

            .answer {{
                background: #f0fdf4;
                padding: 20px;
                border-radius: 10px;
                font-size: 18px;
                line-height: 1.6;
            }}

            .button {{
                display: inline-block;
                margin-top: 20px;
                padding: 12px 20px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>🤖 PocketSmart AI</h1>

            <p>Personal Financial Assistant</p>

        </div>

        <div class="container">

            <div class="card">

                <h2>💬 Your Question</h2>

                <div class="question">
                    {question}
                </div>

                <h2>🤖 AI Answer</h2>

                <div class="answer">
                    {answer}
                </div>

                <a
                    class="button"
                    href="/assistant/"
                >
                    Ask Another Question
                </a>

                <a
                    class="button"
                    href="/dashboard/"
                >
                    ← Dashboard
                </a>

            </div>

        </div>

    </body>

    </html>
    """