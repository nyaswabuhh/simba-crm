from flask import Flask, render_template, request,redirect, url_for
from database import conn,cur
import datetime

app=Flask(__name__)



@app.route('/')
def index():
    today_leads_query= "SELECT COALESCE(COUNT(*)) FROM leads WHERE DATE(created_at) = CURRENT_DATE"
    cur.execute(today_leads_query)
    today_leads = int(cur.fetchone()[0])

    today_notes_query = "SELECT COALESCE(COUNT(*)) FROM lead_notes WHERE DATE(created_at) = CURRENT_DATE"
    cur.execute(today_notes_query)
    today_notes = int(cur.fetchone()[0])

    today_followups_query = "SELECT COALESCE(COUNT(*)) FROM leads WHERE DATE(next_followup) = CURRENT_DATE"
    cur.execute(today_followups_query)
    today_followups = int(cur.fetchone()[0])

    now = datetime.datetime.now()
    today_date = now.strftime("%Y-%m-%d")

    week_leads_query = "SELECT COALESCE(COUNT(*)) FROM leads WHERE DATE(created_at) BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE"
    cur.execute(week_leads_query)
    week_leads = int(cur.fetchone()[0])

    week_followups_query = "SELECT COALESCE(COUNT(*)) FROM leads WHERE DATE(next_followup) = CURRENT_DATE + INTERVAL '1 days'"
    cur.execute(week_followups_query)
    week_followups = int(cur.fetchone()[0])

    week_notes_query = "SELECT COALESCE(COUNT(*)) FROM lead_notes WHERE DATE(created_at) BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE"
    cur.execute(week_notes_query)
    week_notes = int(cur.fetchone()[0])

    lead_status_query = "SELECT lead_stages.lead_stage, COUNT(*) FROM leads JOIN lead_stages ON lead_stages.lead_stage_id=leads.lead_stage GROUP BY lead_stages.lead_stage"
    cur.execute(lead_status_query)
    lead_status = cur.fetchall()

    x=[]
    y=[]

    for i in lead_status:
        x.append(i[0])
        y.append(i[1])

    leadsperstaff_query = "SELECT staff.staff_firstname, COUNT(*) FROM leads JOIN staff ON staff.staff_id=leads.assignedstaff_fk GROUP BY staff.staff_firstname"
    cur.execute(leadsperstaff_query)
    leadsperstaff = cur.fetchall()

    leadspersource_query = "SELECT lead_sources.source, COUNT(*) FROM leads JOIN lead_sources ON lead_sources.lead_source_id=leads.lead_source GROUP BY lead_sources.source"
    cur.execute(leadspersource_query)
    leadspersource = cur.fetchall()

    a=[]
    b=[]

    for i in leadspersource:
        a.append(i[0])
        b.append(i[1])

    business_types_query = "SELECT business_type.biz_type_name, COUNT(*) FROM leads JOIN business_type ON business_type.business_type_id=leads.business_type_fk GROUP BY business_type.biz_type_name"
    cur.execute(business_types_query)
    business_types = cur.fetchall()

    c=[]
    d=[]
    for i in business_types:
        c.append(i[0])
        d.append(i[1])
        print(c, d)

    return render_template('home.html',c=c, d=d, a=a, b=b,x=x, y=y,today_leads=today_leads, today_notes=today_notes, today_followups=today_followups, today_date=today_date, week_leads=week_leads, week_followups=week_followups, week_notes=week_notes, lead_status=lead_status, leadsperstaff=leadsperstaff,leadspersource=leadspersource, business_types=business_types)

