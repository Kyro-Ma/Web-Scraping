from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import pandas as pd
from styleframe import StyleFrame
from sklearn.utils import shuffle
import copy

# to-dp list, appearance topic loses appearancem body
topics = {
    # Animals
    'Animals': 'https://www.oxfordlearnersdictionaries.com/topic/animals',
    'Birds': 'https://www.oxfordlearnersdictionaries.com/topic/birds',
    'Fish and shellfish':'https://www.oxfordlearnersdictionaries.com/topic/fish-and-shellfish',
    'Insects, worms, etc':'https://www.oxfordlearnersdictionaries.com/topic/insects-worms-etc',
    # Appearance
    'Appearance': 'https://www.oxfordlearnersdictionaries.com/topic/appearance',
    'Body': 'https://www.oxfordlearnersdictionaries.com/topic/body',
    'Clothes and Fashion': 'https://www.oxfordlearnersdictionaries.com/topic/clothes-and-fashion',
    'Colors and Shapes': 'https://www.oxfordlearnersdictionaries.com/topic/colours-and-shapes',
    # Communication
    'Language': 'https://www.oxfordlearnersdictionaries.com/topic/language',
    'Phones, email and the Internet': 'https://www.oxfordlearnersdictionaries.com/topic/phones-email-and-the-internet',
    # Culture
    'Art': 'https://www.oxfordlearnersdictionaries.com/topic/art',
    'Film and theatre': 'https://www.oxfordlearnersdictionaries.com/topic/film-and-theatre',
    'Literature and writing': 'https://www.oxfordlearnersdictionaries.com/topic/literature-and-writing',
    'Music': 'https://www.oxfordlearnersdictionaries.com/topic/music',
    'TV, radio and news': 'https://www.oxfordlearnersdictionaries.com/topic/tv-radio-and-news',
    # Food and drink
    'Cooking and eating': 'https://www.oxfordlearnersdictionaries.com/topic/cooking-and-eating',
    'Drinks': 'https://www.oxfordlearnersdictionaries.com/topic/drinks',
    'Food': 'https://www.oxfordlearnersdictionaries.com/topic/food',
    # Functions
    # 'Discussion and agreement': 'https://www.oxfordlearnersdictionaries.com/topic/discussion-and-agreement',
    'Doubt, guessing and certainty': 'https://www.oxfordlearnersdictionaries.com/topic/doubt-guessing-and-certainty',
    'Opinion and argument': 'https://www.oxfordlearnersdictionaries.com/topic/opinion-and-argument',
    'Permission and obligation': 'https://www.oxfordlearnersdictionaries.com/topic/permission-and-obligation',
    'Preferences and decisions': 'https://www.oxfordlearnersdictionaries.com/topic/preferences-and-decisions',
    'Suggestions and advice': 'https://www.oxfordlearnersdictionaries.com/topic/suggestions-and-advice',
    # Health
    'Disability': 'https://www.oxfordlearnersdictionaries.com/topic/disability',
    'Health and Fitness': 'https://www.oxfordlearnersdictionaries.com/topic/health-and-fitness',
    'Health problems': 'https://www.oxfordlearnersdictionaries.com/topic/health-problems',
    'Healthcare': 'https://www.oxfordlearnersdictionaries.com/topic/healthcare',
    'Mental health': 'https://www.oxfordlearnersdictionaries.com/topic/mental-health',
    # Homes and buildings
    'Buildings': 'https://www.oxfordlearnersdictionaries.com/topic/buildings',
    'Gardens': 'https://www.oxfordlearnersdictionaries.com/topic/gardens',
    'Houses and homes': 'https://www.oxfordlearnersdictionaries.com/topic/houses-and-homes',
    # Leisure
    'Games and toys': 'https://www.oxfordlearnersdictionaries.com/topic/games-and-toys',
    'Hobbies': 'https://www.oxfordlearnersdictionaries.com/topic/hobbies',
    'Shopping': 'https://www.oxfordlearnersdictionaries.com/topic/shopping',
    # Notions
    'Change, cause and effect': 'https://www.oxfordlearnersdictionaries.com/topic/change-cause-and-effect',
    'Danger': 'https://www.oxfordlearnersdictionaries.com/topic/danger',
    'Difficulty and failure': 'https://www.oxfordlearnersdictionaries.com/topic/difficulty-and-failure',
    'Success': 'https://www.oxfordlearnersdictionaries.com/topic/success',
    # People
    'Education': 'https://www.oxfordlearnersdictionaries.com/topic/education',
    'Family and relationships': 'https://www.oxfordlearnersdictionaries.com/topic/family-and-relationships',
    'Feelings': 'https://www.oxfordlearnersdictionaries.com/topic/feelings',
    'Life stages': 'https://www.oxfordlearnersdictionaries.com/topic/life-stages',
    'Personal qualities': 'https://www.oxfordlearnersdictionaries.com/topic/personal-qualities',
    # Politics and society
    'Crime and punishment': 'https://www.oxfordlearnersdictionaries.com/topic/crime-and-punishment',
    'Law and justice': 'https://www.oxfordlearnersdictionaries.com/topic/law-and-justice',
    'People in society': 'https://www.oxfordlearnersdictionaries.com/topic/people-in-society',
    'Politics': 'https://www.oxfordlearnersdictionaries.com/topic/politics',
    'Religion and festivals': 'https://www.oxfordlearnersdictionaries.com/topic/religion-and-festivals',
    'Social issues': 'https://www.oxfordlearnersdictionaries.com/topic/social-issues',
    'War and conflict': 'https://www.oxfordlearnersdictionaries.com/topic/war-and-conflict',
    # Science and technology
    'Biology': 'https://www.oxfordlearnersdictionaries.com/topic/biology',
    'Computers': 'https://www.oxfordlearnersdictionaries.com/topic/computers',
    'Engineering': 'https://www.oxfordlearnersdictionaries.com/topic/engineering',
    'Maths and measurement': 'https://www.oxfordlearnersdictionaries.com/topic/maths-and-measurement',
    'Physics and chemistry': 'https://www.oxfordlearnersdictionaries.com/topic/physics-and-chemistry',
    'Scientific research': 'https://www.oxfordlearnersdictionaries.com/topic/scientific-research',
    # Sport
    'Sports: ball and racket sports': 'https://www.oxfordlearnersdictionaries.com/topic/sports-ball-and-racket-sports',
    'Sports: other sports': 'https://www.oxfordlearnersdictionaries.com/topic/sports-other-sports',
    'Sports: water sports': 'https://www.oxfordlearnersdictionaries.com/topic/sports-water-sports',
    # The nature world
    'Farming': 'https://www.oxfordlearnersdictionaries.com/topic/farming',
    'Geography': 'https://www.oxfordlearnersdictionaries.com/topic/geography',
    'Plants and trees': 'https://www.oxfordlearnersdictionaries.com/topic/plants-and-trees',
    'The environment': 'https://www.oxfordlearnersdictionaries.com/topic/the-environment',
    'Weather': 'https://www.oxfordlearnersdictionaries.com/topic/weather',
    # Time and space
    'History': 'https://www.oxfordlearnersdictionaries.com/topic/history',
    'Space': 'https://www.oxfordlearnersdictionaries.com/topic/space',
    'Time': 'https://www.oxfordlearnersdictionaries.com/topic/time',
    # Travel
    'Holidays': 'https://www.oxfordlearnersdictionaries.com/topic/holidays',
    'Transport by air': 'https://www.oxfordlearnersdictionaries.com/topic/transport-by-air',
    'Transport by bus and train': 'https://www.oxfordlearnersdictionaries.com/topic/transport-by-bus-and-train',
    'Transport by car or lorry': 'https://www.oxfordlearnersdictionaries.com/topic/transport-by-car-or-lorry',
    'Transport by water': 'https://www.oxfordlearnersdictionaries.com/topic/transport-by-water',
    # Work and business
    'Business': 'https://www.oxfordlearnersdictionaries.com/topic/business',
    'Jobs': 'https://www.oxfordlearnersdictionaries.com/topic/jobs',
    'Money': 'https://www.oxfordlearnersdictionaries.com/topic/money',
    'Working life': 'https://www.oxfordlearnersdictionaries.com/topic/working-life'
}

