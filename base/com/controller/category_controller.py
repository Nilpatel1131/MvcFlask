from base import app
from flask import render_template, request, redirect
from base.com.vo.category_vo import CategoryVO
from base.com.dao.category_dao import CategoryDAO
from base.com.controller.login_controller import login_required


@app.route('/admin/load_category')
@login_required('admin')
def admin_load_category():
    try:
        return render_template("admin/addCategory.html")
    except Exception as excep:
        print("admin_load_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/insert_category', methods=['post'])
@login_required('admin')
def admin_insert_category():
    try:
        category_name = request.form.get('categoryName')
        category_description = request.form.get('categoryDescription')

        category_vo = CategoryVO()
        category_vo.category_name = category_name
        category_vo.category_description = category_description

        category_dao = CategoryDAO()

        category_dao.insert_category(category_vo)
        return redirect('/admin/home.html')
    except Exception as excep:
        print("admin_insert_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/view_category')
@login_required('admin')
def admin_view_category():
    try:
        category_dao = CategoryDAO()
        category_vo_list = category_dao.view_category()
        print(">>>>>", category_vo_list)
        return render_template('admin/viewCategory.html', category_vo_list=category_vo_list)
    except Exception as excep:
        print("admin_view_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/delete_category', methods=['get'])
@login_required('admin')
def admin_delete_category():
    try:
        category_id = request.args.get('categoryId')
        category_vo = CategoryVO()
        cattegory_dao = CategoryDAO()
        category_vo.category_id = category_id
        cattegory_dao.delete_category(category_vo)
        return redirect('/admin/view_category')
    except Exception as excep:
        print("admin_delete_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/edit_category', methods=['get'])
@login_required('admin')
def admin_edit_category():
    try:
        category_id = request.args.get('categoryId')
        category_vo = CategoryVO()
        category_vo.category_id = category_id
        category_dao = CategoryDAO()
        category_vo_list = category_dao.edit_category(category_vo)
        print(">>>>>>>>>>>>>>>>>>>>>", category_vo_list)
        return render_template('admin/editCategory.html', category_vo_list=category_vo_list)
    except Exception as excep:
        print("admin_delete_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/update_category', methods=['post'])
@login_required('admin')
def admin_update_category():
    try:
        category_id = request.form.get('categoryId')
        category_name = request.form.get('categoryName')
        category_description = request.form.get('categoryDescription')
        category_vo = CategoryVO()
        category_dao = CategoryDAO()
        category_vo.category_id = category_id
        category_vo.category_name = category_name
        category_vo.category_description = category_description
        category_dao.update_category(category_vo)
        return redirect('/admin/view_category')
    except Exception as excep:
        print("admin_update_category route exception occurred>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)