@app.route('/leads', methods=['GET','POST'])
def leads():
    if request.method == 'GET':
        # cur.execute("SELECT lead_id, lead_firstname, lead_lastname,lead_phone, business_location,lead_potential, created_at,assignedstaff_fk,next_followup FROM leads ORDER BY created_at DESC")
        cur.execute("SELECT * FROM leads order by created_at DESC")
        leads = cur.fetchall()
        cur.execute("SELECT * FROM staff")
        staff = cur.fetchall()
        cur.execute("SELECT * FROM revenue_centers")
        revenue_centers = cur.fetchall()
        cur.execute("SELECT * FROM lead_stages")
        lead_stages = cur.fetchall()
        cur.execute("SELECT * FROM lead_sources")
        lead_sources = cur.fetchall()
        cur.execute("SELECT * FROM business_type")
        business_types = cur.fetchall()
        cur.execute("SELECT * FROM counties")
        counties = cur.fetchall()
    

        return render_template('leads.html',business_types=business_types, leads=leads, staff=staff, revenue_centers=revenue_centers, lead_stages=lead_stages, lead_sources=lead_sources, counties=counties)
    else:
        lead_firstname = request.form['lead_firstname']
        lead_lastname = request.form['lead_lastname']
        lead_phone = request.form['lead_phone']
        email = request.form['email']
        county_fk  = int(request.form['county_fk'])
        business_location = request.form['business_location']
        position = request.form['position']
        lead_potential = int(request.form['lead_potential'])
        created_by = int(request.form['created_by'])
        business_type_fk = int(request.form['business_type_fk'])
        revcenter_fk = int(request.form['revcenter_fk'])
        assignedstaff_fk = int(request.form['assignedstaff_fk'])
        lead_source= int(request.form['lead_source'])
        lead_stage = int(request.form['lead_stage'])
        next_followup = request.form['next_followup']
        close_date = request.form['close_date']
        

        lead_query = "INSERT INTO leads(lead_firstname, lead_lastname, lead_phone, email, county_fk, business_location, position, lead_potential, created_by, business_type_fk,revcenter_fk, assignedstaff_fk, lead_source, lead_stage, next_followup, close_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(lead_firstname, lead_lastname, lead_phone, email, county_fk,business_location, position, lead_potential, created_by, business_type_fk,revcenter_fk, assignedstaff_fk, lead_source, lead_stage, next_followup, close_date)
        
        print(lead_query)
        cur.execute(*lead_query)

        conn.commit()
        return redirect('/leads')
    
@app.route('/update-lead', methods=['POST'])
def update_lead():
    if request.method == 'POST':
        lead_id = request.form['lead_id']
        lead_firstname = request.form['lead_firstname']
        lead_lastname = request.form['lead_lastname']
        lead_phone = request.form['lead_phone']
        email = request.form['email']
        county_fk  = int(request.form['county_fk'])
        business_location = request.form['business_location']
        position = request.form['position']
        lead_potential = int(request.form['lead_potential'])
        created_by = int(request.form['created_by'])
        business_type_fk = int(request.form['business_type_fk'])
        revcenter_fk = int(request.form['revcenter_fk'])
        assignedstaff_fk = int(request.form['assignedstaff_fk'])
        lead_source= int(request.form['lead_source'])
        lead_stage = int(request.form['lead_stage'])
        next_followup = request.form['next_followup']
        close_date = request.form['close_date']
        

        # lead_upquery = "UPDATE leads SET lead_firstname=%s, lead_lastname=%s, lead_phone=%s, email=%s, county_fk=%s, business_location=%s, position=%s, lead_potential=%s, created_by=%s, business_type_fk=%s,revcenter_fk=%s, assignedstaff_fk=%s, lead_source=%s, lead_stage=%s, next_followup=%, close_date=%s WHERE lead_id=%s",(lead_firstname, lead_lastname, lead_phone, email, county_fk, business_location, position, lead_potential, created_by, business_type_fk,revcenter_fk, assignedstaff_fk, lead_source, lead_stage, next_followup,lead_id)

        lead_query = "UPDATE leads SET lead_firstname=%s, lead_lastname=%s, lead_phone=%s, email=%s, county_fk=%s, business_location=%s, position=%s, lead_potential=%s, created_by=%s, business_type_fk=%s,revcenter_fk=%s, assignedstaff_fk=%s, lead_source=%s, lead_stage=%s, next_followup=%s, close_date=%s WHERE lead_id=%s",(lead_firstname, lead_lastname, lead_phone, email, county_fk, business_location, position, lead_potential, created_by, business_type_fk,revcenter_fk, assignedstaff_fk, lead_source, lead_stage, next_followup,close_date,lead_id)
        print(lead_query)
        cur.execute(*lead_query)
        conn.commit()
        return redirect('/leads')
    