id_titles = {
    # Animals
    'Animals': 'l2:animals:animals_',
    'Birds': "l2:animals:birds_",
    'Fish and shellfish':"l2:animals:fish_and_shellfish_",
    'Insects, worms, etc': "l2:animals:insects_worms_etc_",
    # Appearance
    'Appearance': "l2:appearance:appearance_",
    'Body': "l2:appearance:body_",
    'Clothes and Fashion': "l2:appearance:clothes_and_fashion_",
    'Colors and Shapes': "l2:appearance:colours_and_shapes_",
    # Communication
    'Language': "l2:communication:language_",
    'Phones, email and the Internet': "l2:communication:phones_email_and_the_internet_",
    # Culture
    'Art': "l2:culture:art_",
    'Film and theatre': "l2:culture:film_and_theatre_",
    'Literature and writing': "l2:culture:literature_and_writing_",
    'Music': "l2:culture:music_",
    'TV, radio and news': "l2:culture:tv_radio_and_news_",
    # Food and drink
    'Cooking and eating': "l2:food_and_drink:cooking_and_eating_",
    'Drinks': "l2:food_and_drink:drinks_",
    'Food': "l2:food_and_drink:food_",
    # Functions
    'Discussion and agreement': "l2:functions:discussion_and_agreement_",
    'Doubt, guessing and certainty': "l2:functions:doubt_guessing_and_certainty_",
    'Opinion and argument': "l2:functions:opinion_and_argument_",
    'Permission and obligation': "l2:functions:permission_and_obligation_",
    'Preferences and decisions': "l2:functions:preferences_and_decisions_",
    'Suggestions and advice': "l2:functions:suggestions_and_advice_",
    # Health
    'Disability': "l2:health:disability_",
    'Health and Fitness': "l2:health:health_and_fitness_",
    'Health problems': "l2:health:health_problems_",
    'Healthcare': "l2:health:healthcare_",
    'Mental health': "l2:health:mental_health_",
    # Homes and buildings
    'Buildings': "l2:homes_and_buildings:buildings_",
    'Gardens': "l2:homes_and_buildings:gardens_",
    'Houses and homes': "l2:homes_and_buildings:houses_and_homes_",
    # Leisure
    'Games and toys': "l2:leisure:games_and_toys_",
    'Hobbies': "l2:leisure:hobbies_",
    'Shopping': 'l2:leisure:shopping_',
    # Notions
    'Change, cause and effect': "l2:notions:change_cause_and_effect_",
    'Danger': "l2:notions:danger_",
    'Difficulty and failure': "l2:notions:difficulty_and_failure_",
    'Success': "l2:notions:success_",
    # People
    'Education': "l2:people:education_",
    'Family and relationships': "l2:people:family_and_relationships_",
    'Feelings': "l2:people:feelings_",
    'Life stages': "l2:people:life_stages_",
    'Personal qualities': "l2:people:personal_qualities_",
    # Politics and society
    'Crime and punishment': "l2:politics_and_society:crime_and_punishment_",
    'Law and justice': "l2:politics_and_society:law_and_justice_",
    'People in society': "l2:politics_and_society:people_in_society_",
    'Politics': "l2:politics_and_society:politics_",
    'Religion and festivals': "l2:politics_and_society:religion_and_festivals_",
    'Social issues': "l2:politics_and_society:social_issues_",
    'War and conflict': "l2:politics_and_society:war_and_conflict_",
    # Science and technology
    'Biology': "l2:science_and_technology:biology_",
    'Computers': "l2:science_and_technology:computers_",
    'Engineering': "l2:science_and_technology:engineering_",
    'Maths and measurement': "l2:science_and_technology:maths_and_measurement_",
    'Physics and chemistry': "l2:science_and_technology:physics_and_chemistry_",
    'Scientific research': "l2:science_and_technology:scientific_research_",
    # Sport
    'Sports: ball and racket sports': "l2:sport:sports_ball_and_racket_sports_",
    'Sports: other sports': "l2:sport:sports_other_sports_",
    'Sports: water sports': "l2:sport:sports_water_sports_",
    # The nature world
    'Farming': "l2:the_natural_world:farming_",
    'Geography': "l2:the_natural_world:geography_",
    'Plants and trees': "l2:the_natural_world:plants_and_trees_",
    'The environment': "l2:the_natural_world:the_environment_",
    'Weather': "l2:the_natural_world:weather_",
    # Time and space
    'History': "l2:time_and_space:history_",
    'Space': "l2:time_and_space:space_",
    'Time': "l2:time_and_space:time_",
    # Travel
    'Holidays': "l2:travel:holidays_",
    'Transport by air': "l2:travel:transport_by_air_",
    'Transport by bus and train': "l2:travel:transport_by_bus_and_train_",
    'Transport by car or lorry': "l2:travel:transport_by_car_or_lorry_",
    'Transport by water': "l2:travel:transport_by_water_",
    # Work and business
    'Business': "l2:work_and_business:business_",
    'Jobs': "l2:work_and_business:jobs_",
    'Money': "l2:work_and_business:money_",
    'Working life': "l2:work_and_business:working_life_",
}


