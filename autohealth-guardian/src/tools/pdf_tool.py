"""Simple weekly PDF generator using reportlab."""
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from pathlib import Path


class PDFTool:
    def __init__(self, out_dir: Path = None):
        self.out_dir = out_dir or Path("./data/reports")
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def generate_weekly_report(self, user_id: str, agg: dict):
        out_path = self.out_dir / f"{user_id}_weekly_report.pdf"
        c = canvas.Canvas(str(out_path), pagesize=letter)
        c.setFont("Helvetica", 14)
        c.drawString(72, 720, f"Weekly Health Report - {user_id}")
        y = 680
        if agg:
            for k, v in agg.items():
                c.setFont("Helvetica", 12)
                c.drawString(72, y, f"{k}: {v:.2f}")
                y -= 24
        else:
            c.drawString(72, y, "No data available for this period.")
        c.showPage()
        c.save()
        return str(out_path)
