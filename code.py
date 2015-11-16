#/usr/local/bin/python3

"""
Author: 	Clint Cooper, Emily Rohrbough
Date:   	11/14/15
CSCI 440:	Recipe Database

Description...
"""

from lxml import html
import requests
import re
import string
import mysql.connector
import sys

units = ['(15 ounce) can', '(10 inch)', '(12 ounce) jar', '(3 ounce) package', '(2 pound)',
		 'pints',  'pint', 'cups', 'cup', 'tablespoons', 'tablespoon', 'teaspoons', 'teaspoon',
		 'ounces', 'ounce', 'cloves', 'clove', 'pounts', 'pound', 'dashes', 'dash']

NumTables = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'Recipes'"
TableNames = "SELECT TABLE_NAME FROM information_schema.tables WHERE table_schema = 'Recipes'"
NextRecipeNum = "SELECT IFNULL(MAX(Recipe_No),-1) FROM `RECIPE`"
NextIngredientNum = "SELECT IFNULL(MAX(Ingredient_No),-1) FROM `INGREDIENT`"
NextSourceNum = "SELECT IFNULL(MAX(Source_No),-1) FROM `SOURCE`"
NextNutritionNum = "SELECT IFNULL(MAX(Nutrition_No),-1) FROM `NUTRITIONAL_FACTS`"
ForeignKeysOff = "SET FOREIGN_KEY_CHECKS = 0"
ForeignKeysOn = "SET FOREIGN_KEY_CHECKS = 1"
TruncateTable = "TRUNCATE TABLE %s"
DropTable = "DROP TABLE %s"

def resetTables(cnx):
	tables = RunQuery(cnx, TableNames)
	RunQuery(cnx, ForeignKeysOff)
	for x in tables:
		RunQuery(cnx, TruncateTable % x)
	RunQuery(cnx, ForeignKeysOn)

def resetDatabase(cnx):
	tables = RunQuery(cnx, TableNames)
	RunQuery(cnx, ForeignKeysOff)
	for x in tables:
		RunQuery(cnx, DropTable % x)
	RunQuery(cnx, ForeignKeysOn)

def scrapeGoogle(ing):
	ing = re.sub("'", '', ing)
	ing = re.sub(", or to taste", '', ing)
	try:
		page = requests.get('http://www.google.com/search?q=%s+nutrition' % ing)
		tree = html.fromstring(page.content)
		#ingType = tree.xpath('//div[@class="kno-fb-ctx"]//span/text()')
		ingType = tree.xpath('//div[@class="_zdb _Pxg"]/text()')
		if ingType == []:
			ingType = ['-']
		print(ingType)
		#ingDescription = tree.xpath('//div[@class="kno-rdesc"]//span/text()')
		ingDescription = [' '.join((tree.xpath('//div[@class="_tXc"]//span/text()')[0]).split('\n'))]
		print(ingDescription)
		#ingAmount = tree.xpath('//div[@class="_Fih"]//select[@class="_sTf kno-nf-ss"]/@title')
		ingAmount = tree.xpath('//div[@class="_f6d"]/text()')
		print(ingAmount)
		#ingCalories = tree.xpath('//tr[@class="kno-fb-ctx kno-nf-cq"]//td//span[@class="abs"]/text()')
		ingCalories = [tree.xpath('//table[@class="_Y5d"]//tr//td/text()')[0]]
		print(ingCalories)
		#ingFat = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/04k8n"]//td[@class="ellip"]//span[@class="abs"]/text()')
		ingFat = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[1]]
		print(ingFat)
		#ingCholesterol = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/01w_3"]//td[@class="ellip"]//span[@class="abs"]/txt()')
		ingCholesterol = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[3]]
		print(ingCholesterol)
		#ingSodium = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/025sf0_"]//td[@class="ellip"]//span[@class="abs"]/text()')
		ingSodium = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[5]]
		print(ingSodium)
		#ingPotassium = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/025s7j4"]//td[@class="ellip"]//span[@class="abs"]/text()')
		ingPotassium = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[7]]
		print(ingPotassium)
		#ingCarbohydrate = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/01sh2"]//td[@class="ellip"]//span[@class="abs"]/text()')
		ingCarbohydrate = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[9]]
		print(ingCarbohydrate)
		#ingProtein = tree.xpath('//table[@class="_yX"]//tbody//tr[@data-mid="/m/05wvs"]//td[@class="ellip"]//span[@class="abs"]/text()')
		ingProtein = [tree.xpath('//table[@class="_Y5d"]//tr//td[@class="_b6d"]//span/text()')[1]]
		print(ingProtein)
		#ingVitamins = tree.xpath('//table[@class="_yX _RXc"]//tbody//tr//td[@class="ellip"]//text()')
		ingVitamins = tree.xpath('//table[@class="_Y5d"]//tr//td/text()')[20:]
		i = 0
		while i < len(ingVitamins)-1: 
			if ingVitamins[i+1] == '0%':
				del ingVitamins[i]
				del ingVitamins[i]
			i += 1
		ingVitamins = [x for x in ingVitamins if x.find('%') == -1]
		results = [ing, ingType, ingDescription, ingAmount, ingCalories, ingFat, ingCholesterol, ingSodium, ingPotassium, ingCarbohydrate, ingProtein, ingVitamins]
		print(results)
		return results
	except:
		return [ing]

