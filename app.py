from flask import Flask, request, jsonify, render_template
from client import create_record, delete_record, update_record, read_record

app = Flask(__name__, template_folder="templates")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create", methods=["POST"])
def handle_create_record():
    data = request.json
    name = data.get("name")
    age = int(data.get("age"))
    roll = data.get("roll")
    city = data.get("city")
    print(name, name, name)
    try:
        record_id = create_record(name, age, city, roll)

        return jsonify({"record_id": record_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/updateRecord", methods=["POST"])
def update_the_record():
    data = request.json
    name = data.get("name")
    age = int(data.get("age"))
    record_id = data.get("roll")
    city = data.get("city")
    print(name, name, name)
    try:
        record_id = update_record(record_id, name, age, city)

        return jsonify({"record_id": record_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/read")
def read():
    return render_template("Read.html")


@app.route("/deleteRecord", methods=["POST"])
def delete_the_record():

    data = request.json
    roll = data.get("roll")

    try:
        delete_response = delete_record(roll)

        return jsonify({"deleted_id": delete_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/readRecord", methods=["POST"])
def read_the_record():

    data = request.json
    roll = data.get("roll")

    try:
        read_response, x = read_record(roll)
        # print(read_response)
        return jsonify(
            {
                "name": read_response.name,
                "age": read_response.age,
                "city": read_response.city,
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # app.run(port=5500)
    app.run(debug=True)
