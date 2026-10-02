from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Expense


router = APIRouter(
    prefix="/dashboard/expenses",
    tags=["Expenses"],
)


@router.get("/", response_class=HTMLResponse)
def expenses_page(db: Session = Depends(get_db)):

    expenses = (
        db.query(Expense)
        .order_by(Expense.id.desc())
        .all()
    )

    expense_rows = ""

    for expense in expenses:
        expense_rows += f"""
        <tr>
            <td>{expense.category}</td>
            <td>₹{expense.amount:.2f}</td>
            <td>{expense.description or "-"}</td>
        </tr>
        """

    if not expense_rows:
        expense_rows = """
        <tr>
            <td colspan="3">No expenses added yet.</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>PocketSmart AI - Expenses</title>

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
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
            }}

            .card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            }}

            input, select {{
                width: 100%;
                padding: 12px;
                margin: 8px 0 15px 0;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-sizing: border-box;
            }}

            button {{
                width: 100%;
                padding: 12px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }}

            button:hover {{
                background: #1d4ed8;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
            }}

            th, td {{
                padding: 14px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }}

            th {{
                background: #f8fafc;
            }}

            .back {{
                display: inline-block;
                margin-top: 20px;
                color: #2563eb;
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="header">
            <h1>💸 PocketSmart AI</h1>
            <p>Expense Management</p>
        </div>

        <div class="container">

            <div class="card">

                <h2>➕ Add New Expense</h2>

                <form action="/dashboard/expenses/add" method="post">

                    <label>Category</label>

                    <select name="category" required>
                        <option value="">Select Category</option>
                        <option value="Food">Food</option>
                        <option value="Travel">Travel</option>
                        <option value="Shopping">Shopping</option>
                        <option value="Bills">Bills</option>
                        <option value="Entertainment">Entertainment</option>
                        <option value="Education">Education</option>
                        <option value="Health">Health</option>
                        <option value="Other">Other</option>
                    </select>

                    <label>Amount</label>

                    <input
                        type="number"
                        name="amount"
                        step="0.01"
                        min="0"
                        placeholder="Enter amount"
                        required
                    >

                    <label>Description</label>

                    <input
                        type="text"
                        name="description"
                        placeholder="Example: Lunch"
                    >

                    <button type="submit">
                        Add Expense
                    </button>

                </form>

            </div>


            <div class="card">

                <h2>📋 Expense History</h2>

                <table>

                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Amount</th>
                            <th>Description</th>
                        </tr>
                    </thead>

                    <tbody>
                        {expense_rows}
                    </tbody>

                </table>

            </div>


            <a class="back" href="/dashboard/">
                ← Back to Dashboard
            </a>

        </div>

    </body>

    </html>
    """


@router.post("/add", response_class=HTMLResponse)
def add_expense(
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):

    expense = Expense(
        user_id=1,
        category=category,
        amount=amount,
        description=description,
    )

    db.add(expense)
    db.commit()

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="refresh" content="0; url=/dashboard/expenses/">
    </head>
    <body>
        <p>Expense added successfully...</p>
    </body>
    </html>
    """