def scrapeRecipe(addr):
	source = addr[:[m.start() for m in re.finditer(r"/", addr)][2]]

	if source == 'http://allrecipes.com':
		page = requests.get(addr)
		tree = html.fromstring(page.content)
		#print(page.content)
		sourceName = 'Allrecipes'
		sourceType = "url"
		author = tree.xpath('//span[@class="submitter__name"]/text()')
		ingredients = tree.xpath('//span[@class="recipe-ingred_txt added"]/text()')
		directions = tree.xpath('//span[@class="recipe-directions__list--item"]/text()')
		serveSize = [''.join([x for x in tree.xpath('//p[@class="subtext"]/text()')[0] if x.isdigit()])]
		recipeName = tree.xpath('//h1[@class="recipe-summary__h1"]/text()')
		cookTime = tree.xpath('//span[@class="ready-in-time"]/text()')
		calorieCount = tree.xpath('//span[@class="calorie-count"]//span/text()')
		recipeType = [''.join(tree.xpath('//ul[@class="breadcrumbs breadcrumbs"]//li//a//span[@class="toggle-similar__title"]/text()')[-1].split())]
		recipeDescription = str(tree.xpath('//div[@class="submitter__description"]/text()')[0])
		recipeDescription = [recipeDescription[recipeDescription.index('"')+1:recipeDescription.rindex('"')]]

		ingredientCount = []
		ingredientUnit = []
		ingredientItem = []
		rescrapePageder = 0
		for ing in ingredients:
			ing = ''.join(filter(lambda x: x in string.printable, ing))
			ingredientCount.append(ing[:[m.start() for m in re.finditer(r" ", ing)][0]])
			remainder = [m.start() for m in re.finditer(r" ", ing)][0]
			step = len(ingredientUnit)
			for u in units:
				if ing.find(u) >= 0:
					ingredientUnit.append(u)
					remainder = ing.index(u) + len(u)
					break
			if len(ingredientUnit) == step:
				ingredientUnit.append("UNKNOWN")
			ingredientItem.append(ing[remainder + 1:])

			# At this point we have source, recipeName[0], serveSize[0], cookTime[0], calorieCount[0],
			# ingredientCount[-], ingredientUnit[-], ingredientItem[-], directions[-]

			# May need to flatten Directions with '\n'.join(['%d: %s\n' % i, Directions[i] for i in range(len(Directions)))

		print(source)
		print('%s' % recipeName[0])
		print('%s' % author[0])
		print('%s' % serveSize[0])
		print('%s' % recipeType[0])
		print('%s' % recipeDescription[0])
		print('CookTime: %s' % cookTime[0])
		print('CalorieCount: %s' % calorieCount[0])

		print('\nIngredients:')
		ingredientDetials = []
		for i in range(len(ingredients)):
			#print(''.join(filter(lambda x: x in string.printable, ingredients[i])))
			print(ingredientCount[i], ingredientUnit[i], ingredientItem[i])
			ingredientDetials.append(scrapeGoogle(ingredientItem[i]))
			print()

		print('\nDirections:')
		#for i in range(len(directions)):
		#	print('%s:' % str(i + 1), directions[i])
		directions = ('\n'.join(['%d: %s\n' % (i+1, directions[i]) for i in range(len(directions))]))
		print(directions)

		pageInfo = []
		recipeInfo = [recipeName[0], recipeDescription[0], serveSize[0], recipeType[0]]
		pageInfo.append(recipeInfo)
		sourceInfo = [sourceName, source, sourceType, author[0]]
		pageInfo.append(sourceInfo)
		amountInfo = [ingredientCount, ingredientUnit]
		pageInfo.append(amountInfo)
		ingInfo = [ingredientDetials]
		pageInfo.append(ingInfo)
		dircInfo = [directions, cookTime] 
		pageInfo.append(dircInfo)

		return pageInfo
	else:
		print('%s is not yet implemented...' % source)


