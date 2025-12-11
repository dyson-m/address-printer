from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField
from wtforms.validators import DataRequired
import csv

class PickAddressForm(FlaskForm):

    whichAddress = SelectField("Choose ->", choices=[])
    """Pick address from dropdown"""
    
    def refreshAddresses(self):
        addressChoices = []
        with open('addressData.csv', newline='') as dataFile:
            fileReader = csv.reader(dataFile, dialect="excel")
            addressChoices.append("PRESS HERE TO CHOOSE")
                # Default/first option that functions as "no selection"
            for row in fileReader:
                addressChoices.append(' | '.join(row))
        self.whichAddress.choices = addressChoices

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.refreshAddresses()

    submit = SubmitField("CONTINUE")
    """Continue to step 2 in regular printing"""
    
    edit = SubmitField("EDIT SELECTED ADDRESS")
    """Edit the currently selected address"""

    new = SubmitField("ADD NEW ADDRESS")
    """Add a new address to the csv"""

    # bulk = SubmitField("PRINT MULTIPLE ADDRESSES")
    # """Select and print multiple addresses at once"""

class EnterLineForm(FlaskForm):
    inputLine = StringField()
    submit = SubmitField("CONTINUE")

class PrintButtonForm(FlaskForm):
    submit = SubmitField("PRINT")
    cancel = SubmitField("CANCEL")

class EditAddressForm(FlaskForm):
    line0 = StringField("line0")
    line1 = StringField("line1")
    line2 = StringField("line2")
    submit = SubmitField("SAVE")
    cancel = SubmitField("CANCEL")
    delete = SubmitField("DELETE")