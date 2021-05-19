from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:qwe1234*@localhost/apiflask'
app.config['SQALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app) 
ma = Marshmallow(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(70), unique=True)
    price = db.Column(db.String(70))

    def __init__(self, name, price):
        self.name = name
        self.price = price

db.create_all()

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'price')

productSchema = ProductSchema()
productSchemas = ProductSchema(many=True)


@app.route('/product',methods=["POST"])
def create_produt():
    name = request.json['name']
    price = request.json['price']

    new_product = Product(name, price)
    db.session.add(new_product)
    db.session.commit()

    return productSchema.jsonify(new_product)

@app.route('/product', methods=["GET"])
def get_products():
    try:
        all_products = Product.query.all()
        result = productSchema.dump(all_products)
    except Exception as err:
        print(err)
        return {'error':True,'message':'missing keys'}
    return productSchemas.jsonify(all_products)

@app.route('/product/<id>', methods=['GET'])
def get_product(id):    
    try:
        product = Product.query.get(id)
    except Exception as err:
        print(err)
        return {'error':True,'message':'missing keys'}
    return productSchema.jsonify(product)

@app.route('/product/<id>', methods=['PUT'])
def put_product(id):
    try:
        updateRow = Product.query.get(id)
        name = request.json['name']
        price = request.json['price']
    except Exception as err:
        print(err)
        return {'error':True,'message':'missing keys'}
                        
    updateRow.name = name
    updateRow.price = price
    db.session.commit()
    return jsonify({'error':False,'message':'successful upgrade'})

@app.route('/product/<id>', methods=['DELETE'])
def delete_task(id):
    try:
        product = Product.query.get(id)
    except Exception as err:
        print(err)
        return {'error':True,'message':'missing keys'}
    
    db.session.delete(product)
    db.session.commit()
    return productSchema.jsonify(product)


if __name__ == '__main__':
    app.run(debug=True)