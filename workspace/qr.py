from flask import Blueprint, Flask, render_template, request, redirect, url_for, send_file
from workspace.db import get_db
import qrcode
from io import BytesIO
import base64
import json
import os

bp = Blueprint('qr', __name__)

@bp.route('/alert')
def index():
    return render_template('main/alert.html', qr_code=None)

@bp.route('/add', methods=['POST'])
def add_user():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO QR_INFO (name, contact,Id, address, age, kName, kContact, kId, kAddress, chronic, chronic1, allergy, allergy1, mental, mental1, medications, medications1)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        request.form.get('name'),
        request.form.get('contact'),
        request.form.get('Id'),
        request.form.get('address'),
        request.form.get('age'),
        request.form.get('Kname'),
        request.form.get('Kcontact'),
        request.form.get('Kid'),
        request.form.get('Kaddress'),
        request.form.get('chronic'),
        request.form.get('chronic_1'),
        request.form.get('allergy'),
        request.form.get('allergy_1'),
        request.form.get('mental'),
        request.form.get('mental_1'),
        request.form.get('medications'),
        request.form.get('medications_1')
    ))
    conn.commit()
    conn.close()
    return redirect(url_for('qr.index'))


@bp.route('/generate', methods=['POST'])
def generate_qr_code():
    # Collect form data
    form_data = {
        "Name": request.form.get('name'),
        "Contact": request.form.get('contact'),
        "Id": request.form.get('id'),
        "Address": request.form.get('address'),
        "Age": request.form.get('age'),
        "Kins Name": request.form.get('Name'),
        "Kins Contact": request.form.get('Contact'),
        "Kins Id": request.form.get('Id'),
        "Kins Address": request.form.get('Address'),
        "Chronic Condition": request.form.get('chronic'),
        "Additional chronic Condition": request.form.get('chronic_1'),
        "Allergy": request.form.get('allergy'),
        "Additional Allergy Condition": request.form.get('allergy_1'),
        "Mental Condition": request.form.get('mental'),
        "Additional Mental Condition": request.form.get('mental_1'),
        "Medication": request.form.get('medications'),
        "Additional Medications": request.form.get('medications_1')
    }

    # Create a formatted string
    qr_data = "\n".join(f"{key}: {value}" for key, value in form_data.items() if value)

    # Generate QR code
    qr = qrcode.make(qr_data)
    img = BytesIO()
    qr.save(img, 'PNG')
    img.seek(0)
    
    # Generate base64-encoded image for displaying in HTML
    qr_code_img = "data:image/png;base64," + base64.b64encode(img.getvalue()).decode('utf-8')
    

    
    
    return render_template('main/alert.html', qr_code=qr_code_img)

@bp.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)
