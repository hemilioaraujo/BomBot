from selenium.webdriver import Firefox

class Rastreador:
    def __init__(self):
        self._url_rastreador = 'https://www2.correios.com.br/sistemas/rastreamento/default.cfm'
        # itens = 'PZ153830489BR;PZ121976672BR;PZ109998961BR'
        self._browser = Firefox()
        # browser = Firefox(executable_path='/usr/local/bin')
        self._browser.implicitly_wait(10)

    def buscar_rastreamento(self, item):
        form_objetos = 'objetos'
        form_btn_buscar = 'btnPesq'
        self._browser.get(self._url_rastreador)
        input_objetos = self._browser.find_element_by_id(form_objetos)
        input_btn_buscar = self._browser.find_element_by_id(form_btn_buscar)
        input_objetos.send_keys(item)
        input_btn_buscar.click()

    def pegar_dados(self):
        result_data_class = 'sroDtEvent'
        result_conteudo_class = 'sroLbEvent'
        data = self._browser.find_elements_by_class_name(result_data_class)
        conteudo = self._browser.find_elements_by_class_name(result_conteudo_class)
        data = self._browser.find_elements_by_class_name(result_data_class)
        conteudo = self._browser.find_elements_by_class_name(result_conteudo_class)

        return data, conteudo

    def print_dados(self, data, conteudo):
        for i in range(len(data)):
            print(data[i].text)
            print(conteudo[i].text)

    def kill(self):
        self._browser.quit()


if __name__ == '__main__':
    item = 'PZ109998961BR'
    a = Rastreador()
    a.buscar_rastreamento(item)
    data, conteudo = a.pegar_dados()
    a.print_dados(data, conteudo)
    a.kill()
