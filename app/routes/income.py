from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Income


router = APIRouter(
    prefix="/dashboard/income",
    tags=["Income"],
)


@router.get("/", response_class=HTMLResponse)
def income_page(db: Session = Depends(get_db)):

    incomes = (
        db.query(Income)
        .filter(Income.user_id == 1)
        .order_by(Income.id.desc())
        .all()
    )

    income_rows = ""

    for income in incomes:
        income_rows += f"""
        <tr>
            <td>{income.category}</td>
            <td>₹{income.amount:.2f}</td>
            <td>{income.description or "-"}</td>
        </tr>
        """

    if not income_rows:
        income_rows = """
        <tr>
            <td colspan="3">No income added yet.</td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>PocketSmart AI - Income</title>

        <style>

            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: #f4f7fb;
            }}

            .header {{
                background: #16a34a;
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

            input,
            select {{
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
                background: #16a34a;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }}

            button:hover {{
                background: #15803d;
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
                background: #f0fdf4;
            }}

            .back {{
                display: inline-block;
                margin-top: 10px;
                color: #2563eb;
                text-decoration: none;
            }}

        </style>

    </head>

    <body>

        <div class="header">
            <h1>💰 PocketSmart AI</h1>
            <p>Income Management</p>
        </div>

        <div class="container">

            <div class="card">

                <h2>➕ Add New Income</h2>

                <form action="/dashboard/income/add" method="post">

                    <label>Income Category</label>

                    <select name="category" required>

                        <option value="">Select Category</option>
                        <option value="Salary">Salary</option>
                        <option value="Freelance">Freelance</option>
                        <option value="Business">Business</option>
                        <option value="Investment">Investment</option>
                        <option value="Other">Other</option>

                    </select>

                    <label>Amount</label>

                    <input
                        type="number"
                        name="amount"
                        step="0.01"
                        min="0"
                        placeholder="Enter income amount"
                        required
                    >

                    <label>Description</label>

                    <input
                        type="text"
                        name="description"
                        placeholder="Example: September Salary"
                    >

                    <button type="submit">
                        Add Income
                    </button>

                </form>

            </div>

            <div class="card">

                <h2>📋 Income History</h2>

                <table>

                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Amount</th>
                            <th>Description</th>
                        </tr>
                    </thead>

                    <tbody>
                        {income_rows}
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
def add_income(
    category: str = Form(...),
    amount: float = Form(...),
    description: str = Form(""),
    db: Session = Depends(get_db),
):

    income = Income(
        user_id=1,
        category=category,
        amount=amount,
        description=description,
    )

    db.add(income)
    db.commit()

    return """
    <!DOCTYPE html>
    <html>

    <head>
        <title>Income Added</title>

        <meta
            http-equiv="refresh"
            content="1; url=/dashboard/income/"
        >

        <style>
            body {
                font-family: Arial;
                background: #f4f7fb;
                text-align: center;
                padding-top: 100px;
            }

            .box {
                display: inline-block;
                background: white;
                padding: 40px;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.10);
            }

            .success {
                color: #16a34a;
            }
        </style>

    </head>

    <body>

        <div class="box">

            <h1 class="success">
                ✅ Income Added Successfully!
            </h1>

            <p>
                Income has been saved to the database.
            </p>

            <p>
                Returning to Income Management...
            </p>

        </div>

    </body>

    </html>
    """