from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
import csv

class PickAddressForm(FlaskForm):
    addressChoices = []
    with open('addressData.csv', newline='') as dataFile:
        fileReader = csv.reader(dataFile, dialect="excel")
        addressChoices.append("PRESS HERE TO CHOOSE")
        for row in fileReader:
            addressChoices.append(' | '.join(row))

    whichAddress = SelectField("Choose ->", choices=addressChoices)
    submit = SubmitField("CONTINUE")

class EnterLineForm(FlaskForm):
    inputLine = StringField()
    submit = SubmitField("CONTINUE")

class PrintButtonForm(FlaskForm):
    submit = SubmitField("PRINT")
    cancel = SubmitField("START OVER")