@app.route('/lead-notes', methods=['GET','POST'])
def lead_notes():
    if request.method == 'GET':
        cur.execute("SELECT lead_notes.lead_note_id,lead_notes.lead_note,leads.lead_firstname, lead_lastname,lead_notes.created_at FROM lead_notes JOIN leads ON lead_notes.lead_id=leads.lead_id ORDER BY lead_notes.created_at DESC")
        lead_notes = cur.fetchall()
        cur.execute("SELECT * FROM leads")
        leads = cur.fetchall()
        cur.execute("SELECT * FROM staff")
        staff = cur.fetchall()
        return render_template('lead_notes.html',lead_notes=lead_notes, leads=leads, staff=staff)
    else:
        lead_note= request.form['lead_note']
        lead_id = int(request.form['lead_id'])        

        note_query = "INSERT INTO lead_notes(lead_note, lead_id) VALUES (%s,%s)",(lead_note, lead_id)
        cur.execute(*note_query)
        conn.commit()
        return redirect('/lead-notes')
    
@app.route('/lead-sources', methods=['GET','POST'])
def lead_sources():
    if request.method == 'GET':
        cur.execute("SELECT * FROM lead_sources order by last_update ASC")
        lead_sources = cur.fetchall()
        return render_template('lead_sources.html',lead_sources=lead_sources)
    else:
        lead_source = request.form['lead_source']
        source_query = "INSERT INTO lead_sources(source) VALUES (%s)",(lead_source,)
        cur.execute(*source_query)
        conn.commit()
        return redirect('/lead-sources')

@app.route('/lead-stages', methods=['GET','POST'])
def lead_stages():
    if request.method == 'GET':
        cur.execute("SELECT * FROM lead_stages order by last_update ASC")
        lead_stages = cur.fetchall()
        return render_template('lead_stages.html',lead_stages=lead_stages)
    else:
        lead_stage = request.form['lead_stage']
        stage_query = "INSERT INTO lead_stages(lead_stage) VALUES (%s)",(lead_stage,)
        cur.execute(*stage_query)
        conn.commit()
        return redirect('/lead-stages')
    
@app.route('/revenue-centers', methods=['GET','POST'])
def revenue_centers():
    if request.method == 'GET':
        cur.execute("SELECT * FROM revenue_centers")
        revenue_centers = cur.fetchall()
        return render_template('revenue_centers.html',revenue_centers=revenue_centers)
    else:
        revenue_center_name = request.form['revenue_center_name']
        description = request.form['description']
        center_query = "INSERT INTO revenue_centers(revenue_center_name, description) VALUES (%s,%s)",(revenue_center_name,description)
        cur.execute(*center_query)
        conn.commit()
        return redirect('/revenue-centers') 
    
@app.route('/business-types', methods=['GET','POST'])
def business_types():
    if request.method == 'GET':
        cur.execute("SELECT * FROM business_type")
        business_types = cur.fetchall()
        return render_template('business_types.html',business_types=business_types)
    else:
        biz_type_name = request.form['biz_type_name']
        biz_type_descr= request.form['biz_type_descr']
        type_query = "INSERT INTO business_type(biz_type_name, biz_type_descr) VALUES (%s,%s)",(biz_type_name,biz_type_descr)
        cur.execute(*type_query)
        conn.commit()
        return redirect('/business-types')

@app.route('/staff', methods=['GET','POST'])
def staff():
    if request.method == 'GET':
        cur.execute("SELECT * FROM staff order by staff_id ASC")
        staff = cur.fetchall()
        return render_template('staff.html',staff=staff)
    else:
        staff_nationalid = request.form['staff_nationalid']
        staff_firstname = request.form['staff_firstname']
        staff_lastname = request.form['staff_lastname']
        staff_phone = request.form['staff_phone']
        email = request.form['email']
        date_of_employment = request.form['date_of_employment']
        position = request.form['position']

        staff_query = "INSERT INTO staff(staff_nationalid, staff_firstname, staff_lastname, staff_phone, email, date_of_employment, position) VALUES (%s,%s,%s,%s,%s,%s,%s)",(staff_nationalid,staff_firstname,staff_lastname,staff_phone,email,date_of_employment,position)
        cur.execute(*staff_query)
        conn.commit()
        return redirect('/staff')
    
@app.route('/update-staff', methods=['POST'])
def update_staff():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        staff_nationalid = request.form['staff_nationalid']
        staff_firstname = request.form['staff_firstname']
        staff_lastname = request.form['staff_lastname']
        staff_phone = request.form['staff_phone']
        email = request.form['email']
        date_of_employment = request.form['date_of_employment']
        position = request.form['position']

        staff_query = "UPDATE staff SET staff_nationalid=%s, staff_firstname=%s, staff_lastname=%s, staff_phone=%s, email=%s, date_of_employment=%s, position=%s WHERE staff_id=%s",(staff_nationalid,staff_firstname,staff_lastname,staff_phone,email,date_of_employment,position,staff_id)
        cur.execute(*staff_query)
        conn.commit()
        return redirect('/staff')
    