def getHtml(url):
    req = Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_8) AppleWebKit/534.50.2 (KHTML, like Gecko)\
         Version/5.0.6 Safari/533.22.3'
    })
    html_bytes = urlopen(req).read()
    html = html_bytes.decode("utf-8")
    return html


#
def obtainWords(url, topic, id_title):
    html = getHtml(url)
    soup = BeautifulSoup(html, "html.parser")

    # To get words for dictionary
    pattern_for_words = 'data-hw="[a-z ]*"'
    match_results_words = re.findall(pattern_for_words, html)
    filtration = '[a-z ]+"$'
    words_for_dictionary = []
    for result in match_results_words:
        word = re.findall(filtration, result)
        words_for_dictionary.append(word[0][:-1])

    # Because when u search for href of words by id, the words should be a little different,
    # so we modify the words for dictionary for the need of the words for href searching
    words_for_search_href = copy.deepcopy(words_for_dictionary)  # use deepcopy,so when change words_for_search_href,
    # it won't change words_for_dictionary
    for i in range(len(words_for_search_href)):
        # Get rid of space in the words
        if ' ' in words_for_search_href[i]:
            words_for_search_href[i] = words_for_search_href[i].replace(' ', '')
        times = words_for_search_href.count(
            words_for_search_href[i])  # find how many times this word appears in the list
        # if times > 1, like woof which appears 3 times, we change them to woof, woof1, woof2
        # number_use_to_add_after_word is the number to be added behind the word
        number_use_to_add_after_word = 1
        specific_word = words_for_search_href[i]
        while times > 1:
            for j in range(len(words_for_search_href)):
                if words_for_search_href[j] == specific_word:
                    words_for_search_href[j] += str(number_use_to_add_after_word)
                    break
            times -= 1
            number_use_to_add_after_word += 1
    print(words_for_dictionary)
    urls = []
    none_verb_etcs = []
    for word in words_for_search_href:
        # id = "l2:animals:animals_yak"
        supa = soup.find('li', attrs={'id': id_title + word})
        pattern_for_href = '/definition/english/[a-z- ]*_?[1-9]?'
        href = re.findall(pattern_for_href, str(supa))
        href = 'https://www.oxfordlearnersdictionaries.com' + href[0]
        urls.append(href)
        # print(supa)
        none_verb_etc = supa.find('span').text
        none_verb_etcs.append(none_verb_etc)

    # Get definitions of words
    definations = []
    for u in urls:
        html = getHtml(u)
        soup = BeautifulSoup(html, "html.parser")
        supa = soup.find_all('span', attrs={'class': 'def'})
        defination = ''
        for part_of_html in supa:
            defination += part_of_html.text + '; \n'
        definations.append(defination)

    df = pd.DataFrame({
        'Words': words_for_dictionary,
        'Grammar': none_verb_etcs,
        'Definitions': definations,
    })
    df = shuffle(df)
    # Using styleframe to export excel can make defitions to have multiple lines
    StyleFrame(df).to_excel(topic + '.xlsx').save()


if __name__ == '__main__':
    for topic, url in topics.items():
        obtainWords(url, topic, id_titles[topic])
