def write_offer(text_offer):
    offer_dict = text_offer.__dict__
    first_name = offer_dict['json']['chat']['first_name']
    username = offer_dict['json']['chat']['id']
    text = offer_dict['json']['text']
    with open('offer.txt', 'a', encoding='utf-8') as file:
        file.write(f'Name - {first_name}. id - {username}. Offer text - {text}')
        file.write('\n')
