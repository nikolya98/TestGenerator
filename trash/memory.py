def ad_unit_analyze(temps_with_ad_unit):
    '''
    Функция анализирует содержимое блока Using
    '''

    # obj_pattern = r'\$\S+'
    # op_pattern = r'\*'
    # objs = []
    # ops = []

    for temp in temps_with_ad_unit:
        with open(f'{PATH}{temp}', 'r', encoding='utf-8') as tmp:
            text = tmp.readlines()
            text_to_str = ''.join(text)
            ad_unit = re.search(r'using\([\s\S[^)]+?\)', text_to_str, re.IGNORECASE)
            ad_unit_body = ad_unit.group()
            objs = re.findall(r'\$[a-zA-z]+', ad_unit_body)
            ops = re.findall(r'\*', ad_unit_body)

        return objs, ops


def generate():
    '''
    Функция построчно читает шаблоны .txt, расположенный в path
    и осуществляет запись в tests/test_name.c'
    '''

    for temp in temps:
        with open(f'{PATH}{temp}', 'r', encoding='utf-8') as tmp:
            line = tmp.readline()
            test = open(f'tests/test_{temp.replace(".txt", "")}.c', 'w+', encoding='utf-8')

            while line:
                test.write(line)
                line = tmp.readline()

            test.close()