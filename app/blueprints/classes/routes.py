from flask import Blueprint, request, render_template, jsonify
from app.models import Class
from app import db
from flask_login import login_required,  current_user




classes_bp = Blueprint('classes', __name__)



#API CLASSES --------------------------------------------------
@classes_bp.route('/api/classes', methods=['POST', 'GET'])
@login_required
def add_class():
    if request.method == 'POST':
        try:
            data = request.json

            name = data.get("name")
            icon = data.get("icon")

            new_class = Class(name=name, icon=icon, user_id = current_user.id)
            db.session.add(new_class)
            db.session.commit()
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
    elif request.method == 'GET':
        user_classes = Class.query.filter_by(user_id = current_user.id).all()
        return jsonify([class_obj.to_dict() for class_obj in user_classes])
    



#USUWANIE KLAS---------------------------------------------------------
@classes_bp.route('/api/classes/<int:class_id>', methods=['DELETE'])
@login_required
def delete_class(class_id):
    cls = Class.query.filter_by(id=class_id, user_id=current_user.id).first()
    if not cls:
        return jsonify({"error": "Class not found"}), 404

    db.session.delete(cls)
    db.session.commit()
    return jsonify({"message":  f"Class {class_id} deleted"}), 200




#ROBIENIE DYNAMICZNIE STRON DLA KLAS-----------------------------------------
@classes_bp.route('/class/<int:class_id>')
@login_required
def class_detail(class_id):
    return render_template("class.html", class_id=class_id, user=current_user)





#POBIERANIE NAZWY KLASY DO WYSWIETLENIA JEJ-------------------------------------
@classes_bp.route('/api/classes/<int:class_id>', methods=['GET'])
@login_required
def get_class_name_by_id(class_id):
    cls = Class.query.filter_by(id=class_id, user_id=current_user.id).first()
    if not cls:
        return jsonify({"error": "Class not found"}), 404
    
    return jsonify(cls.to_dict()), 200

#UPDATOWANIE KLASY----------------------------------------------


@classes_bp.route('/api/updateClass/<int:classId>', methods=["PATCH"])
@login_required
def update_class_data(classId):

    try:
        class_id = classId

        data = request.json
        if not data:
            return jsonify({"message":"No data provided"}), 400
        
        icon = data.get('icon')
        class_name = data.get('name')
        print(icon, class_name)

        if not icon and not class_name:
            return jsonify({"message": "No changes provided"})
        
        class_ = Class.query.filter_by(id=class_id).first()
        if not class_:
            return jsonify({"error": "Class not found"}), 404
        
        if class_name:
            class_.name = class_name
        if icon:
            class_.icon = icon

        db.session.commit()

        return jsonify({"message": "Class updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f'Error updating class data {str(e)}'}), 404