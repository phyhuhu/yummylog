import requests, json, os

# get table of nutritions for all ingredients
# nutrition data from https://www.fatsecret.com/
with open('static/data/data.json', 'r') as fp:
    nutritions = json.load(fp)

class calculate_nutritions():

    def __init__(self, ingredient, quantity):
        self.ingredient=ingredient
        self.quantity=quantity

    def find(self):
        # initial dictionary of nutritions
        ingredient_nutritions={'Calories':0, 'Total Fat':0, 'Total Carbohydrate': 0, 'Protein':0}

        # list unit of weight and unit transformation
        weight_unit={'g', 'kg', 'oz', 'lb', 'lbs'}
        weight_unit_trans={'g':1.0, 'kg':1000.0, 'oz':28.3495,  'lb':453.592, 'lbs':453.592}

        # list unit of volume and unit transformation
        volume_unit={'cup', 'tbs', 'tbsp', 'tsp', 'fl oz', 'l', 'ml'}
        volume_unit_trans={'cup':1.0, 'tbs':0.0625, 'tbsp':0.0625,  'tsp':0.0208333, 'fl oz':0.125, 'l':4.22675, 'ml':0.00422675}

        # for 'Egg', 'Milk', 'Butter', 'Bacon', 'Galic'
        if self.ingredient=='Egg' or self.ingredient=='Eggs':
            q_ingredient=self.quantity.replace(' ','')
            check_number=False
            for i in q_ingredient:
                if i.isdigit():
                    check_number=True
            if not check_number:
                return {}

            test_weight_ingredient=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i

            test_volume_ingredient=''
            for i in volume_unit:
                if i in q_ingredient:
                    test_volume_ingredient='volume'
                    unit_volume_ingredient=i
            
            if test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                value_ingredient=weight_ingredient*unit
                transfer_unit=1.0/243.0

            elif test_volume_ingredient!='':

                unit=volume_unit_trans[unit_volume_ingredient]
                volume_ingredient=self.get_value(q_ingredient, unit_volume_ingredient)
                value_ingredient=volume_ingredient*unit
                transfer_unit=1.0

            else:

                if '/' not in q_ingredient:
                    value=''
                    for i in q_ingredient:
                        if i.isdigit():
                            value+=str(i)
                        else:
                            break
                    if value!='':
                        value_ingredient=float(value)
                    else:
                        return {}
                else:
                    position_divide=q_ingredient.find('/')
                    numerator=''
                    for i in q_ingredient:
                        if i.isdigit():
                            numerator+=str(i)
                        else:
                            break
                    denominator=''
                    for i in q_ingredient[position_divide+1:]:
                        if i.isdigit():
                            denominator+=str(i)
                        else:
                            break
                    value_ingredient=float(numerator)/float(denominator)
                transfer_unit=1.0/4.86

            ingredient_nutritions['Calories']=348*value_ingredient*transfer_unit
            ingredient_nutritions['Total Fat']=23*value_ingredient*transfer_unit
            ingredient_nutritions['Total Carbohydrate']=1.7*value_ingredient*transfer_unit
            ingredient_nutritions['Protein']=31*value_ingredient*transfer_unit

            return ingredient_nutritions

        elif self.ingredient=='Egg White':
            q_ingredient=self.quantity.replace(' ','')
            check_number=False
            for i in q_ingredient:
                if i.isdigit():
                    check_number=True
            if not check_number:
                return {}

            test_weight_ingredient=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i

            test_volume_ingredient=''
            for i in volume_unit:
                if i in q_ingredient:
                    test_volume_ingredient='volume'
                    unit_volume_ingredient=i
            
            if test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                value_ingredient=weight_ingredient*unit
                transfer_unit=1.0/243.0

            elif test_volume_ingredient!='':

                unit=volume_unit_trans[unit_volume_ingredient]
                volume_ingredient=self.get_value(q_ingredient, unit_volume_ingredient)
                value_ingredient=volume_ingredient*unit
                transfer_unit=1.0

            else:

                if '/' not in q_ingredient:
                    value=''
                    for i in q_ingredient:
                        if i.isdigit():
                            value+=str(i)
                        else:
                            break
                    if value!='':
                        value_ingredient=float(value)
                    else:
                        return {}
                else:
                    position_divide=q_ingredient.find('/')
                    numerator=''
                    for i in q_ingredient:
                        if i.isdigit():
                            numerator+=str(i)
                        else:
                            break
                    denominator=''
                    for i in q_ingredient[position_divide+1:]:
                        if i.isdigit():
                            denominator+=str(i)
                        else:
                            break
                    value_ingredient=float(numerator)/float(denominator)
                transfer_unit=33.0/243.0

            ingredient_nutritions['Calories']=125*value_ingredient*transfer_unit
            ingredient_nutritions['Total Fat']=0.4*value_ingredient*transfer_unit
            ingredient_nutritions['Total Carbohydrate']=1.8*value_ingredient*transfer_unit
            ingredient_nutritions['Protein']=26*value_ingredient*transfer_unit

            return ingredient_nutritions

        elif self.ingredient=='Egg Yolk' or self.ingredient=='Egg Yolks':
            q_ingredient=self.quantity.replace(' ','')
            check_number=False
            for i in q_ingredient:
                if i.isdigit():
                    check_number=True
            if not check_number:
                return {}

            test_weight_ingredient=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i

            test_volume_ingredient=''
            for i in volume_unit:
                if i in q_ingredient:
                    test_volume_ingredient='volume'
                    unit_volume_ingredient=i
            
            if test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                value_ingredient=weight_ingredient*unit
                transfer_unit=1.0/243.0

            elif test_volume_ingredient!='':

                unit=volume_unit_trans[unit_volume_ingredient]
                volume_ingredient=self.get_value(q_ingredient, unit_volume_ingredient)
                value_ingredient=volume_ingredient*unit
                transfer_unit=1.0

            else:

                if '/' not in q_ingredient:
                    value=''
                    for i in q_ingredient:
                        if i.isdigit():
                            value+=str(i)
                        else:
                            break
                    if value!='':
                        value_ingredient=float(value)
                    else:
                        return {}
                else:
                    position_divide=q_ingredient.find('/')
                    numerator=''
                    for i in q_ingredient:
                        if i.isdigit():
                            numerator+=str(i)
                        else:
                            break
                    denominator=''
                    for i in q_ingredient[position_divide+1:]:
                        if i.isdigit():
                            denominator+=str(i)
                        else:
                            break
                    value_ingredient=float(numerator)/float(denominator)
                transfer_unit=17.0/243.0

            ingredient_nutritions['Calories']=782*value_ingredient*transfer_unit
            ingredient_nutritions['Total Fat']=64*value_ingredient*transfer_unit
            ingredient_nutritions['Total Carbohydrate']=9*value_ingredient*transfer_unit
            ingredient_nutritions['Protein']=39*value_ingredient*transfer_unit

            return ingredient_nutritions

        elif self.ingredient=='Milk' or self.ingredient=='Whole Milk':
            ingredient_nutritions['Calories']=148
            ingredient_nutritions['Total Fat']=8
            ingredient_nutritions['Total Carbohydrate']=12
            ingredient_nutritions['Protein']=8
            return ingredient_nutritions

        elif self.ingredient=='Butter':
            q_ingredient=self.quantity.replace(' ','')
            check_number=False
            for i in q_ingredient:
                if i.isdigit():
                    check_number=True
            if not check_number:
                return {}

            test_weight_ingredient=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i

            test_volume_ingredient=''
            for i in volume_unit:
                if i in q_ingredient:
                    test_volume_ingredient='volume'
                    unit_volume_ingredient=i
            
            if test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                value_ingredient=weight_ingredient*unit
                transfer_unit=1.0/227.0

            elif test_volume_ingredient!='':

                unit=volume_unit_trans[unit_volume_ingredient]
                volume_ingredient=self.get_value(q_ingredient, unit_volume_ingredient)
                value_ingredient=volume_ingredient*unit
                transfer_unit=1.0

            else:

                if '/' not in q_ingredient:
                    value=''
                    for i in q_ingredient:
                        if i.isdigit():
                            value+=str(i)
                        else:
                            break
                    if value!='':
                        value_ingredient=float(value)
                    else:
                        return {}
                else:
                    position_divide=q_ingredient.find('/')
                    numerator=''
                    for i in q_ingredient:
                        if i.isdigit():
                            numerator+=str(i)
                        else:
                            break
                    denominator=''
                    for i in q_ingredient[position_divide+1:]:
                        if i.isdigit():
                            denominator+=str(i)
                        else:
                            break
                    value_ingredient=float(numerator)/float(denominator)
                transfer_unit=5.0/227.0

            ingredient_nutritions['Calories']=1627*value_ingredient*transfer_unit
            ingredient_nutritions['Total Fat']=184*value_ingredient*transfer_unit
            ingredient_nutritions['Total Carbohydrate']=0.1*value_ingredient*transfer_unit
            ingredient_nutritions['Protein']=1.9*value_ingredient*transfer_unit

            return ingredient_nutritions

        elif self.ingredient=='Bacon':
            q_ingredient=self.quantity.replace(' ','')
            check_number=False
            for i in q_ingredient:
                if i.isdigit():
                    check_number=True
            if not check_number:
                return {}

            test_weight_ingredient=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i
            
            if test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                value_ingredient=weight_ingredient*unit
                transfer_unit=1.0/100.0

            else:

                if '/' not in q_ingredient:
                    value=''
                    for i in q_ingredient:
                        if i.isdigit():
                            value+=str(i)
                        else:
                            break
                    if value!='':
                        value_ingredient=float(value)
                    else:
                        return {}
                else:
                    position_divide=q_ingredient.find('/')
                    numerator=''
                    for i in q_ingredient:
                        if i.isdigit():
                            numerator+=str(i)
                        else:
                            break
                    denominator=''
                    for i in q_ingredient[position_divide+1:]:
                        if i.isdigit():
                            denominator+=str(i)
                        else:
                            break
                    value_ingredient=float(numerator)/float(denominator)
                transfer_unit=8.0/100.0

            ingredient_nutritions['Calories']=541*value_ingredient*transfer_unit
            ingredient_nutritions['Total Fat']=42*value_ingredient*transfer_unit
            ingredient_nutritions['Total Carbohydrate']=1.4*value_ingredient*transfer_unit
            ingredient_nutritions['Protein']=37*value_ingredient*transfer_unit

            return ingredient_nutritions

        elif self.ingredient=='Garlic':
            return {}

        elif self.ingredient=='Onions':
            return {}

        # for other ingredients
        letter=self.ingredient[0].lower()

        search_item=self.ingredient
        if self.ingredient=='Beef':
            search_item=self.ingredient+' Round'

        # find match in database
        temp=set()
        for food in nutritions[letter]:
            food_reduce=food[:food.find('(')]
            if search_item in food_reduce:
                temp.add(food)
            
        food=''
        if len(temp)>0:
            size=float('inf')
            for i in temp:
                if i[len(search_item)]==' ':
                    if i.find('(')>0:
                        i_reduce=i[len(search_item)+1:]
                    else:
                        i_reduce=i[len(search_item)+1:i.find('(')]

                    if len(i_reduce)<size:
                        food=i
                        size=len(i_reduce)

        # calculate ingredient_nutritions
        if food!='':
            # find units for ingredient and corresponding one in database
            q_ingredient=self.quantity.replace(" ", "")
            q_nutrition=nutritions[letter][food]['Weight'].replace(" ", "")

            test_weight_ingredient=''
            test_weight_nutrition=''
            for i in weight_unit:
                if i in q_ingredient:
                    test_weight_ingredient='weight'
                    unit_weight_ingredient=i
                if i in q_nutrition:
                    test_weight_nutrition='weight'
                    unit_weight_nutrition=i

            test_volume_ingredient=''
            test_volume_nutrition=''
            for i in volume_unit:
                if i in q_ingredient:
                    test_volume_ingredient='volume'
                    unit_volume_ingredient=i
                if i in q_nutrition:
                    test_volume_nutrition='volume'
                    unit_volume_nutrition=i

            if test_weight_ingredient=='' and test_weight_nutrition=='' and test_volume_ingredient=='' and test_volume_nutrition=='':
                return {}

            if test_weight_ingredient == test_weight_nutrition and test_weight_ingredient!='':

                unit=weight_unit_trans[unit_weight_ingredient]
                weight_ingredient=self.get_value(q_ingredient, unit_weight_ingredient)
                if weight_ingredient==None:
                    return {}
                value_ingredient=weight_ingredient*unit

                unit=weight_unit_trans[unit_weight_nutrition]
                weight_nutrition=self.get_value(q_nutrition, unit_weight_nutrition)
                if weight_nutrition==None:
                    return {}
                value_nutrition=weight_nutrition*unit

                ingredient_nutritions['Calories']=float(nutritions[letter][food]['Calories'])*value_ingredient/value_nutrition
                ingredient_nutritions['Total Fat']=float(nutritions[letter][food]['Total Fat'][:-1])*value_ingredient/value_nutrition
                ingredient_nutritions['Total Carbohydrate']=float(nutritions[letter][food]['Total Carbohydrate'][:-1])*value_ingredient/value_nutrition
                ingredient_nutritions['Protein']=float(nutritions[letter][food]['Protein'][:-1])*value_ingredient/value_nutrition

                return ingredient_nutritions

            elif test_volume_ingredient == test_volume_nutrition and test_volume_ingredient!='':

                unit=volume_unit_trans[unit_volume_ingredient]
                volume_ingredient=self.get_value(q_ingredient, unit_volume_ingredient)
                if volume_ingredient==None:
                    return {}
                value_ingredient=volume_ingredient*unit
                
                unit=volume_unit_trans[unit_volume_nutrition]
                volume_nutrition=self.get_value(q_nutrition, unit_volume_nutrition)
                if volume_nutrition==None:
                    return {}
                value_nutrition=volume_nutrition*unit

                ingredient_nutritions['Calories']=float(nutritions[letter][food]['Calories'])*value_ingredient/value_nutrition
                ingredient_nutritions['Total Fat']=float(nutritions[letter][food]['Total Fat'][:-1])*value_ingredient/value_nutrition
                ingredient_nutritions['Total Carbohydrate']=float(nutritions[letter][food]['Total Carbohydrate'][:-1])*value_ingredient/value_nutrition
                ingredient_nutritions['Protein']=float(nutritions[letter][food]['Protein'][:-1])*value_ingredient/value_nutrition

                return ingredient_nutritions

            else:
                return {}

    def get_value(self, quantity, unit):
        check_number=False
        for i in quantity:
            if i.isdigit():
                check_number=True
        if not check_number:
            return None

        if '/' not in quantity:
            value=''
            for i in quantity:
                if i.isdigit():
                    value+=str(i)
                elif i=='.':
                    value+=i
                else:
                    break
            if value!='':
                return float(value)   
            else:
                return None
        else:
            position_divide=quantity.find('/')
            numerator=''
            for i in quantity:
                if i.isdigit():
                    numerator+=str(i)
                else:
                    break
            denominator=''
            for i in quantity[position_divide+1:]:
                if i.isdigit():
                    denominator+=str(i)
                else:
                    break
            return float(numerator)/float(denominator)

        return None