def insertInfo(cnx, pageInfo):
	recipeNum = RunQuery(cnx, NextRecipeNum)[0][0]+1
	sourceNum = RunQuery(cnx, NextSourceNum)[0][0]+1

	addRecipe = "INSERT INTO RECIPE (Recipe_No, Name, Description, Quantity, Type, Direction_No, Source_No) VALUES (%d, '%s', '%s', %s, '%s', %d, %d)"
	addSource = "INSERT INTO SOURCE (Source_No, Name, Reference, Type, Author) VALUES (%d, '%s', '%s', '%s', '%s')"
	addIngredient = "INSERT INTO INGREDIENT (Ingredient_No, Name, Type, Description, Contains_Dairy, Contains_Glutten, Nutrition_No) VALUES (%s, '%s', '%s', '%s', %s, %s, %s)"
	addAmount = "INSERT INTO AMOUNT_REQUIRED (Recipe_No, Ingredient_No, Amount, Unit) VALUES (%s, %s, %s, '%s')"
	addNutrition = "INSERT INTO NUTRITIONAL_FACTS (Nutrition_No, Units, Calories, Protien, Sugar, Sodium, Fat) VALUES (%s, '%s', '%s', '%s', '%s', '%s', '%s')"
	addDirection = "INSERT INTO INSTRUCTION_LIST (Direction_No, Directions, Prep_Time, Difficulty) VALUES (%s, '%s', '%s', %s)"
	addVitamin = "INSERT INTO VITAMIN (Nutrition_No, Vitamin) VALUES (%s, '%s')"

	recipeInfo = pageInfo[0]
	sourceInfo = pageInfo[1]
	amountInfo = pageInfo[2]
	ingredInfo = pageInfo[3][0]
	directInfo = pageInfo[4]

	# Source Entry
	source = (sourceNum, sourceInfo[0], sourceInfo[1], sourceInfo[2], sourceInfo[3])
	RunQuery(cnx, addSource % source)

	# Ingredient and Amount Entries
	for i in range(len(amountInfo[0])):
		ingredientNum = RunQuery(cnx, NextIngredientNum)[0][0]+1
		
		amounts = (recipeNum, ingredientNum, amountInfo[0][i], amountInfo[1][i]) 
		RunQuery(cnx, addAmount % amounts)

		nutritionNum = RunQuery(cnx, NextNutritionNum)[0][0]+1
		#print(len(ingredInfo[i]), ingredInfo[i])

		if len(ingredInfo[i]) > 1:
			ingredient = (ingredientNum, ingredInfo[i][0], ingredInfo[i][1][0], ingredInfo[i][2][0], 0, 1 if ingredInfo[i][9] != 0 else 0, nutritionNum)
			nutrition = (nutritionNum, ingredInfo[i][3][0], ingredInfo[i][4][0], ingredInfo[i][10][0], ingredInfo[i][9][0], ingredInfo[i][7][0], ingredInfo[i][5][0])
		else:
			ingredient = (ingredientNum, ingredInfo[i][0], '-', '-', 0, 0, ingredientNum)
			nutrition = (nutritionNum, '-', 0, 0, 0, 0, 0)
		RunQuery(cnx, addNutrition % nutrition)
		RunQuery(cnx, addIngredient % ingredient)
		if len(ingredInfo[i]) > 1:
			#Vitamins
			for x in ingredInfo[i][-1]:
				vitamin = (nutritionNum, x)
				RunQuery(cnx, addVitamin % vitamin)

	direction = (recipeNum, directInfo[0], directInfo[1][0], 0)
	RunQuery(cnx, addDirection % direction)

	recipe = (recipeNum, recipeInfo[0], recipeInfo[1], recipeInfo[2], recipeInfo[3], recipeNum, sourceNum)
	RunQuery(cnx, addRecipe % recipe)

def RunQuery(cnx, query):
	print('\nRun: %s' % query)
	cursor = cnx.cursor()
	cursor.execute(query)
	result = [x for x in cursor]
	if result == []:
		cnx.commit()
	cursor.close()
	return result


def RunSQLFile(cnx, filename):
	cursor = cnx.cursor()

	f = open(filename, 'r')
	sqlFile = f.read()
	f.close()

	for query in [x for x in sqlFile.split(';') if x != '\n']:
		try:
			cursor.execute(query)
		except:
			print("\nCommand skipped: %s" % query, '\n')
			print("Error: ", sys.exc_info())

	cursor.close()


def main():
	cnx = mysql.connector.connect()
	try:
		cnx = mysql.connector.connect(user='root', password='umbranium', host='localhost', database='Recipes')
	except:
		print('Can\'t connect to MySQL server...\n')

	resetDatabase(cnx)
	if RunQuery(cnx, NumTables)[0][0] == 0:
		print("Run: Create tables from SchemaSetup.")
		RunSQLFile(cnx, 'SchemaSetup.sql')
	else:
		print('Tables already built.')
		resetTables(cnx)
	print()

	pageInfo = scrapeRecipe('http://allrecipes.com/recipe/8691/chicken-enchiladas-i/')
	insertInfo(cnx, pageInfo)
	pageInfo = scrapeRecipe('http://allrecipes.com/recipe/213742/meatball-nirvana/')
	insertInfo(cnx, pageInfo)
	# print('\n/-----/\n')
	# scrapeRecipe('http://allrecipes.com/recipe/219046/rich-and-creamy-beef-stroganoff/')

	try: cnx.close()
	except: None

if __name__ == '__main__':
	main()
