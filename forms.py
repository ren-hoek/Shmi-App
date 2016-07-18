from flask.ext.wtf import Form
from wtforms.fields import TextField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Required

class TrustForm(Form):
    hosp_drop = SelectField("Select Trust")
    submit = SubmitField("Go")

class DiagForm(Form):
    diag_drop = SelectField("Select diagnosis")
    submit = SubmitField("Go")
