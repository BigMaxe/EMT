from flask import Blueprint, request
from app.services.report_service import ReportService

report_bp = Blueprint('report_bp', __name__)

report_service = ReportService()

@report_bp.route('/campaign_report/<int:campaign_id>', methods=['GET'])
def campaign_report(campaign_id):
    return report_service.generate_campaign_report(campaign_id)

@report_bp.route('/summary_report', methods=['GET'])
def summary_report():
    return report_service.generate_summary_report()

@report_bp.route('/export_report', methods=['POST'])
def export_report():
    report = request.json.get('report')
    file_format = request.json.get('file_format', 'json')
    return report_service.export_report(report, file_format)
