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

units = ['(15 ounce) can', '(10 inch)', '(12 ounce) jar', '(3 ounce) package', '(2 pound)',
		 'pints',  'pint', 'cups', 'cup', 'tablespoons', 'tablespoon', 'teaspoons', 'teaspoon',
		 'ounces', 'ounce', 'cloves', 'clove', 'pounts', 'pound', 'dashes', 'dash']

NumTables = "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = '[database name]' AND table_name = '[table name]'"


def scrapePage(addr):
	source = addr[:[m.start() for m in re.finditer(r"/", addr)][2]]

	if source == 'http://allrecipes.com':
		page = requests.get(addr)
		tree = html.fromstring(page.content)
		sourceName = 'Allrecipes'
		sourceType = "url"
		author = '//span[@class="submitter__name"]/text()')
		ingredients = tree.xpath(
			'//span[@class="recipe-ingred_txt added"]/text()')
		directions = tree.xpath(
			'//span[@class="recipe-directions__list--item"]/text()')
		serveSize = tree.xpath('//p[@class="subtext"]/text()')
		recipeName = tree.xpath('//h1[@class="recipe-summary__h1"]/text()')
		cookTime = tree.xpath('//span[@class="ready-in-time"]/text()')
		calorieCount = tree.xpath(
			'//span[@class="calorie-count"]//span/text()')
		recipeType = tree.xpath('//span[@class="toggle-similar__title"]/text()')

		ingredientCount = []
		ingredientUnit = []
		ingredientItem = []
		rescrapePageder = 0
		for ing in ingredients:
			ing = ''.join(filter(lambda x: x in string.printable, ing))
			ingredientCount.append(ing[:[m.start()
										 for m in re.finditer(r" ", ing)][0]])
			remainder = [m.start() for m in re.finditer(r" ", ing)][0]
			step = len(ingredientUnit)
			for u in units:
				if ing.find(u) >= 0:
					ingredientUnit.append(u)
					remainder = ing.index(u) + len(u)
					break
			if len(ingredientUnit) == step:
				ingredientUnit.append('_')
			ingredientItem.append(ing[remainder + 1:])

		print(source)
		print('%s' % recipeName[0])
		print('%s' % serveSize[0])
		print('CookTime: %s' % cookTime[0])
		print('CalorieCount: %s' % calorieCount[0])

		print('\nIngredients:')
		for i in range(len(ingredients)):
			#print(''.join(filter(lambda x: x in string.printable, ingredients[i])))
			print(ingredientCount[i], ingredientUnit[i], ingredientItem[i])

		print('\nDirections:')
		for i in range(len(directions)):
			print('%s:' % str(i + 1), directions[i])
	else:
		print('%s is not yet implemented...' % source)
	pageInfo = []
	recipeInfo = [recipeName, serveSize, recipeType]
	pageInfo.append(recipeInfo)
	sourceInfo = [sourceName, source, sourceType, author]
	pageInfo.append(sourceInfo)
	dircInfo = [directions, cookTime] 
	pageInfo.append(dircInfo)
	ingInfo = []
	pageInfo.append(ingInfo)

	return pageInfo


def insertInfo(cnx, pageInfo):
	recipeNum = cursor.lastrowid
	addRecipe = ("INSERT INTO RECIPE "
               "(Recipe_No, Name, Quantity, Type, Direciton_No, Source_No) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
	recipeInfo = pageInfo[0]
	recipe = {'Recipe_No': recipeNum, 'Name': recipeInfo[0], 'Quantity': recipeInfo[1], 'Type': recipeInfo[2], 'Direction_No': recipeNum, 'Source_No': recipeNum }
	cnx.execute(addRecipe, recipe)

	addSource = ("INSERT INTO SOURCE "
               "(Source_No, Name, Reference, Type, Author) "
               "VALUES (%s, %s, %s, %s, %s)")
	sourceInfo = pageInfo[1]
	source = {'Source_No': recipeNum, 'Name': sourceInfo[0], 'Reference': sourceInfo[1], 'Type': sourceInfo[2], 'Author': sourceInfo[3]}
	cnx.execute(addSource, source)

	addInstructions = ("INSERT INTO INSTRUCTION_LIST "
               "(Direction_No, Description, Prep_Time, Difficulty) "
               "VALUES (%s, %s, %s, %s)")
	dircInfo = pageInfo[2]
	directions = {'Direction_No': recipeNum, 'Description': str(dircInfo[0]), 'Prep_Time': dircInfo[1], 'Difficulty': null}
	cxn.execute(addInstructions, dirctions)

	addIngredients = = ("INSERT INTO INGREDIENT "
               "(Ingredient_No, Name, Type, Description, Contains_Dairy, Contains_Glutten) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
	ingInfo = pageInfo[3]
	instructions = {'Ingredient_No':, 'Name':, 'Type':, 'Description':, 'Contains_Dairy':, 'Contains_Glutten':} 
	cxn.execute(addIngredients, ingrdients)

	addAmounts = ("INSERT INTO AMOUNT_REQUIRED "
               "(Recipe_No, Ingredient_No, Amount, Unit) "
               "VALUES (%s, %s, %s, %s)")
	amountInfo = pageInfo[3]
	amounts = {'Recipe_No':, 'Ingredient_No':, 'Amount':, 'Unit':} 
	cxn.execute(addAmounts, amounts)

	addIngredients = = ("INSERT INTO INGREDIENT "
               "(Ingredient_No, Name, Type, Description, Contains_Dairy, Contains_Glutten) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
	ingInfo = pageInfo[3]
	instructions = {'Ingredient_No':, 'Name':, 'Type':, 'Description':, 'Contains_Dairy':, 'Contains_Glutten':} 
	cxn.execute(addIngredients, ingrdients)





def RunQuery(cnx, query):
	cursor = cnx.cursor()
	cursor.execute(query)
	result = ['%s' % x for x in cursor]
	cursor.close()
	return result


def main():
	cnx = mysql.connector.connect()
	try:
		cnx = mysql.connector.connect(user='root',
									  password='<replace>',
									  host='localhost',
									  database='Recipes')
	except:
		print('Can\'t connect to MySQL server...\n')

	if int(RunQuery(cnx, NumTables)[0]) == 0:
		print('Need to setup schema')

	pageInfo = scrapePage('http://allrecipes.com/recipe/8691/chicken-enchiladas-i/')
	insertInfo(cns, pageInfo);
	# print('\n/-----/\n')
	# scrapePage('http://allrecipes.com/recipe/213742/meatball-nirvana/')
	# print('\n/-----/\n')
	# scrapePage('http://allrecipes.com/recipe/219046/rich-and-creamy-beef-stroganoff/')

	cnx.close()

if __name__ == '__main__':
	main()
