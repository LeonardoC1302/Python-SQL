from flask import Flask, request, jsonify
from queryORM import getWastesQuantity

app = Flask(__name__)
@app.route('/wastes', methods=['POST'])
def get_wastes():
    quantity = request.json['quantity']
    result = getWastesQuantity(quantity)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
