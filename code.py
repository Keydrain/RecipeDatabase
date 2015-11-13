#/usr/local/bin/python3

from lxml import html
import requests

units = ['pint', 'cup', 'tablespoon', 'teaspoon', 'ounce', 'clove']

def main(addr):
	page = requests.get(addr)
	tree = html.fromstring(page.content)

	ingredients = tree.xpath('//span[@class="recipe-ingred_txt added"]/text()')
	directions = tree.xpath('//span[@class="recipe-directions__list--item"]/text()')
	serveSize = tree.xpath('//p[@class="subtext"]/text()')
	recipeName = tree.xpath('//h1[@class="recipe-summary__h1"]/text()')
	cookTime = tree.xpath('//span[@class="ready-in-time"]/text()')
	calorieCount = tree.xpath('//span[@class="calorie-count"]//span/text()')

	print('%s' % recipeName[0])
	print('%s' % serveSize[0])
	print('CookTime: %s' % cookTime[0])
	print('CalorieCount: %s' % calorieCount[0])

	print('\nIngredients:')
	for i in ingredients:
		print(i)

	print('\nDirections:')
	for i in range(len(directions)):
		print(i+1, directions[i])

if __name__ == '__main__':
	#main(sys.argv[1])
	main('http://allrecipes.com/recipe/8691/chicken-enchiladas-i/')
