from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField

#CHAKRA_CHOICES = [('1','--Chakra--'),('2','Crown'),('3','Third eye'),('4','Throat'),('5','Heart'),('6','Solar plexus'),('7','Sacral'),('8','Root')]
#BIRTH_MONTH_CHOICES = [('1','--Birth Month--'),('2','January'),('3','February'),('4','March'),('5','April'),('6','May'),('7','June'),('8','July'),('9','August'),('10','September'),('11','October'),('12','November'),('13','December')]
#ZODIAC_CHOICES = [('1','--Zodiac Sign--'),('2','Aires'),('3','Taurus'),('4','Gemini'),('5','Cancer'),('6','Leo'),('7','Virgo'),('8','Libra'),('9','Scorpio'),('10','Sagitarius'),('11','Capricorn'),('12','Aquarius'),('13','Pisces')]

# create a search form
#
# variable names need to be identical to what they are in each html template file
class SearchForm(FlaskForm):
	search_image = FileField("Search by Image")
	chakra_select = SelectField("Chakra select")
#	chakra_select = SelectField("Chakra select", choices=CHAKRA_CHOICES)
	birth_month_select = SelectField("Birth Month select")
#	birth_month_select = SelectField("Birth Month select", choices=BIRTH_MONTH_CHOICES)
	zodiac_select = SelectField("Zodiac select")
#	zodiac_select = SelectField("Zodiac select", choices=ZODIAC_CHOICES)
	submit = SubmitField("Submit")
