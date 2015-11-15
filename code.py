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

def scrapePage(addr):
	source = addr[:[m.start() for m in re.finditer(r"/",addr)][2]]

	if source == 'http://allrecipes.com':
		page = requests.get(addr)
		tree = html.fromstring(page.content)

		ingredients = tree.xpath('//span[@class="recipe-ingred_txt added"]/text()')
		directions = tree.xpath('//span[@class="recipe-directions__list--item"]/text()')
		serveSize = tree.xpath('//p[@class="subtext"]/text()')
		recipeName = tree.xpath('//h1[@class="recipe-summary__h1"]/text()')
		cookTime = tree.xpath('//span[@class="ready-in-time"]/text()')
		calorieCount = tree.xpath('//span[@class="calorie-count"]//span/text()')

		ingredientCount = []
		ingredientUnit = []
		ingredientItem = []
		rescrapePageder = 0
		for ing in ingredients:
			ing = ''.join(filter(lambda x: x in string.printable, ing))
			ingredientCount.append(ing[:[m.start() for m in re.finditer(r" ",ing)][0]])
			remainder = [m.start() for m in re.finditer(r" ",ing)][0]
			step = len(ingredientUnit)
			for u in units:
				if ing.find(u) >= 0:
					ingredientUnit.append(u)
					remainder = ing.index(u) + len(u)
					break;
			if len(ingredientUnit) == step:
				ingredientUnit.append('_')
			ingredientItem.append(ing[remainder+1:])

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
			print('%s:' % str(i+1), directions[i])
	else:
		print('%s is not yet implemented...' % source)

def main():
	try:
		cnx = mysql.connector.connect(user='root', 
									  password='<replace_when_running>',
		                              host='localhost',
		                              database='Recipe')
	except:
		print('It didn\'t work...')

	scrapePage('http://allrecipes.com/recipe/8691/chicken-enchiladas-i/')
	print('\n/-----/\n')
	scrapePage('http://allrecipes.com/recipe/213742/meatball-nirvana/')
	print('\n/-----/\n')
	scrapePage('http://allrecipes.com/recipe/219046/rich-and-creamy-beef-stroganoff/')

if __name__ == '__main__':
	main()
