from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models import Budget, Expense


router = APIRouter(
    prefix="/dashboard/budget",
    tags=["Budget"],
)


@router.get("/", response_class=HTMLResponse)
def budget_page(db: Session = Depends(get_db)):

    current_month = datetime.now().strftime("%Y-%m")

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == 1,
            Budget.month == current_month
        )
        .order_by(Budget.id.desc())
        .first()
    )

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == 1)
        .all()
    )

    total_expenses = sum(expense.amount for expense in expenses)

    budget_amount = budget.amount if budget else 0
    remaining = budget_amount - total_expenses

    if budget_amount > 0:
        percentage = (total_expenses / budget_amount) * 100
    else:
        percentage = 0

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>PocketSmart AI - Budget</title>

        <style>

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
            }}

            .header {{
                background: #2563eb;
                color: white;
                padding: 20px 40px;
            }}

            .container {{
                padding: 40px;
                max-width: 900px;
                margin: auto;
            }}

            .card {{
                background: white;
                padding: 25px;
                margin-bottom: 20px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-top: 8px;
                margin-bottom: 15px;
                box-sizing: border-box;
                border: 1px solid #ddd;
                border-radius: 8px;
            }}

            button {{
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }}

            .stats {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }}

            .stat {{
                background: #f8fafc;
                padding: 20px;
                border-radius: 12px;
            }}

            .amount {{
                font-size: 25px;
                font-weight: bold;
            }}

            .green {{
                color: #16a34a;
            }}

            .red {{
                color: #dc2626;
            }}

            .blue {{
                color: #2563eb;
            }}

            .back {{
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                color: #2563eb;
            }}

            @media (max-width: 700px) {{
                .stats {{
                    grid-template-columns: 1fr;
                }}

                .container {{
                    padding: 20px;
                }}
            }}

        </style>

    </head>

    <body>

        <div class="header">
            <h1>💰 PocketSmart AI</h1>
            <p>Monthly Budget Management</p>
        </div>

        <div class="container">

            <div class="card">

                <h2>Set Monthly Budget</h2>

                <form method="post" action="/dashboard/budget/add">

                    <label>Budget Amount</label>

                    <input
                        type="number"
                        name="amount"
                        step="0.01"
                        min="1"
                        placeholder="Example: 20000"
                        required
                    >

                    <button type="submit">
                        💾 Save Budget
                    </button>

                </form>

            </div>


            <div class="card">

                <h2>📊 Current Month Budget</h2>

                <p>
                    Month: <strong>{current_month}</strong>
                </p>

                <div class="stats">

                    <div class="stat">

                        <h3>Budget</h3>

                        <div class="amount blue">
                            ₹{budget_amount:.2f}
                        </div>

                    </div>


                    <div class="stat">

                        <h3>Spent</h3>

                        <div class="amount red">
                            ₹{total_expenses:.2f}
                        </div>

                    </div>


                    <div class="stat">

                        <h3>Remaining</h3>

                        <div class="amount green">
                            ₹{remaining:.2f}
                        </div>

                    </div>

                </div>

                <p>
                    <strong>
                        Spending: {percentage:.1f}%
                    </strong>
                </p>

            </div>


            <a
                class="back"
                href="/dashboard/"
            >
                ← Back to Dashboard
            </a>

        </div>

    </body>

    </html>
    """


@router.post("/add", response_class=HTMLResponse)
def add_budget(
    amount: float = Form(...),
    db: Session = Depends(get_db),
):

    current_month = datetime.now().strftime("%Y-%m")

    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == 1,
            Budget.month == current_month
        )
        .order_by(Budget.id.desc())
        .first()
    )

    if budget:
        budget.amount = amount
    else:
        budget = Budget(
            user_id=1,
            amount=amount,
            month=current_month,
        )

        db.add(budget)

    db.commit()

    return """
    <!DOCTYPE html>
    <html>

    <head>

        <meta
            http-equiv="refresh"
            content="1; url=/dashboard/budget/"
        >

        <title>Budget Saved</title>

    </head>

    <body>

        <h2>✅ Budget saved successfully!</h2>

        <p>Redirecting...</p>

    </body>

    </html>
    """