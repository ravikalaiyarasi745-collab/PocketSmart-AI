from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Income, Expense


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/", response_class=HTMLResponse)
def dashboard(db: Session = Depends(get_db)):

    incomes = (
        db.query(Income)
        .filter(Income.user_id == 1)
        .order_by(Income.id.desc())
        .all()
    )

    expenses = (
        db.query(Expense)
        .filter(Expense.user_id == 1)
        .order_by(Expense.id.desc())
        .all()
    )

    total_income = sum(income.amount for income in incomes)
    total_expenses = sum(expense.amount for expense in expenses)
    balance = total_income - total_expenses

    transactions = []

    for income in incomes:
        transactions.append({
            "type": "Income",
            "category": income.category,
            "amount": income.amount,
            "description": income.description or "-",
            "id": income.id,
        })

    for expense in expenses:
        transactions.append({
            "type": "Expense",
            "category": expense.category,
            "amount": expense.amount,
            "description": expense.description or "-",
            "id": expense.id,
        })

    transactions.sort(
        key=lambda transaction: transaction["id"],
        reverse=True,
    )

    transaction_rows = ""

    for transaction in transactions[:10]:

        if transaction["type"] == "Income":
            amount_display = f"+₹{transaction['amount']:.2f}"
            amount_class = "income"
        else:
            amount_display = f"-₹{transaction['amount']:.2f}"
            amount_class = "expense"

        transaction_rows += f"""
        <tr>
            <td>{transaction["type"]}</td>
            <td>{transaction["category"]}</td>
            <td>{transaction["description"]}</td>
            <td class="{amount_class}">
                {amount_display}
            </td>
        </tr>
        """

    if not transaction_rows:
        transaction_rows = """
        <tr>
            <td colspan="4">
                No transactions yet.
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>PocketSmart AI - Dashboard</title>

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
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}

            .header h1 {{
                margin: 0;
            }}

            .container {{
                padding: 40px;
            }}

            .welcome {{
                margin-bottom: 30px;
            }}

            .cards {{
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20px;
            }}

            .card {{
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }}

            .card h3 {{
                margin-top: 0;
                color: #555;
            }}

            .amount {{
                font-size: 30px;
                font-weight: bold;
            }}

            .income {{
                color: #16a34a;
                font-weight: bold;
            }}

            .expense {{
                color: #dc2626;
                font-weight: bold;
            }}

            .balance {{
                color: #2563eb;
            }}

            .section {{
                margin-top: 35px;
                background: white;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }}

            .button {{
                display: inline-block;
                margin-top: 15px;
                padding: 12px 20px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }}

            .button:hover {{
                background: #1d4ed8;
            }}

            .button.green {{
                background: #16a34a;
            }}

            .button.green:hover {{
                background: #15803d;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }}

            th,
            td {{
                padding: 14px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}

            th {{
                background: #f8fafc;
            }}

            .actions {{
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
            }}

            @media (max-width: 800px) {{

                .cards {{
                    grid-template-columns: 1fr;
                }}

                .container {{
                    padding: 20px;
                }}

                .header {{
                    padding: 20px;
                }}

                table {{
                    font-size: 14px;
                }}

            }}

        </style>

    </head>

    <body>

        <div class="header">

            <h1>💰 PocketSmart AI</h1>

            <span>Dashboard</span>

        </div>


        <div class="container">

            <div class="welcome">

                <h2>
                    Welcome to PocketSmart AI 👋
                </h2>

                <p>
                    Manage your money smarter with
                    AI-powered financial insights.
                </p>

            </div>


            <div class="cards">

                <div class="card">

                    <h3>Total Income</h3>

                    <div class="amount income">
                        ₹{total_income:.2f}
                    </div>

                </div>


                <div class="card">

                    <h3>Total Expenses</h3>

                    <div class="amount expense">
                        ₹{total_expenses:.2f}
                    </div>

                </div>


                <div class="card">

                    <h3>Remaining Balance</h3>

                    <div class="amount balance">
                        ₹{balance:.2f}
                    </div>

                </div>

            </div>


            <div class="section">

                <h2>📊 Recent Transactions</h2>

                <table>

                    <thead>

                        <tr>
                            <th>Type</th>
                            <th>Category</th>
                            <th>Description</th>
                            <th>Amount</th>
                        </tr>

                    </thead>

                    <tbody>

                        {transaction_rows}

                    </tbody>

                </table>


                <div class="actions">

                    <a
                        href="/dashboard/income/"
                        class="button green"
                    >
                        ➕ Add Income
                    </a>

                    <a
                        href="/dashboard/expenses/"
                        class="button"
                    >
                        ➕ Add Expense
                    </a>

                </div>

            </div>


            <div class="section">

                <h2>🤖 AI Financial Assistant</h2>

                <p>
                    Get personalized recommendations based
                    on your spending habits and budget.
                </p>

                <a
                    href="/recommendations/health"
                    class="button"
                >
                    Check AI Service
                </a>
                <a
                    href="/assistant/"
                    class="button"
                >
                    🤖 Open AI Assistant
                </a>

            </div>

        </div>

    </body>

    </html>
    """