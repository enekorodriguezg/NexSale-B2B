from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fpdf import FPDF

from server.models import Order

### --------------------------------------------------###

def create_report(order_id: int, format: str, db: Session):
    media_type: str = f"application/{format}"
    file_extension: str = format
    try: 
        stmt = select(Order).where(Order.id == order_id)
        order: Order = db.execute(stmt).scalar_one_or_none()
        
        if not order:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Order with ID {order_id} not found"
            )
        
        if format == "pdf":
            file_bytes = create_pdf_report(order = order)
        elif format == "rtf":
            file_bytes = create_rtf_report(order = order)
        else:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Invalid report format"
            )

        return file_bytes, media_type, file_extension

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "An unexpected error occured during report generation"
        ) from e

def create_pdf_report(order: Order) -> bytearray:
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, f"Order Invoice #Order ID: {order.id}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5) 
    
    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 8, f"Customer ID: {order.user_id}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)

    pdf.set_font("helvetica", "B", 12)
    pdf.cell(40, 10, "Product ID", border=1)
    pdf.cell(40, 10, "Quantity", border=1)
    pdf.cell(40, 10, "Unit Price", border=1)
    pdf.cell(0, 10, "Subtotal", border=1, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 12)
    total_amount = 0.0
    
    for item in order.items: 
        subtotal = item.quantity * item.unit_price
        total_amount += subtotal
        
        pdf.cell(40, 10, str(item.product_id), border=1)
        pdf.cell(40, 10, str(item.quantity), border=1)
        pdf.cell(40, 10, f"{item.unit_price:.2f}", border=1)
        pdf.cell(0, 10, f"{subtotal:.2f}", border=1, new_x="LMARGIN", new_y="NEXT")
        
    pdf.ln(5)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(120, 10, "Order Total:", align="R")
    pdf.cell(0, 10, f"{total_amount:.2f}", new_x="LMARGIN", new_y="NEXT")

    return pdf.output()

def create_rtf_report(order: Order):
    rtf_lines = [
            r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033{\fonttbl{\f0\fnil\fcharset0 Helvetica;}}",
            r"\f0\fs24\pard",
            rf"{{\b Order Invoice #{order.id}\par}}",
            rf"Customer ID: {order.user_id}\par",
            r"\par",
            r"{\b Product ID \tab Quantity \tab Unit Price \tab Subtotal\par}",
        ]
        
    total_amount = 0.0
        
    for item in order.items:
        subtotal = item.quantity * item.unit_price
        total_amount += subtotal
        line = rf"{item.product_id} \tab {item.quantity} \tab {item.unit_price:.2f} \tab {subtotal:.2f}\par"
        rtf_lines.append(line)
        
    rtf_lines.append(r"\par")
    rtf_lines.append(rf"{{\b Order Total: {total_amount:.2f}\par}}")
    rtf_lines.append(r"}")
    rtf_content = "\n".join(rtf_lines)

    return rtf_content.encode("utf-8")


