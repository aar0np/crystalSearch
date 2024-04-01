from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField

# create a search form
#
# variable names need to be identical to what they are in each html template file
class SearchForm(FlaskForm):
	search_image = FileField("Search by Image")
	chakra_select = SelectField("Chakra select")
	birth_month_select = SelectField("Birth Month select")
	zodiac_select = SelectField("Zodiac select")
	submit = SubmitField("Submit")
