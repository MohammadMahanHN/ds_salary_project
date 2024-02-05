import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from time import sleep


def get_jobs(job_field, num_jobs=5, slp_time=5, debug=False, max_num_jobs=False):
    driver = webdriver.Chrome()
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + job_field + "&sc.keyword=" + job_field + "&locT=&locId=&jobType="
    driver.get(url)

    if max_num_jobs:
        title = driver.title.strip()
        max_job_count = ''.join(filter(str.isdigit, title))
        num_jobs = int(max_job_count)

    jobs = []
    for _ in range(num_jobs):
        print(f'Processing {_ + 1}/{num_jobs}')

        if (_ + 1) % 30 == 1:
            driver.find_element(by=By.XPATH,
                                value='/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/div/button').click()
            sleep(slp_time)

        print("-----------------------------------") if debug else None
        job_title_fxp = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{_ + 1}]/div/div/div[1]/div[1]/a[1]'
        job_title = driver.find_element(by=By.XPATH, value=job_title_fxp).text
        print('job title: ', job_title) if debug else None

        salary_estimate_fxp = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{_ + 1}]/div/div/div[1]/div[1]/div[3]'
        try:
            salary_estimate = driver.find_element(by=By.XPATH, value=salary_estimate_fxp).text[:-16]
            print('salary estimate: ', salary_estimate) if debug else None
        except NoSuchElementException:
            salary_estimate = None

        rating_fxp = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{_ + 1}]/div/div/div[1]/div[1]/div[1]/div[2]/div'
        try:
            rating = driver.find_element(by=By.XPATH, value=rating_fxp).text
            print('rating: ', rating) if debug else None
        except NoSuchElementException:
            rating = None
            print('no rating') if debug else None

        company_name_fxp = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{_ + 1}]/div/div/div[1]/div[1]/div[1]/div[2]/span'
        try:
            company_name = driver.find_element(by=By.XPATH, value=company_name_fxp).text
            print('company: ', company_name) if debug else None
        except NoSuchElementException:
            company_name = None
            print('no company') if debug else None

        location_fxp = f'/html/body/div[3]/div[1]/div[3]/div[2]/div[1]/div[2]/ul/li[{_ + 1}]/div/div/div[1]/div[1]/div[2]'
        try:
            location = driver.find_element(by=By.XPATH, value=location_fxp).text
            print('location: ', location) if debug else None
        except NoSuchElementException:
            location = None
            print('no location') if debug else None

        location_element = driver.find_element(by=By.XPATH, value=location_fxp)
        ActionChains(driver).key_down(Keys.CONTROL).click(location_element).key_up(Keys.CONTROL).perform()
        sleep(slp_time)

        size_fxp = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[1]/div'
        try:
            size = driver.find_element(by=By.XPATH, value=size_fxp).text
            print('size: ', size) if debug else None
        except NoSuchElementException:
            size = None
            print('no size') if debug else None

        founded_fxp = '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[2]/div'
        try:
            founded = driver.find_element(by=By.XPATH, value=founded_fxp).text
            print('founded: ', founded) if debug else None
        except NoSuchElementException:
            founded = None
            print('no founded') if debug else None

        type_of_ownership_fxp = '//*[@id="app-navigation"]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[3]/div'
        try:
            type_of_ownership = driver.find_element(by=By.XPATH, value=type_of_ownership_fxp).text
            print('type_of_ownership: ', type_of_ownership) if debug else None
        except NoSuchElementException:
            type_of_ownership = None
            print('no type_of_ownership') if debug else None

        industry_fxp = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[4]/div'
        try:
            industry = driver.find_element(by=By.XPATH, value=industry_fxp).text
            print('industry: ', industry) if debug else None
        except NoSuchElementException:
            industry = None
            print('no industry') if debug else None

        sector_fxp = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[5]/div'
        try:
            sector = driver.find_element(by=By.XPATH, value=sector_fxp).text
            print('sector: ', sector) if debug else None
        except NoSuchElementException:
            sector = None
            print('no sector') if debug else None

        revenue_fxp = '/html/body/div[3]/div[1]/div[3]/div[2]/div[2]/div[1]/section/section[2]/div/div/div[6]/div'
        try:
            revenue = driver.find_element(by=By.XPATH, value=revenue_fxp).text
            print('revenue: ', revenue) if debug else None
        except NoSuchElementException:
            revenue = None
            print('no revenue') if debug else None

        jobs.append({"Job Title": job_title,
                     "Salary Estimate": salary_estimate,
                     "Rating": rating,
                     "Company Name": company_name,
                     "Location": location,
                     "Size": size,
                     "Founded": founded,
                     "Type of ownership": type_of_ownership,
                     "Industry": industry,
                     "Sector": sector,
                     "Revenue": revenue})

        df = pd.DataFrame(jobs)
        df.to_excel('glassdoor-datascience-jobs.xlsx', index=False)

    driver.quit()

    return jobs


get_jobs('Data Science', num_jobs=9000)
