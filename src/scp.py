def scraping(link, driver, random, time, By, re, NoSuchElementException):
    dict = {}
    driver.get(link['URL'])
    time.sleep(1 + random.random())
    # Proposição
    dict["Proposição"] = driver.find_element(By.XPATH, "//*[contains(text(), 'Medida Provisória n')]").text
    # URL
    dict["URL"] = driver.current_url
    # Ementa
    try:
        dict["Ementa"] = driver.find_element(By.XPATH,
                                             "//strong[text()='Ementa:']/following-sibling::br/following-sibling::span").text
    except NoSuchElementException:
        dict["Ementa"] = None
    # Indexação
    driver.find_element(By.CSS_SELECTOR, "#quadro-informacoes").click()
    time.sleep(1 + random.random())
    try:
        driver.find_element(By.XPATH, "//dt[text()='Indexação:']/following-sibling::dd")
        dict["Indexação"] = driver.find_element(By.XPATH, "//dt[text()='Indexação:']/following-sibling::dd").text
    except NoSuchElementException:
        dict["Indexação"] = None
    # Norma jurídica gerada
    try:
        dict["Norma gerada"] = driver.find_element(By.XPATH,
                                           "//dt[text()='Norma jurídica gerada:']/following-sibling::dd/a").text
    except NoSuchElementException:
        dict["Norma gerada"] = None
    # Audiências
    driver.find_element(By.CSS_SELECTOR, "#tramitacao_toggle").click()
    time.sleep(3 + random.random())
    page_content = driver.find_element(By.TAG_NAME, 'body').text # Separa o texto completo da página
    dict["Audiências públicas realizadas"] = page_content.count("É realizada Audiência Pública")
    # Emendas
    try:
        # Usa regex para localizar o número de emendas no texto completo (variável page_content, criada nas linhas anteriores)
        match = re.search(r'foram apresentadas (\d+) emendas', page_content)
        if match:
            numero_emendas = int(match.group(1))
        else:
            numero_emendas = 0
    except NoSuchElementException:
        # Se não encontrar o elemento 'body', define o número de emendas como None
        numero_emendas = None
    dict["Quantidade de emendas"] = numero_emendas

    return dict
