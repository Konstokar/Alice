from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
# создаём словарь, в котором ключ — название города, а значение — массив,
# где перечислены id картинок, которые мы записали в прошлом пункте.
cities = {
    'москва':
    [
        '1656841/7327010afa8d14a2c006',
        '1030494/1a0b99d07987cae3acf6',
        '1652229/0820457b332c20441ba5',
        '1540737/a2568ebee0ffbcbd0775',
        '1540737/a2568ebee0ffbcbd0775',
        '1656841/d0241e844e67be67ee20',
        '997614/57b9af04c5057f978abe'
    ],
    'санкт-петербург':
    [
        '1540737/03220caf83b94be2dda0',
        '1656841/d09e46ea8eec55ba2a9f',
        '1652229/233c0d9002d192df1a4a',
        '965417/24d5705c4041530f4101',
        '997614/a6388391d9a940b1f2fe',
        '1652229/853e998deedfc03749ac',
        '965417/d152ab14fe3aad19296c',
        '965417/7c58a97966d61ef3a7fd',
        '1540737/3b80caa4b578ee6ef8b8',
        '1540737/cdfc3b1a8050d17ea960'
    ],
    'великий новгород':
    [
        '1540737/41359f6451f1e1299fd5',
        '1540737/144ffa0e9438dca757e7',
        '937455/51508620bd90d154df7c',
        '1540737/e91dc704ea3628631d38',
        '1540737/b8edf25266b37f0fbc46',
        '1540737/e482fe3ee27a067a5cf5',
        '997614/367293af6320be540b70',
        '1652229/8d95e127e1e796aff457',
        '1652229/483b69626991a5139ce1',
        '937455/494f765ec1e8ae3d8bd5'
    ],
    'владимир':
    [
        '1540737/170331a54df7c66ce181',
        '1652229/3444c2dde8c00f69f27d',
        '1540737/94eb471002f7b8ff84eb',
        '965417/e947e07311a14d5589d7',
        '1540737/d781e1774b7d28c4fd3b',
        '965417/8eb23bf7591467588572',
        '1652229/ca5a40748fca09504205',
        '213044/7a3ef7c51efeabf5b0ae',
        '1652229/ffa01cf84bf62111ecb4',
        '1652229/f76f1465012dadb85d3c'
    ],
    'волгоград':
    [
        '1540737/9dc555ccf3b0fb9e8e15',
        '1656841/606054f7c831787ace41',
        '1030494/6aadcc56e554f6f8078f',
        '1652229/1b1111cdd1a2c6cd8552',
        '1030494/953e42cd7bc2fa09d0bd',
        '1652229/995b020fb3496d1ae733',
        '1540737/5815c98983da664f4f53',
        '1521359/3ead6cefa50c0caee7ef',
        '213044/944b93b4f843e72d7e6d',
        '1652229/7c306765b9b5d09dc252'
    ],
    'екатеринбург':
    [
        '1521359/cd9d61f65cf5c3671ad7',
        '1652229/4735c7d506af40c2aa33',
        '937455/60c4cb45001718611e11',
        '213044/f7c1f05c736f1fa8e27d',
        '937455/abf929aa8381ff5233fc',
        '1030494/84821e52bc7c9cf2bde0',
        '1540737/c58083f7f71b7de99c8e',
        '1030494/78329d5fc77a79d6d4ff'
    ],
    'казань':
    [
        '213044/e12c8b987a5ad6d924dc',
        '965417/537dc1a480e39ed03735',
        '997614/71cf10a16cdeaeb62109',
        '1540737/99a9d948e8fd01d64c90',
        '965417/ad5690e527ee9de97ba7',
        '965417/c09cd9fbc7254e6a886c',
        '1030494/5f6771d99fb0c4eb5bad',
        '997614/e1c8c3d46902d55db5cc',
        '1652229/4a407cbf7e4cd53d6fd7',
        '1521359/b137f7da4c7fc3590e1f'
    ],
    'калининград':
    [
        '213044/4f5af663e5989f3f5ee5',
        '1030494/b00c5738ea8a8bc5fdf6',
        '1652229/1a6a2b852ddab3228b7a',
        '937455/3f1aef8e0632bef1cbb7',
        '213044/5a9f35622ee48c7961ab',
        '965417/292a76d08165aebbee04',
        '965417/b1f87a20d8f826546ed8',
        '1540737/e52455e8135cb7c77f9e',
        '1652229/afbd7beb6b7a9b00ce09'
    ],
    'краснодар':
    [
        '1652229/ac6d2a006a0ecf616b49',
        '1652229/706f800e6c03a52c6c51',
        '1652229/e9fe4c3f55abe44403f2',
        '965417/b93f87c310ea8f496e62',
        '937455/fe730089197852668017',
        '213044/a428164943716c880ab7',
        '1652229/2f4bd2e5207f4cb549cf',
        '1656841/eaf0b5e1d072a2d382fa',
        '1652229/0786268c93d6efbe76fc'
    ],
    'мурманск':
    [
        '1652229/bf35c5227593cb89007b',
        '965417/23965b07b1f0ee85f860',
        '1652229/a99cc2ce7f72a6206441',
        '1656841/c8b5ea40ded008ff7648',
        '965417/19c8b62d798f97744011',
        '1652229/9d82f2d48cd6958c1f3b',
        '1652229/ca8943362b90ff611f2b',
        '1533899/144491f6f4b2d37233ca',
        '937455/ac9575f0c8c5a774e8ce'
    ],
    'нижний новгород':
    [
        '1540737/fe26890b9253b9c03c68',
        '1652229/08f4900219fe00676f0c',
        '1540737/094be60704750796a099',
        '1540737/8bff23ac67517c1a7607',
        '1656841/763e2d8f0f99331be699',
        '1030494/75768eebb6b4f8bf370e',
        '1652229/51e1e4958a313ea102e5',
        '213044/2c1d1e4621066e48ba17',
        '1656841/1c3480d24e291e6fc0de'
    ],
    'омск':
    [
        '997614/d1291d75f9c9adba7057',
        '1540737/102ca576facb7684936a',
        '1030494/349161cf7fb99eb92a3f',
        '213044/0afab2d3de048cdb4b99',
        '1030494/416077b77fb1c37d136f',
        '1652229/ee42c1931ce70068fc7f',
        '1656841/82f48b89b4828aa95925',
        '965417/29b070f41e90d772e790',
        '965417/af33d2c6b528c693c3b0'
    ],
    'пермь':
    [
        '1656841/b423ec9857e853d3e368',
        '1540737/b082d647d2156f9a72d8',
        '1652229/edcd146d2baf14adbfd2',
        '965417/0f2cef7d46e8ca44c2f6',
        '1540737/93a258c203b2b5c49281',
        '965417/ef7e88eb386edb817fe1',
        '1540737/e1befe6f8d6a5ece19e5',
        '1540737/5ee2271ac7eced9eb427',
        '1540737/82ed09989ca0520e10d6',
        '1030494/a8b4f0c671df7522a7e0'
    ],
    'ростов-на-дону':
    [
        '1540737/34fe7d9403b41a6954f1',
        '1540737/be95f1cd3e724cddf340',
        '1652229/8ab2f72e4b1d46e2f436',
        '1652229/80852225ce99368eb369',
        '965417/26de70176018c69c61e4',
        '1652229/e99f841d5c570ab375a2',
        '1656841/b2f7375c72f6e4ee101b',
        '1540737/c936add5bdf9eb0d2509',
        '1540737/76c804cd5e2f399827db',
        '1030494/0b194525ef1adec0b825'
    ],
    'саратов':
    [
        '997614/525d1b89b06ff1b3a7b0',
        '1540737/ef88a00c1f6b029296b8',
        '1656841/041d6220ff7236750c88',
        '997614/538d4b65044c743df436',
        '937455/fa3fad1c6464f97cf89e',
        '965417/c972230d50efc800957f',
        '1521359/e2b1bbaa3f8226189b68',
        '965417/979973037ead37620c5b',
        '1540737/185faed2b544f8fbe78e',
        '965417/ff8682f95edf8330dd79'
    ],
    'томск':
    [
        '1540737/7f4c1a17d177c235e915',
        '1652229/512bcfb536efe3316d4e',
        '1652229/7e072cccbb5bb30d141a',
        '1652229/78c0aa94d4c8f5966524',
        '1652229/6cba6b649a7f4e4aa288',
        '1540737/db10072040cca7482cb1',
        '1652229/7a8564a0163e08b908a6',
        '1656841/742ad99e005f0d029695',
        '965417/54c522cc0cb5f6828ca2',
        '965417/09cc55ce960612757f07'
    ],
    'уфа':
    [
        '1540737/05f3a5498edfacbb3533',
        '1030494/95cc97b9936f4f6687d1',
        '1652229/55b2ac4950084a71806e',
        '1540737/05d796afec941af9e886',
        '1656841/14ec829fc3a0d48802b9',
        '1540737/01ffb89f9c1aafc02adc',
        '1656841/35dc69806eec78e5c556',
        '965417/f43f241e95dec49cc5ed',
        '1533899/cea45ce7b14936432b32',
        '1030494/279f1253866eaae6dc82'
    ],
    'ярославль':
    [
        '1030494/9c9733b909d759d0bcd1',
        '1540737/6c7439b3396d515850c6',
        '997614/fcb0dab939ed1d50f23c',
        '1652229/54c0fad1e0af7319c474',
        '1652229/91c5b54688fa18e78cae',
        '1652229/fb44b3e51e4b1589819c',
        '1030494/36126aa624a6fff4060a',
        '1652229/f6b7ac0f6c93b040f779',
        '1652229/9622791823ad1c71cf30',
        '1540737/733a81edf707a95c68a0'
    ],
}
cit = cities.keys()

