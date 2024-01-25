from flask import jsonify, Blueprint, request, abort
from apidev.models import Plant

bp = Blueprint('main', __name__)

@bp.route('/')
def plants():
    plants = Plant.query.all()
    return jsonify({
        'success': True,
        'plants': plants.format()
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

    if plans is None:
        abort(404)
    else:
        formatted_output = [plant.format() for plant in plants]
        return jsonify({
            'success': True,
            'plant':formatted_output
        })