@app.route('/item-categories', methods=['GET','POST'])
def item_categories():
    if request.method == 'GET':
        cur.execute("SELECT * FROM item_categories")
        item_categories = cur.fetchall()
        return render_template('item_categories.html',item_categories=item_categories)
    else:
        category_name = request.form['category_name']
        category_description = request.form['category_description']
        category_query = "INSERT INTO item_categories(category_name, category_description) VALUES (%s,%s)",(category_name,category_description)
        cur.execute(*category_query)
        conn.commit()
        return redirect('/item-categories')

@app.route('/items', methods=['GET','POST'])
def items():
    if request.method == 'GET':
        cur.execute("SELECT items.item_id,items.item_name,items.item_descr,item_categories.category_name,items.item_price FROM items JOIN item_categories ON items.item_category=item_categories.item_category_id")
        items = cur.fetchall()
        cur.execute("SELECT * FROM item_categories")
        categories = cur.fetchall()        
        return render_template('items.html',items=items, categories=categories)
    else:
        item_name = request.form['item_name']
        item_descr = request.form['item_descr']
        item_category = int(request.form['item_category'])
        item_price = request.form['item_price']
        is_stock = request.form['is_stock']
        if is_stock == 1:
            is_stock = True
        else:
            is_stock = False
        
        item_query = "INSERT INTO items(item_name, item_descr, item_category, item_price, is_stock) VALUES (%s,%s,%s,%s,%s)",(item_name,item_descr,item_category,item_price,is_stock)
        cur.execute(*item_query)
        conn.commit()
        return redirect('/items')         
        
@app.route('/today-followup', methods=['GET','POST'])
def today_followup():
    if request.method == 'GET':
        cur.execute("SELECT * FROM leads WHERE DATE(next_followup) = CURRENT_DATE")
        leads = cur.fetchall()
        cur.execute("SELECT * FROM staff")
        staff = cur.fetchall()
        cur.execute("SELECT * FROM revenue_centers")
        revenue_centers = cur.fetchall()
        cur.execute("SELECT * FROM lead_stages")
        lead_stages = cur.fetchall()
        cur.execute("SELECT * FROM lead_sources")
        lead_sources = cur.fetchall()
        cur.execute("SELECT * FROM business_type")
        business_types = cur.fetchall()
        cur.execute("SELECT * FROM counties")
        counties = cur.fetchall()

        return render_template('today_followup.html',leads=leads, staff=staff, revenue_centers=revenue_centers, lead_stages=lead_stages, lead_sources=lead_sources, business_types=business_types, counties=counties)
    else:
        update_lead()

        return render_template('today_followup.html')
    
@app.route('/leads/<lead_id>', methods=['GET'])
def lead_details(lead_id):
    cur.execute("SELECT * FROM leads WHERE lead_id=%s",(lead_id,))
    lead = cur.fetchone()
    cur.execute("SELECT * FROM lead_notes WHERE lead_id=%s order by created_at DESC",(lead_id,))
    lead_notes = cur.fetchall()
    return render_template('lead_details.html',lead=lead, lead_notes=lead_notes)

@app.route('/counties', methods=['GET','POST'])
def counties():
    if request.method == 'GET':
        cur.execute("SELECT * FROM counties")
        counties = cur.fetchall()
        return render_template('county_names.html',counties=counties)
    else:
        county_name = request.form['county_name']
        county_code = request.form['county_code']
        county_query = "INSERT INTO counties(county_name, county_code) VALUES (%s,%s)",(county_name,county_code)
        cur.execute(*county_query)
        conn.commit()
        return redirect('/counties')
    
@app.route('/company_details')
def company_details():
    cur.execute("SELECT * FROM company_details")
    company_details = cur.fetchall()

    return render_template('company_details.html', company_details=company_details)