# создаём словарь, где для каждого пользователя мы будем хранить его имя
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови своё имя!'
        sessionStorage[user_id] = {
            'first_name': None,  # здесь будет храниться имя
            'game_started': False  # здесь информация о том, что пользователь начал игру. По умолчанию False
        }
        return

    if sessionStorage[user_id]['first_name'] is None:
        first_name = get_first_name(req)
        if first_name is None:
            res['response']['text'] = 'Не расслышала имя. Повтори, пожалуйста!'
        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' + first_name.title() \
                          + '. Я - Алиса. Вбей название города, которого ты хочешь увидеть ' \
                            '(если я его знаю). \nСейчас я знаю города:\n{}'.format(',\n'.join(cit))
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [
                {
                    'title': 'Помощь',
                    'hide': True
                }
            ]
    # если мы знакомы с пользователем и он нам что-то написал,
    # то это говорит о том, что он уже говорит о городе, что хочет увидеть.
    else:
        if 'помощь' in req['request']['nlu']['tokens']:
            res['response']['text'] = 'Я показываю тебе фотографии города, названного тобой ' \
                                      '(если я его знаю). \nСейчас я знаю города:\n{}'.format(',\n'.join(cit))
            res['response']['end_session'] = True
            res['response']['buttons'] = [
                {
                    'title': 'Помощь',
                    'hide': True
                }]
            return
        # ищем город в сообщение от пользователя
        city = get_city(req)
        # если этот город среди известных нам,
        # то показываем его (выбираем одну из двух картинок случайно)
        if city in cities:
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю.'
            res['response']['card']['image_id'] = random.choice(
                cities[city])
            res['response']['text'] = 'Я угадал!'
        # если не нашел, то отвечает пользователю
        # 'Первый раз слышу об этом городе.'
            res['response']['buttons'] = [
                {
                    'title': 'Города, которые я знаю',
                    'hide': True
                }
            ]
            res['response']['buttons'].append(
                {'title': 'Помощь', 'hide': True}
            )
        else:
            res['response']['text'] = \
                'Первый раз слышу об этом городе. Попробуй еще разок!'
            res['response']['buttons'] = [
                {
                    'title': 'Помощь',
                    'hide': True
                }
            ]

def get_city(req):
    # перебираем именованные сущности
    for entity in req['request']['nlu']['entities']:
        # если тип YANDEX.GEO то пытаемся получить город(city),
        # если нет то возвращаем None
        if entity['type'] == 'YANDEX.GEO':
            # возвращаем None, если не нашли сущности с типом YANDEX.GEO
            return entity['value'].get('city', None)


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
