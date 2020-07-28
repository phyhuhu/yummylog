import requests
from bs4 import BeautifulSoup
from lxml import html
import json

class get_nutritions():

    def cal_nutritions(self):

        nutritions={}

        for letter in 'abcdefghijklmnopqrstuvwxyz*':
            print(letter)
            page=0
            URL = f'https://www.fatsecret.com/Default.aspx?pa=toc&pg={page}&f={letter}&s=2'

            get_html = requests.get(URL).content
            soup = BeautifulSoup(get_html, 'lxml')
            div = soup.find_all('div', class_="searchResultSummary")
            num = div[0].text.split(' ')

            page_num=0
            if int(num[3])!=0:
                temp=int(num[5])/int(num[3])
                page_num = int(temp) if temp-int(temp)==0 else int(temp)+1
                
            all_a={}
            for page in range(page_num):
                print(letter,page)
                URL = f'https://www.fatsecret.com/Default.aspx?pa=toc&pg={page}&f={letter}&s=2'

                get_html = requests.get(URL).content
                soup = BeautifulSoup(get_html, 'lxml')

                for a in soup.find_all('a'):
                    if a.get('href')[:25]=='/calories-nutrition/usda/':
                        all_a[a.get('title')]='https://www.fatsecret.com'+a.get('href')

            temp_nutritions={}
            for item in all_a:
                print(letter,item)
                temp_dict={}
                get_html=requests.get(all_a[item]).content
                soup=BeautifulSoup(get_html, 'lxml')

                td=soup.find_all("td", class_="serving_size black us serving_size_value")
                temp_dict['Weight']=td[0].text

                div_energy=soup.find_all("div", class_="hero_value black right")
                temp_dict['Calories']=div_energy[0].text

                # Total Fat = Saturated Fat + Trans Fat + Polyunsaturated Fat + Monounsaturated Fat
                # Total Carbohydrate = Dietary Fiber + Sugars
                nutritions_name=['Total Fat', 'Saturated Fat', 'Trans Fat', 'Polyunsaturated Fat', 'Monounsaturated Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Sugars', 'Protein', 'Vitamin D', 'Calcium', 'Iron', 'Potassium', 'Vitamin A', 'Vitamin C']
                div=soup.find_all("div", class_="nutrient value left")
                for i in range(len(div)):
                    if div[i].text!='-':
                        temp_dict[nutritions_name[i]]=div[i].text
                    else:
                        temp_dict[nutritions_name[i]]='0g'

                temp_nutritions[item]=temp_dict

            nutritions[letter]=temp_nutritions

        return nutritions


# nutritions=get_nutritions().cal_nutritions()

# with open('data.json', 'w') as fp:
#     json.dump(nutritions, fp)

# with open('data.json', 'r') as fp:
#     nutritions = json.load(fp)