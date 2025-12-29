from flask import render_template, redirect, request, url_for
from app import app
import json, base64
from app.forms import PickAddressForm, EnterLineForm, PrintButtonForm, EditAddressForm
from werkzeug.datastructures import MultiDict
from app.printer import Print
import app.address_bank as adb

printObj = Print()

@app.route('/index', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def step1():

    user = {'username' : 'Grandma'}

    form = PickAddressForm()

    if form.validate_on_submit():
        printObj.set_chosenAddress(form.whichAddress.data)

        # branch depending on which button was pressed
        if form.edit.data: # "Edit Address" button pressed
            return redirect('/edit')
        elif form.new.data: # "Add Address" button pressed
            return redirect('/edit?add=1')
        elif form.bulk.data:
            return redirect('/bulk/select')
        else:
            return redirect('/step2')
        
    return render_template('step1.html', title='Step 1', user=user, form=form)

@app.route('/step2', methods=['GET', 'POST'])
def step2():

    address = {}
    address['line0'] = "(Original: " + printObj.get_chosenAddress()[0] + ")"
    address['line1'] = printObj.getAddLine1()
    address['line2'] = printObj.getAddLine2()
    if address['line1'] == " ":
        address['prompt'] = "Type ENTIRE address with PERIOD after EACH LINE:"
        address['line0'] = " "
    else:
        address['prompt'] = "Type ONLY the NAME of the person this mail is for:"
    form = EnterLineForm()

    if form.validate_on_submit():
        if len(form.inputLine.data) > 0:
            printObj.set_firstLine(form.inputLine.data)
        else:
            printObj.set_firstLine(printObj.get_chosenAddress()[0])
        if printObj.get_chosenAddress()[1] == "ERROR":
            return redirect('/')
        return redirect('/step3')

    return render_template('step2.html', title="Step 2", form=form, address=address)


@app.route('/step3', methods=['GET', 'POST'])
def step3():
    return render_template('step3.html', title="Step 3")

@app.route('/stickerpos/<int:stickerNum>', methods=['GET', 'POST'])
def sticker(stickerNum):
    printObj.set_stickerLocation(stickerNum)
    address = {}
    address["line0"] = printObj.get_firstLine()
    address["line1"] = printObj.getAddLine1()
    address["line2"] = printObj.getAddLine2()
    printObj.genChosenSticker()
    form = PrintButtonForm()
    if form.validate_on_submit():
        if form.submit.data:
            printObj.startPrint()
            return redirect('/')
        else:
            return redirect('/')

    return render_template('verify.html', title="Verify", address=address, form=form)

@app.get('/bulk/select')
def bulk_select():
    addresses, _ = adb.readAddresses()
    return render_template("bulk_select.html", addresses=addresses)

@app.post('/bulk/edit')
def bulk_edit():
    # Each checkbox submits a base64 encoded JSON string
    selected_base64 = request.form.getlist("selected")
    selected = [json.loads(base64.b64decode(s).decode("utf-8")) for s in selected_base64]
    return render_template("bulk_edit.html", selected=selected)

@app.post("/bulk/sticker")
def bulk_sticker():
    line0 = request.form.getlist("line0") # can be changed
    line1 = request.form.getlist("line1")  
    line2 = request.form.getlist("line2")

    bulk_addresses = [[a, b, c] for a, b, c in zip(line0, line1, line2)]

    print(bulk_addresses)
    #TODO: add bulk_addresses to print object in some fashion

    #TODO: find a way to loop sticker selection and track remaining # left to pick
    return None #render_template("bulk_sticker.html")


@app.route('/edit', methods=['GET', 'POST'])
def edit():
    
    # Default values are for "Add Address"
    address = {}
    show_delete = False
    title = "Add Address"

    address_is_valid = True

    # If actually editing, change values and fill address
    if request.args.get("add") != '1':
        show_delete = True
        title = "Edit Address"
        address["line0"] = printObj.getAddLine0()
        address["line1"] = printObj.getAddLine1()
        address["line2"] = printObj.getAddLine2()

    form = EditAddressForm(data=MultiDict(address))
    if form.validate_on_submit():
        if form.cancel.data:
            return redirect('/')
            #If cancel is pressed, exit asap before stuff happens

        if form.delete.data:
            _, err = adb.delAddress(list(address.values()))
            if err:
                is_error = True
                success_message = err
            else:
                is_error = False
                success_message = "Address has been deleted"

            return render_template(
                "edit.html",
                title=title,
                form=form,
                address=form.data,
                show_delete=show_delete,
                address_is_valid=False,
                need_confirm=False, 
                success_message=success_message,
                is_error=is_error
            )
        
        address_is_valid, err = adb.validateAddress(
            [form.line0.data, form.line1.data, form.line2.data]
        )

        force_save = request.form.get('force_save') == '1'

        if not address_is_valid and not force_save:
            # This is when we ask user 'are you sure' when address invalid
            return render_template(
                "edit.html",
                title=title,
                form=form,
                address=form.data,
                show_delete=show_delete,
                address_is_valid=False,
                need_confirm=True,
                success_message=None,
                is_error=False
            )
        
        # At this point, the address is already valid or user has confirmed twice
        # Write address:
        
        newAddress = [form.line0.data, form.line1.data, form.line2.data]

        # If we are editing an existing address, show_delete is True
        if show_delete:
            oldAddress = list(address.values())
            success_message = "Address has been changed"
        else:
            oldAddress = None
            success_message = "Address has been added"
        
        _, err = adb.writeAddress(newAddress, oldAddress)
        
        if err:
            is_error = True
            success_message = err
        else:
            is_error = False

        return render_template(
            "edit.html",
            title=title,
            form=form,
            address=form.data,
            show_delete=show_delete,
            address_is_valid=True,
            need_confirm=False,
            success_message=success_message,
            is_error=is_error
        )
    
    # Default (on first visit)
    return render_template('edit.html', 
                           title="Edit Address", 
                           form=form, 
                           address=address, 
                           show_delete=show_delete,
                           address_is_valid=address_is_valid,
                           need_confirm=False,
                           success_message=None,
                           is_error=False
                           )