from selenium.webdriver import Chrome


class Coronavirus():
	def __init__(self):
		self.driver = Chrome()
		self.driver.get('https://www.worldometers.info/coronavirus/')
		
		table = self.driver.find_element_by_xpath('//*[@id="main_table_countries"]/tbody[1]')
		country_element = table.find_element_by_xpath("//td[contains(text(), 'China')]")
		
