from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import sys
from typing import Dict
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add the project root to Python path
sys.path.append(project_root)

app = FastAPI()

# Mount static files using absolute path
static_path = os.path.join(project_root, 'static')
templates_path = os.path.join(project_root, 'templates')

app.mount("/static", StaticFiles(directory=static_path), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory=templates_path)

@app.get("/", response_class=HTMLResponse)
async def read_assessment(request: Request):
    # Import the assessment generation function
    from src.generate_assessment_widget import generate_assessment_widget
    
    # Generate the assessment widget
    assessment_widget = generate_assessment_widget()
    
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "assessment_widget": assessment_widget
    })

async def send_email(email: str, total_score: float) -> bool:
    """Send assessment results via email"""
    try:
        # Check if SMTP settings are configured
        smtp_host = os.getenv("SMTP_HOST")
        smtp_port = os.getenv("SMTP_PORT")
        smtp_user = os.getenv("SMTP_USER")
        smtp_pass = os.getenv("SMTP_PASS")
        
        if not all([smtp_host, smtp_port, smtp_user, smtp_pass]):
            print("Email configuration not found. Please set SMTP environment variables.")
            return False

        message = MIMEMultipart()
        message["From"] = smtp_user
        message["To"] = email
        message["Subject"] = "Your Inclusive Space Index Assessment Results"

        # Create email content
        body = f"""
        Thank you for completing the Inclusive Space Index Assessment!

        Your Results:
        Total Score: {total_score}

        Thank you for helping us improve inclusivity in spaces!
        """

        message.attach(MIMEText(body, "plain"))

        # Send email
        await aiosmtplib.send(
            message,
            hostname=smtp_host,
            port=int(smtp_port),
            username=smtp_user,
            password=smtp_pass,
            use_tls=True
        )
        return True
    except aiosmtplib.SMTPException as e:
        print(f"SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.post("/submit")
async def submit_assessment(request: Request):
    # Get form data
    form_data = await request.form()
    
    # Process the answers
    answers = {}
    total_score = 0
    
    for key, value in form_data.items():
        if key.startswith('q'):
            answers[key] = float(value)
            total_score += float(value)
    
    return templates.TemplateResponse("result.html", {
        "request": request,
        "answers": answers,
        "total_score": total_score
    })

@app.post("/send-email")
async def send_email_results(
    request: Request,
    email: str = Form(...),
    consent: bool = Form(...),
    total_score: float = Form(...)
):
    if not consent:
        raise HTTPException(status_code=400, detail="Consent is required")
    
    # Send email
    success = await send_email(email, total_score)
    
    if success:
        return {"message": "Results sent successfully to your email!"}
    else:
        if not all([os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"), 
                   os.getenv("SMTP_USER"), os.getenv("SMTP_PASS")]):
            return {"message": "Email service not configured. Please try again later."}
        raise HTTPException(status_code=500, detail="Failed to send email")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