@app.route('/customers', methods=['GET','POST'])
def customers():
    if request.method == 'GET':
        cur.execute("SELECT * FROM customers order by created_date DESC")
        customers = cur.fetchall()
        cur.execute("SELECT * FROM business_type")
        business_types = cur.fetchall()
        cur.execute("SELECT * FROM counties")
        counties = cur.fetchall()
        cur.execute("SELECT * FROM staff")
        staff = cur.fetchall()

        return render_template('customers.html',customers=customers, business_types=business_types, counties=counties, staff=staff)
    else:
        customer_fname = request.form['customer_fname']
        customer_sname = request.form['customer_sname']
        customer_phone = request.form ['customer_phone']
        customer_bizname = request.form['customer_bizname']
        business_type_fk = int(request.form['business_type_fk'])
        customer_email = request.form['customer_email']
        customer_website = request.form['customer_website']
        customer_address = request.form['customer_address']
        customer_building = request.form['customer_building']
        customer_street = request.form['customer_street']
        customer_town = request.form['customer_town']
        customer_county_fk = int(request.form['customer_county_fk'])
        customer_notes = request.form['customer_notes']
        next_followup = request.form['next_followup']

        customer_query = "INSERT INTO customers(customer_fname, customer_sname,customer_phone, customer_bizname, business_type_fk, customer_email, customer_website, customer_address, customer_building, customer_street, customer_town, customer_county_fk, customer_notes, next_followup) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(customer_fname, customer_sname,customer_phone, customer_bizname, business_type_fk, customer_email, customer_website, customer_address, customer_building, customer_street, customer_town, customer_county_fk, customer_notes, next_followup)
        cur.execute(*customer_query)
        conn.commit()

        return redirect('/customers')

@app.route('/update-customers', methods=['POST'])
def update_customers():
    if request.method =='POST':
        customer_id= int(request.form['customer_id'])
        customer_fname = request.form['customer_fname']
        customer_sname = request.form['customer_sname']
        customer_phone = request.form ['customer_phone']
        customer_bizname = request.form['customer_bizname']
        business_type_fk = int(request.form['business_type_fk'])
        customer_email = request.form['customer_email']
        customer_website = request.form['customer_website']
        customer_address = request.form['customer_address']
        customer_building = request.form['customer_building']
        customer_street = request.form['customer_street']
        customer_town = request.form['customer_town']
        customer_county_fk = int(request.form['customer_county_fk'])
        customer_notes = request.form['customer_notes']
        next_followup = request.form['next_followup']

        customer_upquery = "UPDATE customers SET customer_fname=%s, customer_sname=%s,customer_phone=%s, customer_bizname=%s, business_type_fk=%s, customer_email=%s, customer_website=%s, customer_address=%s, customer_building=%s, customer_street=%s, customer_town=%s, customer_county_fk=%s, customer_notes=%s, next_followup=%s WHERE customer_id=%s",(customer_fname, customer_sname,customer_phone, customer_bizname, business_type_fk, customer_email, customer_website, customer_address, customer_building, customer_street, customer_town, customer_county_fk, customer_notes, next_followup, customer_id)   
        print(customer_upquery)
        cur.execute(*customer_upquery)
        conn.commit()

        return redirect('/customers')      

@app.route('/customers/<customer_id>', methods=['GET'])
def customer_details(customer_id):
    cur.execute("SELECT * FROM customers WHERE customer_id=%s",(customer_id,))
    customer = cur.fetchone()

    cur.execute("SELECT * FROM customernotes WHERE customer_id_fk=%s",(customer_id))
    customer_notes=cur.fetchall()
    
    return render_template('customer_details.html',customer=customer, customer_notes=customer_notes)

@app.route('/customer-notes', methods=['GET','POST'])
def customer_notes():
    if request.method == 'GET':
        cur.execute("SELECT customernotes.customer_note_id,customernotes.customer_note,customers.customer_fname, customers.customer_bizname,customernotes.created_date FROM customernotes JOIN customers ON customernotes.customer_id_fk=customers.customer_id ORDER BY  customernotes.created_date DESC")
        customer_notes = cur.fetchall()
        
        cur.execute("SELECT * FROM staff")
        staff=cur.fetchall()

        cur.execute("SELECT * FROM customers")
        customers = cur.fetchall()

        return render_template('customer_notes.html',customer_notes=customer_notes, customers=customers, staff=staff)
    else:
        customer_note= request.form['customer_note']
        customer_id_fk = int(request.form['customer_id_fk']) 
        staff_id_fk = int(request.form['staff_id_fk'])       

        customer_note_query = "INSERT INTO customernotes(customer_note, customer_id_fk, staff_id_fk) VALUES (%s,%s,%s)",(customer_note, customer_id_fk, staff_id_fk)
        cur.execute(*customer_note_query)
        conn.commit()
        return redirect('/customer-notes')
        

if __name__ == '__main__':
    app.run(debug=True)

