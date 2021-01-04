from flask import Flask, request, jsonify, render_template, redirect
import pickle
import pandas as pd 

from preprocess import cleanHtml, cleanPunc, keepAlpha, lower
from flask import Flask,redirect, url_for, request, render_template, send_file

from flask_wtf import Form
from werkzeug.exceptions import abort
import os
import webbrowser
from threading import Timer


try:

    from flask import Flask, flash
    from werkzeug.exceptions import abort
    from flask_wtf import Form, FlaskForm
    from flask import redirect, url_for, request, render_template, send_file
    from io import BytesIO

    from flask_wtf.file import FileField
    from wtforms import SubmitField, TextField, TextAreaField,  SelectField, StringField
    from flask_wtf import Form
    import sqlite3
    from flask import Flask, request, redirect, render_template
    from werkzeug import secure_filename
    from wtforms.validators import DataRequired
    import sys
    print("All Modules Loaded .... ")
except:
    print (" Some Module are missing ...... ")


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
model = pickle.load(open('model.pkl', 'rb'))

##### Prints current directory
folder_location = os.getcwd()
print(folder_location)

############## Changes to given directory
#os.chdir(r'static/files')

### NOW PRINT THE CHANGED DIRECTORY
#print(os.getcwd())

app.config["FILE_UPLOADS"] = folder_location + r"\\static\\files\\"


@app.route('/download_file', methods=["GET", "POST"])
def download_file():
    from functions.sqlquery import sql_query, sql_download
    fetched = request.args.get('fetched')
    print(fetched)
     #with open(r'C:\Users\Shreya Walia\jenny\static\images\', 'rb') as static_file:
    return render_template('view_file.html', uploaded_file="/static/files/" + fetched)

#####THIS IS FOR BUTTON SEARCH OF SDG
def get_sdg(sdg):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    sdg = '% '+sdg+' %'
    #print(sdg)
    post_for_sdg = conn.execute('SELECT id, date, entered_by, title, about, department, sdgs, upload, name FROM data_table_2 WHERE sdgs LIKE ?',
                        (sdg,)).fetchall()
    conn.close()
    
    return post_for_sdg

#####THIS IS FOR BUTTON SEARCH OF DEPARTMENT
def get_department(department):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    #department = 'Academic'
    department = '%'+department+'%'
    print(department)
    post_for_department = conn.execute('SELECT id, date, entered_by, title, about, department, sdgs, upload, name FROM data_table_2 WHERE department LIKE ?',
                        (department,)).fetchall()
    conn.close()
    return post_for_department

######## HOME PAGE

@app.route('/') 
def sql_database():
    from functions.sqlquery import sql_query
    results = sql_query(''' SELECT * FROM data_table_2''')
    msg = 'SELECT * FROM data_table_2'
    return render_template('home_page.html', results=results, msg=msg)   

######## INSERT DATA IN HOME PAGE

@app.route('/insert',methods = ['POST', 'GET']) #this is when user submits an insert
def sql_datainsert():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':

        date = request.form['date']
        if date == '':
            abort(406)
        entered_by = request.form['entered_by']
        title = request.form['title']
        about = request.form['about']
        print(about)  
        new_string = about
        print("*********CHANGE CHANGE***********************************+         NEW STRING    " + new_string)
        chars = ['\n','\n\n','\t', ';', ':', '!', "*", ".", " ", "'", "?", "/", "\\", "*", ",", "(", ")", "{", "}", "<", ">", "[", "]", "@", "#", "$", "%", "^", "&", "*", "-", "_", "+", "=", "\"", "\'"]
        for i in chars:
            new_string = new_string.replace(i, '')
        print("*********CHANGE CHANGE***********************************+             "+ new_string)
        print("########################################################## ABOUT "+ about)
        #details_table = form.details.data   
        #print(details_table)

        ########### Department list #######

        department_list = request.form.getlist("department[]")
        print(request.form.getlist("department[]"))
        department = ', '.join(department_list)
        print(department)
        ###################################

        amin = request.form.getlist("sdg[]")
        print(request.form.getlist("sdg[]"))
        sdgs = ','.join(amin)
        print(sdgs)
        upload = request.form['upload'] 
        #search = 4equest.form['search']
        #print(search)
        if upload == 'Yes': 

            f = request.files['other_file']
            
            name = f.filename
            #data = f.read()
           
            f.save(os.path.join(app.config["FILE_UPLOADS"], name))
            f.close()
            data = "NO DATA AS OF NOW"
        else:
            name = "NO FILE ATTACHED"
            data = "NO FILE ATTACHED"
      
       
        sql_edit_insert(''' INSERT INTO data_table_2 ( date, entered_by, title, about, department, sdgs, upload, name, new_string) VALUES ( ?, ?, ?,?, ?,?,?, ?, ?) ''', (date, entered_by, title, about, department, sdgs, upload, name,  new_string) )
        
        flash(f' Previous details saved successfully!', 'success')
        return redirect(url_for('sql_database'))
        #prediction_to_print = 'sdgs can be {}{}'.format(output, o)
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    
    return render_template('home_page.html', results=results) 

