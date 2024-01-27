from flask import jsonify, Blueprint, request, abort
from apidev.models import Plant
from apidev import db

bp = Blueprint('main', __name__)

@bp.route('/')
def plants():
    plants = Plant.query.all()
    formatted_output = [plant.format() for plant in plants]
    return jsonify({
        'success': True,
        'plants': formatted_output
    })

@bp.route('/plants')
def paginate_plants():
    page = request.args.get('page', 1, type=int)
    start = (page -1) * 12
    end = start + 3
    plants = Plant.query.all()
    formatted_output = [plant.format() for plant in plants]

    return jsonify({
        'success': True,
        'plants': formatted_output[start:end],
        'total_plants': len(formatted_output)
    })

@bp.route('/plants/<int:plant_id>')
def get_specific_plant(plant_id):
    plants = Plant.query.filter(Plant.id==plant_id).one_or_none()

    if plants is None:
        abort(404)
    else:
        return jsonify({
            'success': True,
            'plant':plants.format()
        })

@bp.route('/plants/<int:plants_id>', methods=['PATCH'])
def update_plant(plants_id):
    body = request.get_json()
    plant = Plant.query.filter(Plant.id==plants_id).one_or_none()
    if plant is None:
        abort(404)
    if 'name' and 'scientific_name' in body:
        plant.name = body.get('name')
        plant.scientific_name = body.get('scientific_name')
        

    plant.update()

    return jsonify({
        'success': True,
        'id':plant.id
    })

@bp.route('/plants/<int:plants_id>', methods=['DELETE'])
def delete_plan(plants_id):
    plant = Plant.query.filter(Plant.id==plants_id).one_or_none()
    if plant is None:
        abort(404)
    plant.delete()
   
    return jsonify({
        'success': True,
        'deleted': plant.id,
        'total_plants': len(Plant.query.all())
    })

@bp.route('/plants', methods=['POST'])
def create_plant():
    body = request.get_json()
    new_name = body.get('name', None)
    new_scientificname = body.get('scientific_name', None)
    new_state = body.get('is_poisonous', None)
    new_color = body.get('primary_color', None)

    plant = Plant(name=new_name,
                  scientific_name=new_scientificname,
                  is_poisonous=new_state,
                  primary_color=new_color)
    plant.insert()

    return jsonify({
        'success': True,
        'id':plant.id,
        'total_plants': len(Plant.query.all())
    })

@bp.errorhandler(404)
def not_found(error):
    return jsonify({
    'success': False,
    'error': 404,
    'message': 'resource not found'
    }), 404