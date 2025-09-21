from datetime import datetime
from flask import Flask, Response, render_template, send_file, session, jsonify, redirect, url_for,request, redirect
from werkzeug.exceptions import abort
from routes.usecases.ForExportingRoutes import ForExportingRoutes
import io

class ExportWebController():

    def __init__(self, webapp: Flask, export_service: ForExportingRoutes):
        self.webapp = webapp
        self.export_service = export_service
        self.webapp.add_url_rule('/app/export_page', view_func=self.export_parameters, methods=['GET'])
        self.webapp.add_url_rule('/app/export', view_func=self.export, methods=['GET'])

    def export_parameters(self):
        return render_template('export.html', tenant_id=session.get("tenant_id"))

    def export(self):        
        year = int(request.args.get('year'))
        print(f"Export for year: {year}")
        content = self.export_service.export(year)
        print(f"Exported {len(content)} bytes")
        
        return send_file(
            io.BytesIO(content),
            download_name='export_berichtsjahr_'+str(year)+ '_'+datetime.today().strftime('%Y-%m-%d')+'.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True
        )
