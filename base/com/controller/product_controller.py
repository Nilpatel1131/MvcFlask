import os
from base import app
from base.com.dao.category_dao import CategoryDAO
from base.com.dao.subcategory_dao import SubCategoryDAO
from base.com.vo.subcategory_vo import SubCategoryVO
from flask import render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from base.com.vo.product_vo import ProductVO
from base.com.dao.product_dao import ProductDAO
from base.com.controller.login_controller import login_required

product_folder = 'base/static/adminResources/product/'
app.config['product_folder'] = product_folder


@app.route('/admin/load_product')
@login_required('admin')
def load_product():
    try:
        category_dao = CategoryDAO()
        category_vo_list = category_dao.view_category()
        return render_template('admin/addProduct.html', category_vo_list=category_vo_list)

    except Exception as excep:
        print("admin_load_product route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/ajax_subcategory_product')
@login_required('admin')
def admin_ajax_subcategory_product():
    try:
        subcategory_category_id = request.args.get('productCategoryId')
        print("++++++++", subcategory_category_id)
        subcategory_dao = SubCategoryDAO()
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_category_id = subcategory_category_id
        subcategory_vo_list = subcategory_dao.view_ajax_sucategory_product(subcategory_vo)
        print("ajax_subcategory_vo_list>>>>", subcategory_vo_list)
        ajax_product_subcategory = [i.as_dict() for i in subcategory_vo_list]
        print("<<ajax_product_subcategory>>", ajax_product_subcategory)
        return jsonify(ajax_product_subcategory)
    except Exception as excep:
        print("admin_ajax_product route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/insert_product', methods=['post'])
@login_required('admin')
def admin_insert_product():
    try:
        product_category_id = request.form.get('productCategoryId')
        product_subcategory_id = request.form.get('productSubcategoryId')
        product_name = request.form.get('productName')
        product_description = request.form.get('productDescription')
        product_price = float(request.form.get('productPrice'))
        product_quantity = int(request.form.get('productQuantity'))
        product_total_price = product_price*product_quantity
        product_image = request.files.get('productImage')
        product_image_name = secure_filename(product_image.filename)
        product_image_path = os.path.join(app.config['product_folder'])
        product_image.save(os.path.join(product_image_path, product_image_name))
        product_vo = ProductVO()
        product_vo.product_category_id = product_category_id
        product_vo.product_subcategory_id = product_subcategory_id
        product_vo.product_name = product_name
        product_vo.product_description = product_description
        product_vo.product_quantity = product_quantity
        product_vo.product_price = product_price
        product_vo.product_total_price = product_total_price
        product_vo.product_image_name = product_image_name
        product_vo.product_image_path = product_image_path.replace("base",
                                                                   "..")
        product_dao = ProductDAO()
        product_dao.insert_product(product_vo)
        return render_template('admin/home.html')
    except Exception as excep:
        print("admin_insert_product route exception occurred >>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/view_product')
@login_required('admin')
def admin_view_product():
    try:
        product_dao = ProductDAO()
        product_vo_list = product_dao.view_product()
        print("<<product_vo_list>>>>>>>>>>>", product_vo_list)
        return render_template('admin/viewProduct.html', product_vo_list=product_vo_list)
    except Exception as excep:
        print("admin_view_product route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/delete_product')
@login_required('admin')
def admin_delete_product():
    try:
        product_id = request.args.get('productId')
        product_vo = ProductVO()
        product_vo.product_id = product_id
        product_dao = ProductDAO()
        product_vo_list = product_dao.delete_product(product_id)
        file_path = product_vo_list.product_image_path.replace("..", "base") + product_vo_list.product_image_name
        os.remove(file_path)
        return redirect(url_for('admin_view_product'))
    except Exception as excep:
        print("admin_delete_product route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/edit_product')
@login_required('admin')
def admin_edit_product():
    product_id = request.args.get('productId')
    product_vo = ProductVO()
    product_vo.product_id = product_id
    product_dao = ProductDAO()
    product_vo_list = product_dao.edit_product(product_vo)
    category_dao = CategoryDAO()
    category_list = category_dao.view_category()
    print(">>>>>>>>>>>product_vo_list_edit", product_vo_list[0].__dict__)
    print(">>>>>>>>>>>category_vo_list_edit", category_list, category_list[0].category_id)
    return render_template('admin/editProduct.html', product_vo_list=product_vo_list, category_list=category_list)


@app.route('/admin/update_product',methods=['post'])
@login_required('admin')
def admin_update_product():
    product_id = request.form.get('productId')
    product_category_id = request.form.get('productCategoryId')
    # print('<<product_category_id>>',product_category_id)
    product_subcategory_id = request.form.get('productSubcategoryId')
    product_name = request.form.get('productName')
    product_description = request.form.get('productDescription')
    product_price = request.form.get('productPrice')
    product_quantity = request.form.get('productQuantity')
    product_image = request.files.get('productImage')
    print(f"product_image::::{product_image}")
    product_image_name = secure_filename(product_image.filename)
    product_image_path = os.path.join(app.config['product_folder'])
    product_image.save(os.path.join(product_image_path, product_image_name))
    product_vo = ProductVO()
    product_vo.product_id = product_id
    product_vo.product_category_id = product_category_id
    product_vo.product_subcategory_id = product_subcategory_id
    product_vo.product_name = product_name
    product_vo.product_description = product_description
    product_vo.product_quantity = product_quantity
    product_vo.product_price = product_price
    product_vo.product_image_name = product_image_name
    product_vo.product_image_path = product_image_path.replace("base",
                                                               "..")
    product_dao = ProductDAO()
    product_dao.update_product(product_vo)
    return render_template('admin/home.html')
