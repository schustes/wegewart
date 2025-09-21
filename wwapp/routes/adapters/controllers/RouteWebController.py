from datetime import datetime
from flask import Flask, render_template, session, jsonify, redirect, url_for,request, redirect
from werkzeug.exceptions import abort
import routes.adapters.controllers.RouteDictMapper as RouteMapper
from routes.domain.entities.RouteId import RouteId
from routes.usecases.ForReadingRoutes import ForReadingRoutes
from routes.usecases.ForSavingRoutes import ForSavingRoutes

class RouteWebController():

    def __init__(self, 
                 route_reader: ForReadingRoutes, 
                 route_writer: ForSavingRoutes, 
                 webapp: Flask):
        self.route_reader = route_reader
        self.route_writer = route_writer
        self.webapp = webapp

        self.webapp.add_url_rule('/app/all-routes', view_func=self.get_all_routes, methods=['GET'])
        self.webapp.add_url_rule('/app/my-routes', view_func=self.get_my_routes, methods=['GET'])
        self.webapp.add_url_rule('/app/my-routes/<route_id>', view_func=self.get_route_by_id, methods=['GET'])
        self.webapp.add_url_rule('/app/my-routes/<route_id>', view_func=self.delete_route, methods=['DELETE'])
        self.webapp.add_url_rule('/app/my-routes', view_func=self.add_route, methods=['POST'])
        self.webapp.add_url_rule('/app/my-routes/<route_id>', view_func=self.update_route, methods=['PUT'])
        self.webapp.add_url_rule('/app/add-route-form', view_func=self.add_route_form, methods=['GET'])

    def get_all_routes(self):
        routes = self.route_reader.get_all_routes()
        route_dtos = [RouteMapper.route_dto_to_dict(route) for route in routes]
        return render_template('all_routes.html', tenant_id=session.get("tenant_id"), routes=route_dtos)

    def get_my_routes(self):
        routes = self.route_reader.get_my_routes()
        route_dtos = [RouteMapper.route_dto_to_dict(route) for route in routes]
        return render_template('my_routes.html', routes=route_dtos)

    def get_route_by_id(self, route_id):
        print(f"get_route_by_id: {route_id}")
        route = self.route_reader.get_route_by_id(RouteId(route_id))
        if route is None:
            abort(404)
        return render_template('route.html', route=RouteMapper.route_dto_to_dict(route))

    def add_route_form(self):
        return render_template('add_route_form.html')

    def delete_route(self, route_id):
        self.route_writer.delete_route(route_id)
        return redirect(url_for('get_my_routes'))

    def add_route(self):
        if not request.json or 'activity' not in request.json or 'date' not in request.json:
            abort(400)

        try:
            date_obj = datetime.strptime(request.json['date'], '%Y-%m-%d').date()
        except ValueError:
            abort(400)
        route_command = RouteMapper.route_command_from_dict(request.json)
        route_command.user_id = session.get('user_id')
        route_command.tenant_id = session.get('tenant_id')
        self.route_writer.add_route(route_command)
        return redirect(url_for('get_my_routes'))
    
    def update_route(self, route_id):
        if not request.json:
            abort(400)
        route_command = RouteMapper.route_command_from_dict(request.json)
        route_command.route_id=route_id
        updated_route = self.route_writer.update_route(route_command)
        if updated_route is None:
            abort(404)
        return jsonify(RouteMapper.route_dto_to_dict(updated_route))

    
