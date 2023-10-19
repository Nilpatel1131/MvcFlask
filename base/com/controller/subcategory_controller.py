from base import app
from base.com.dao.category_dao import CategoryDAO
from base.com.vo.subcategory_vo import SubCategoryVO
from base.com.dao.subcategory_dao import SubCategoryDAO
from flask import render_template, request, redirect
from base.com.controller.login_controller import login_required


@app.route('/admin/load_subcategory')
@login_required('admin')
def admin_load_subcategory():
    try:
        category_dao = CategoryDAO()
        category_vo_list = category_dao.view_category()
        return render_template('admin/addSubcategory.html', category_vo_list=category_vo_list)
    except Exception as excep:
        print("admin_load_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/insert_subcategory', methods=['post'])
@login_required('admin')
def admin_insert_subcategory():
    try:
        subcategory_name = request.form.get('subcategoryName')
        subcategory_description = request.form.get('subcategoryDescription')
        subcategory_category_id = request.form.get('subcategoryCategoryId')
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_name = subcategory_name
        subcategory_vo.subcategory_description = subcategory_description
        subcategory_vo.subcategory_category_id = subcategory_category_id
        subcategory_dao = SubCategoryDAO()
        subcategory_dao.insert_subcategory(subcategory_vo)
        return redirect('/admin/home.html')
    except Exception as excep:
        print("admin_insert_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/view_subcategory')
@login_required('admin')
def admin_view_subcategory():
    try:
        subcategory_dao = SubCategoryDAO()
        subcategory_vo_list = subcategory_dao.view_subcategory()
        print("subcategory_vo_list_edit>>>>>>>>>>>", subcategory_vo_list)
        return render_template('admin/viewSubcategory.html', subcategory_vo_list=subcategory_vo_list)
    except Exception as excep:
        print("admin_view_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/delete_subcategory')
@login_required('admin')
def admin_delete_subcategory():
    try:
        subcategory_id = request.args.get('subcategoryId')
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_id = subcategory_id
        subcategory_dao = SubCategoryDAO()
        subcategory_dao.delete_subcategory(subcategory_vo)
        return redirect('/admin/view_subcategory')
    except Exception as excep:
        print("admin_delete_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/edit_subcategory')
@login_required('admin')
def admin_edit_subcategory():
    try:
        subcategory_id = request.args.get('subcategoryId')
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_id = subcategory_id
        subcategory_dao = SubCategoryDAO()
        subcategory_vo_list = subcategory_dao.edit_subcategory(subcategory_vo)
        print("<<subcategory_vo_list_edit>>", subcategory_vo_list)
        category_dao = CategoryDAO()
        category_vo_list = category_dao.view_category()
        return render_template('admin/editSubcategory.html', category_vo_list=category_vo_list,
                               subcategory_vo_list=subcategory_vo_list)
    except Exception as excep:
        print("admin_edit_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)


@app.route('/admin/update_subcategory', methods=['post'])
@login_required('admin')
def admin_update_subcategory():
    try:
        subcategory_category_id = request.form.get('subcategoryCategoryId')
        subcategory_id = request.form.get('subcategoryId')
        subcategory_name = request.form.get('subcategoryName')
        subcategory_description = request.form.get('subcategoryDescription')
        subcategory_vo = SubCategoryVO()
        subcategory_vo.subcategory_id = subcategory_id
        subcategory_vo.subcategory_category_id = subcategory_category_id
        subcategory_vo.subcategory_name = subcategory_name
        subcategory_vo.subcategory_description = subcategory_description
        subcategory_dao = SubCategoryDAO()
        subcategory_dao.update_subcategory(subcategory_vo)
        return redirect('/admin/view_subcategory')
    except Exception as excep:
        print("admin_update_subcategory route exception occured>>>>>>>>", excep)
        return render_template('admin/viewError.html', excep=excep)