######## DELETE RECORDS

@app.route('/delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query
    if request.method == 'GET':
        ldate = request.args.get('ldate')
        ltitle = request.args.get('ltitle')
        #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #r = confirm("Press a button!");
        #if r == True:
            #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #else: 
            #print("Delete cancelled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!s")
        sql_delete(''' DELETE FROM data_table_2 where date = ? and title = ?''', (ldate, ltitle) )
        flash('Selected record deleted successfully!', 'danger alert-dismissible fade show')
    results = sql_query(''' SELECT * FROM data_table_2''')
    #msg = 'DELETE FROM data_table WHERE date = ' + ldate + ' and title = ' + ltitle
   
    #return render_template('sqldatabase.html', results=results, msg=msg)
    return render_template('new_view.html',  results = results)
############################## FOR DETELE AND REDIRECT, AFTER SEARCH #####################
 






######## #######################  EDIT LINK FOR RECORDS   ################################

@app.route('/query_edit',methods = ['POST', 'GET']) #this is when user clicks edit link
def sql_editlink():
    from functions.sqlquery import sql_query, sql_query2
    if request.method == 'GET':
        #elname = request.args.get('elname')
        edit_title = request.args.get('edit_title') 

        #efname = request.args.get('efname')
        edit_date = request.args.get('edit_date')

        eresults = sql_query2(''' SELECT * FROM data_table_2 where date = ? and title = ?''', (edit_date,edit_title))
    results = sql_query(''' SELECT * FROM data_table_2''')
    return render_template('update_page.html', eresults=eresults, results=results)


######################################### EDIT PAGE FOR VIEW ALL ###################################################33

@app.route('/edit',methods = ['POST', 'GET']) #this is when user submits an edit
def sql_dataedit():
    from functions.sqlquery import sql_edit_insert, sql_query
    if request.method == 'POST':
        #old_last_name = request.form['old_last_name']
        old_title = request.form['old_title'] 
        #old_first_name = request.form['old_first_name']
        old_date = request.form['old_date']
          
        #last_name = request.form['last_name']
        title = request.form['title'] 

        #first_name = request.form['first_name']
        date = request.form['date']
        entered_by = request.form['entered_by']

        about = request.form['about']
        print(about)  
        new_string = about
        print("*********CHNAGE CHANGE***********************************+         NEW STRING    " + new_string)
        chars = ['\n','\n\n','\t', ';', ':', '!', "*", ".", " ", "'", "?", "/", "\\", "*", ",", "(", ")", "{", "}", "<", ">", "[", "]", "@", "#", "$", "%", "^", "&", "*", "-", "_", "+", "=", "\"", "\'"]
        for i in chars:
            new_string = new_string.replace(i, '')
        print("*********CHNAGE CHANGE***********************************+    MODIFIED NEW STRING    "+ new_string)
        print("########################################################## ABOUT "+ about)

         ########### Department list #######

        department_list = request.form.getlist("department[]")
        print(request.form.getlist("department[]"))
        department = ', '.join(department_list)
        print(department)

        amin = request.form.getlist("sdg[]")
        print(request.form.getlist("sdg[]"))
        sdgs = ','.join(amin)
        print(sdgs)
        upload = request.form['upload']  
        if upload == 'Yes': 

        #### MAKING CHANGES HERE #########
            #### MAKING CHANGES HERE #########
            f = request.files['other_file']
            
            name = f.filename
            f.save(os.path.join(app.config["FILE_UPLOADS"], name))
            f.close()

            data = "NO DATA AS OF NOW"
        else:
            name = "NO FILE ATTACHED"
            data = "NO FILE ATTACHED"

        sql_edit_insert(''' UPDATE data_table_2 set date = ?, entered_by = ?, title = ?, about = ?, department = ?, sdgs = ?, upload = ?, name = ?,  new_string = ?  WHERE date=? and title=? ''', (date, entered_by, title, about, department, sdgs, upload, name,  new_string, old_date,old_title) )
        

    results = sql_query(''' SELECT * FROM data_table_2''')
    return render_template('update_confirmation.html', results=results)



###################### VIEW ALL RECORDS URL  #####################33
@app.route('/view',methods = ['POST', 'GET']) #this is when user submits an edit
def view():
    from functions.sqlquery import sql_query
    
    
    results = sql_query(''' SELECT * FROM data_table_2 ORDER BY id DESC ''') 
    msg = "Saved successfully!"
    return render_template('new_view.html', results=results, msg=msg) 
    

############  SEARCH BY SDGS TEXT INPUT URLLLLLLLLL  ###################

@app.route('/search_sdg_page',methods = ['POST', 'GET']) #this is when user submits an edit
def search_sdg_page():
    from functions.sqlquery import sql_query_search, sql_query

    if request.method == "POST":
        sdg = request.form['sdg']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    return render_template('sdg_search.html', results=results)

#########################  SEARCH SDG FUNTION FOR BUTTON

@app.route('/search', methods=['GET', 'POST'])
def search():
    from functions.sqlquery import sql_query_search, sql_query
    if request.method == 'POST':
        #elname = request.args.get('elname')
        #sdg = "%six %"
        sdg = request.form['sdg']

        print(sdg)
        sdg = "% "+sdg+" %"
        #sdg = sdg+" %"
        print(sdg)
        typed_sdg = request.args.get('typed_sdg') 
        print(typed_sdg)
    
        results = sql_query_search(''' SELECT id, date, entered_by, title, about, department, sdgs, upload, name, new_string FROM data_table_2 WHERE sdgs LIKE ? ''', (sdg,))
        if not results:
            
            return render_template('no_result.html')
        else:
            return render_template('sdg_searched_page.html', results=results)




############  SEARCH BY NAME TEXT INPUT URLLLLLLLLL  ###################

@app.route('/search_name_page',methods = ['POST', 'GET']) #this is when user submits an edit
def search_name_page():
    from functions.sqlquery import sql_query_search, sql_query

    if request.method == "POST":
        entered_by = request.form['entered_by']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    return render_template('name_search.html', results=results)

#########################  SEARCH NAME FUNTION FOR BUTTON

@app.route('/search_name_display', methods=['GET', 'POST'])
def search_name_display():
    from functions.sqlquery import sql_query_search, sql_query
    if request.method == 'POST':
        #elname = request.args.get('elname')
        #sdg = "%six %"
        entered_by = request.form['entered_by']
        print(entered_by)
        entered_by = "%"+entered_by+"%"
        print(entered_by)
       
    results = sql_query_search(''' SELECT id, date, entered_by, title, about, department, sdgs, upload, name, new_string FROM data_table_2 WHERE entered_by LIKE ? ''', (entered_by,))
    if not results:
            
        return render_template('no_result.html')
    else:
        return render_template('name_searched_page.html', results=results)


############  SEARCH BY DEPARTMENT TEXT INPUT URLLLLLLLLL  ###################

@app.route('/search_department_page',methods = ['POST', 'GET']) #this is when user submits an edit
def search_department_page():
    from functions.sqlquery import sql_query_search, sql_query

    if request.method == "POST":
        department = request.form['department']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    return render_template('department_search.html', results=results)

#########################  SEARCH DEPARTMENT FUNTION FOR BUTTON

@app.route('/search_department_display', methods=['GET', 'POST'])
def search_department_display():
    from functions.sqlquery import sql_query_search, sql_query
    if request.method == 'POST':
        #elname = request.args.get('elname')
        #sdg = "%six %"
        department = request.form['department']
        print(department)
        department = "%"+department+"%"
        print(department)
       
    results = sql_query_search(''' SELECT id, date, entered_by, title, about, department, sdgs, upload, name, new_string FROM data_table_2 WHERE department LIKE ? ''', (department,))
    if not results:
            
        return render_template('no_result.html')
    else:
        return render_template('department_searched_page.html', results=results)



################################ FOR BUTTON SEARCH OF SDGS

@app.route('/<string:sdg>')
def post_for_sdg(sdg):
    post_for_sdg = get_sdg(sdg)
    if not post_for_sdg:
        return render_template('no_result.html')
    else:
        return render_template('post_for_sdg.html', post_for_sdg=post_for_sdg)

################################ FOR BUTTON SEARCH OF Department

@app.route('/search_department_page/<string:department>')
def post_for_department(department):
    #department='Academic'
    post_for_department = get_department(department)
    if not post_for_department:
        return render_template('no_result.html')
    else:
        return render_template('post_for_department.html', post_for_department=post_for_department)


#def search():
#endpoint for search
#@app.route('/search', methods=['GET', 'POST'])
#def search():
#    from functions.sqlquery import sql_query_search, sql_query
#    if request.method == "POST":
        #upload = request.form['sdg']
#        upload = 'yes'
#        print(upload)

        #sdg = '%'+sdg+'%'
#        print("%&**********###########" +     upload)
        # search by author or book
        #sql_query_search(''' SELECT date, title, about, sdgs, upload, name FROM data_table WHERE upload LIKE ?''', (upload,))
        #data = conn.execute('SELECT date, title, about, sdgs, upload, name FROM data_table WHERE sdgs LIKE ?', (sdg,)).fetchall()
        
        
        # all in the search box will return all the tuples      
       
        #return render_template('newnew_search.html', data=data)
#        data = sql_query_search(''' SELECT date, title, about, sdgs, upload, name FROM data_table WHERE upload LIKE ?''', (upload,))
    #data = sql_query(''' SELECT * FROM data_table''')    
#        return render_template('newnew_search.html', data = data)    

############################## FOR DETELE AND REDIRECT, AFTER SEARCH OF SDG #####################
 
@app.route('/sdg_delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def sdg_sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query2
    if request.method == 'GET':
        ldate = request.args.get('ldate')
        ltitle = request.args.get('ltitle')
        #sdg = request.args.get('sdgs')
        #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #r = confirm("Press a button!");
        #if r == True:
            #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #else: 
            #print("Delete cancelled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!s")
        sql_delete(''' DELETE FROM data_table_2 where date = ? and title = ?''', (ldate, ltitle) )
        
        flash('Selected record deleted successfully!', 'danger alert-dismissible fade show')
    return render_template('delete_confirmation_for_SDG.html')

############################## FOR DETELE AND REDIRECT, AFTER SEARCH OF NAME #####################
 
@app.route('/name_delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def name_sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query2
    if request.method == 'GET':
        ldate = request.args.get('ldate')
        ltitle = request.args.get('ltitle')
        #sdg = request.args.get('sdgs')
        #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #r = confirm("Press a button!");
        #if r == True:
            #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #else: 
            #print("Delete cancelled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!s")
        sql_delete(''' DELETE FROM data_table_2 where date = ? and title = ?''', (ldate, ltitle) )
        
        flash('Selected record deleted successfully!', 'danger alert-dismissible fade show')
    return render_template('delete_confirmation_for_name.html')

############################## FOR DETELE AND REDIRECT, AFTER SEARCH OF DEPARTMENT #####################
 
@app.route('/department_delete',methods = ['POST', 'GET']) #this is when user clicks delete link
def department_sql_datadelete():
    from functions.sqlquery import sql_delete, sql_query2
    if request.method == 'GET':
        ldate = request.args.get('ldate')
        ltitle = request.args.get('ltitle')
        #sdg = request.args.get('sdgs')
        #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #r = confirm("Press a button!");
        #if r == True:
            #sql_delete(''' DELETE FROM data_table where date = ? and title = ?''', (ldate, ltitle) )
        #else: 
            #print("Delete cancelled!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!s")
        sql_delete(''' DELETE FROM data_table_2 where date = ? and title = ?''', (ldate, ltitle) )
        
        flash('Selected record deleted successfully!', 'danger alert-dismissible fade show')
    return render_template('delete_confirmation_for_department.html')










############################ SORT BY DATE   ######################################3

@app.route('/sort_by_date',methods = ['POST', 'GET']) #this is when user submits an edit
def sort_by_date():
    from functions.sqlquery import sql_query_search, sql_query

    #if request.method == "POST":
        #entered_by = request.form['entered_by']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ORDER BY date ASC''')
    return render_template('new_view.html', results=results)





############  PRECIDTIOM INPUT URLLLLLLLLL  FROM HOME PAGE ###################

@app.route('/predict_url',methods = ['POST', 'GET']) #this is when user submits an edit
def predict_url():
    from functions.sqlquery import sql_query_search, sql_query

    if request.method == "POST":
        about = request.form['about']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    return render_template('prediction_page.html', results=results)
        #return render_template('prediction_page.html')

#########################  SEARCH FUNTION FOR BUTTON









#########################     MODEL FOR PREDICTION  IN INSERT PAGE FROM HOME PAGE #############
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        input_text = request.form['about']
        print(input_text)
        text = lower(input_text)
        text = cleanHtml(text)
        text = cleanPunc(text)
        text = keepAlpha(text)
        tfidf = model.best_estimator_.named_steps['tfidf']
        final_features = tfidf.transform([text])
        clf = model.best_estimator_.named_steps['clf']
        prediction = clf.predict(final_features)

    output = prediction
    
    # target = {output[:,0]:'Goal 1', output[:,1]:'Goal 2', output[:,2]:'Goal 3', output[:,3]:'Goal 4', 
    #           output[:,4]:'Goal 5', output[:,5]:'Goal 6', output[:,6]:'Goal 7', output[:,7]:'Goal 8',
    #           output[:,8]:'Goal 9', output[:,9]:'Goal 10', output[:,10]:'Goal 11', output[:,11]:'Goal 12',
    #           output[:,12]:'Goal 13', output[:,13]:'Goal 14', output[:,14]:'Goal 15', output[:,15]:'Goal 16',
    #           output[:,16]:'Goal 17'}

    #print(text)
    o = ''
    sdg_list = ["No poverty", "Zero hunger" ,"Good health and well being", "Quality education", "Gender equality", "Clean water and sanitation", "Affordable and clean energy", "Decent work and economic growth", "Industry, innovation and infrastructure", "Reduced inequalities", "Sustainable cities and communities", "Responsible consumption and production", "Climate action", "Life below water", "Life on land", "Peace, justice and strong intuitions", "Partnerships for the goals"]
    for i in range(1,18):
        if output[0][i-1] == 1:
            x = 'Goal ' + str(i) + ": " + sdg_list[i-1] + '; ' 
            o = o +  x + " "   
    return render_template('prediction_page.html', prediction_text=' \n {}\n'.format(o))

############  PRECIDTIOM INPUT URLLLLLLLLL  FROM UPDATE PAGE ###################

@app.route('/predict_url_2',methods = ['POST', 'GET']) #this is when user submits an edit
def predict_url_2():
    from functions.sqlquery import sql_query_search, sql_query

    if request.method == "POST":
        about = request.form['about']
        #print("******************USER ENTERED****************************" + sdg)
        #print(sdg)
        #sdg = '%'+sdg+' %'
        #print("##########################################   "+sdg+"   ##########################") 
    #######THIS RESULTS BELOW ACTUALLY DOES NOT MATTER AT ALL--------PASS ANY QUERY, WHATEVER1111    
    results = sql_query(''' SELECT * FROM data_table_2 ''')
    return render_template('prediction_page_2.html', results=results)


#########################     MODEL FOR PREDICTION  IN UPDATE PAGE #############
@app.route('/predict_2',methods=['POST'])
def predict_2():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        input_text = request.form['about']
        print(input_text)
        text = lower(input_text)
        text = cleanHtml(text)
        text = cleanPunc(text)
        text = keepAlpha(text)
        tfidf = model.best_estimator_.named_steps['tfidf']
        final_features = tfidf.transform([text])
        clf = model.best_estimator_.named_steps['clf']
        prediction = clf.predict(final_features)

    output = prediction
    
    # target = {output[:,0]:'Goal 1', output[:,1]:'Goal 2', output[:,2]:'Goal 3', output[:,3]:'Goal 4', 
    #           output[:,4]:'Goal 5', output[:,5]:'Goal 6', output[:,6]:'Goal 7', output[:,7]:'Goal 8',
    #           output[:,8]:'Goal 9', output[:,9]:'Goal 10', output[:,10]:'Goal 11', output[:,11]:'Goal 12',
    #           output[:,12]:'Goal 13', output[:,13]:'Goal 14', output[:,14]:'Goal 15', output[:,15]:'Goal 16',
    #           output[:,16]:'Goal 17'}

    #print(text)
    o = ''
    for i in range(1,18):
        if output[0][i-1] == 1:
            x = 'Goal' + str(i) + '; '
            o = o + " " + x   
    return render_template('prediction_page_2.html', prediction_text='sdgs can be {}{}'.format(output, o))
    #return render_template('sqldatabase.html', prediction_text='sdgs can be {}{}'.format(output, o))
    



@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    text = lower(data)
    text = cleanHtml(text)
    text = cleanPunc(text)
    text = keepAlpha(text)
    tfidf = model.best_estimator_.named_steps['tfidf']
    final_features = tfidf.transform([text])
    clf = model.best_estimator_.named_steps['clf']
    prediction = clf.predict(final_features)

    output = prediction
    return jsonify(output)


#if __name__ == "__main__":
#    app.run(debug=True)


def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == "__main__":
    Timer(1, open_browser).start();
    app.run(port=5000)