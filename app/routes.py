from flask import render_template, redirect
from app import app
from app.forms import PickAddressForm, EnterLineForm, PrintButtonForm
from app.printer import Print

printObj = Print()


@app.route('/', methods=['GET', 'POST'])
def step1():

    user = {'username' : 'Grandma'}

    form = PickAddressForm()

    if form.validate_on_submit():
        printObj.set_chosenAddress(form.whichAddress.data)
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
