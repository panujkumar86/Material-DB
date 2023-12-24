from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from flask import render_template
import pandas as pd

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'materials_database',
    'host': 'mongodb://localhost/materials_database'
}

db = MongoEngine(app)


class Material(db.Document):
    nsites = db.IntField()
    formula_pretty = db.StringField()
    volume = db.FloatField()
    density = db.FloatField()
    symmetry__crystal_system = db.StringField()
    symmetry__symbol = db.StringField()
    symmetry__number = db.IntField()
    symmetry__point_group = db.StringField()
    symmetry__symprec = db.FloatField()
    symmetry__version = db.StringField()
    formation_energy_per_atom = db.FloatField()
    energy_above_hull = db.FloatField()
    is_stable = db.BooleanField()
    band_gap = db.FloatField()
    is_gap_direct = db.BooleanField()
    is_metal = db.BooleanField()
    ordering = db.StringField()
    total_magnetization = db.FloatField()
    universal_anisotropy = db.FloatField()
    theoretical = db.BooleanField()


def load_data_from_csv():
    try:
        data = pd.read_csv('data.csv')
        records = data.to_dict(orient='records')

        # Make sure all records are instances of Material
        material_records = [Material(**record) for record in records]

        # Insert the correct instances into the database
        Material.objects.insert(material_records)

        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")

    #Material.objects.insert(records)
    ##data = pd.read_csv('/Users/anujkumarpandey/Downloads/data.csv')

     #data = pd.read_csv('data.csv')


@app.route('/store-data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        material = Material(**data)
        material.save()
        return jsonify({'message': 'Data stored successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['GET'])
def search():
    try:
        query = request.args.get('query')
        results = Material.objects.filter(formula_pretty__icontains=query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Mathematical filters on numerical fields
#@app.route('/filter', methods=['GET'])
#def filter_data():
  #  try:
  #      field = request.args.get('field')
   #     operator = request.args.get('operator')
  #      value = float(request.args.get('value'))
  #      query = {f'{field}__{operator}': value}
 #       results = Material.objects.filter(**query)
  #      return jsonify(results), 200
 #   except Exception as e:
 #       return jsonify({'error': str(e)}), 500
# Mathematical filters on numerical fields
# Mathematical filters on numerical fields
# Mathematical filters on numerical fields
# Mathematical filters on numerical fields
# Mathematical filters on numerical fields
@app.route('/filter', methods=['GET'])
def filter_data():
    try:
        field = request.args.get('field')
        operator = request.args.get('operator')
        value = float(request.args.get('value'))

        if operator == '>':
            results = Material.objects.filter(**{f'{field}__gt': value})
        elif operator == '<':
            results = Material.objects.filter(**{f'{field}__lt': value})
        elif operator == '=':
            results = Material.objects.filter(**{f'{field}__exact': value})
        else:
            return jsonify({'error': f"Unsupported operator: {operator}"}), 400

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Boolean field filter
@app.route('/boolean-filter', methods=['GET'])
def boolean_filter():
    try:
        field = request.args.get('field')
        value = request.args.get('value').lower() == 'true'
        query = {field: value}
        results = Material.objects.filter(**query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Element-based filtering
# Element-based filtering
@app.route('/element-filter', methods=['GET'])
def element_filter():
    try:
        elements = request.args.get('elements').split('-')
        query = {'formula_pretty__in': elements}
        results = Material.objects.filter(**query)
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Multi-column sort
# Multi-column sort
# Multi-column sort
# Multi-column sort
@app.route('/sort', methods=['GET'])
def sort_data():
    try:
        sort_columns = request.args.get('columns').split(',')
        order = request.args.get('order', 'asc')

        if order == 'asc':
            results = Material.objects.order_by(*sort_columns)
        elif order == 'desc':
            results = Material.objects.order_by(*["-" + col for col in sort_columns])
        else:
            return jsonify({'error': f"Unsupported order: {order}"}), 400

        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/')
def home():
    return render_template('index.html')
    #return 'Welcome to the Materials Database API!'





if __name__ == '__main__':
    load_data_from_csv()
app.run(host='0.0.0.0', port=8080, debug=True)
