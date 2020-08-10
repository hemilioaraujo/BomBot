from selenium.webdriver import Firefox

itens = 'PZ109998961BR'
url_rastreador = 'https://www2.correios.com.br/sistemas/rastreamento/default.cfm'
# itens = 'PZ153830489BR;PZ121976672BR;PZ109998961BR'
browser = Firefox()
# browser = Firefox(executable_path='/usr/local/bin')
browser.implicitly_wait(10)


def buscar_rastreamento(itens):
    form_objetos = 'objetos'
    form_btn_buscar = 'btnPesq'
    result_data_class = 'sroDtEvent'
    result_conteudo_class = 'sroLbEvent'
    browser.get(url_rastreador)
    input_objetos = browser.find_element_by_id(form_objetos)
    input_btn_buscar = browser.find_element_by_id(form_btn_buscar)
    input_objetos.send_keys(itens)
    input_btn_buscar.click()

    data = browser.find_elements_by_class_name(result_data_class)
    conteudo = browser.find_elements_by_class_name(result_conteudo_class)

    # browser.quit()

    return data, conteudo


if __name__ == '__main__':
    data, conteudo = buscar_rastreamento(itens)
    for i in range(len(data)):
        print(data[i].text)
        print(conteudo[i].text)
    browser.quit()
