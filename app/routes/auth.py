import hashlib
import hmac
import secrets

from fastapi import APIRouter, Depends, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        310000,
    )

    return salt.hex() + ":" + password_hash.hex()


def verify_password(password: str, stored_password: str) -> bool:
    try:
        salt_hex, hash_hex = stored_password.split(":")

        salt = bytes.fromhex(salt_hex)
        stored_hash = bytes.fromhex(hash_hex)

        calculated_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            310000,
        )

        return hmac.compare_digest(
            calculated_hash,
            stored_hash,
        )

    except Exception:
        return False


@router.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PocketSmart AI - Login</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                text-align: center;
                padding-top: 80px;
            }

            .box {
                display: inline-block;
                width: 380px;
                background: white;
                padding: 35px;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.10);
            }

            input {
                width: 90%;
                padding: 12px;
                margin: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
            }

            button {
                width: 95%;
                padding: 12px;
                margin-top: 15px;
                background: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }

            a {
                display: block;
                margin-top: 15px;
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>💰 PocketSmart AI</h1>
            <p>Login to your account</p>

            <form action="/auth/login" method="post">

                <input
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Enter your password"
                    required
                >

                <button type="submit">
                    Login
                </button>

            </form>

            <a href="/auth/register">
                Create New Account
            </a>

            <a href="/">
                ← Back to Home
            </a>
        </div>
    </body>
    </html>
    """


@router.get("/register", response_class=HTMLResponse)
def register_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PocketSmart AI - Register</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f7fb;
                text-align: center;
                padding-top: 80px;
            }

            .box {
                display: inline-block;
                width: 380px;
                background: white;
                padding: 35px;
                border-radius: 16px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.10);
            }

            input {
                width: 90%;
                padding: 12px;
                margin: 10px;
                border: 1px solid #ddd;
                border-radius: 8px;
            }

            button {
                width: 95%;
                padding: 12px;
                margin-top: 15px;
                background: #16a34a;
                color: white;
                border: none;
                border-radius: 8px;
                cursor: pointer;
            }

            a {
                display: block;
                margin-top: 15px;
                color: #2563eb;
                text-decoration: none;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>💰 PocketSmart AI</h1>
            <p>Create your account</p>

            <form action="/auth/register" method="post">

                <input
                    type="text"
                    name="name"
                    placeholder="Enter your name"
                    required
                >

                <input
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    required
                >

                <input
                    type="password"
                    name="password"
                    placeholder="Create a password"
                    required
                >

                <button type="submit">
                    Register
                </button>

            </form>

            <a href="/auth/">
                Already have an account? Login
            </a>
        </div>
    </body>
    </html>
    """


@router.post("/register", response_class=HTMLResponse)
def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user:
        return """
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial; text-align: center; padding: 80px;">
            <h2>⚠️ Email already registered</h2>
            <p>Please use another email address.</p>
            <a href="/auth/register">Try Again</a>
        </body>
        </html>
        """

    password_hash = hash_password(password)

    user = User(
        name=name,
        email=email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Registration Successful</title>
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

            a {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>🎉 Registration Successful!</h1>
            <p>Your PocketSmart AI account has been created.</p>
            <a href="/auth/">Go to Login</a>
        </div>
    </body>
    </html>
    """


@router.post("/login", response_class=HTMLResponse)
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not user:
        return """
        <h2>❌ Invalid email or password</h2>
        <a href="/auth/">Try Again</a>
        """

    if not verify_password(password, user.password_hash):
        return """
        <h2>❌ Invalid email or password</h2>
        <a href="/auth/">Try Again</a>
        """

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Welcome</title>
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

            a {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }
        </style>
    </head>

    <body>
        <div class="box">
            <h1>Login Successful! 🎉</h1>
            <p>Welcome to PocketSmart AI.</p>
            <a href="/">Go to PocketSmart AI</a>
        </div>
    </body>
    </html>
    """