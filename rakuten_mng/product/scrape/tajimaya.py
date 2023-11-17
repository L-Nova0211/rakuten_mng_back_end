import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

from rakuten_mng.utils.convertext import convert_text, convert_product_name


class ScrapingEngine:
    def __init__(self) -> None:
        self.headers = {
            'Cookie': '_gcl_au=1.1.125596646.1692779382; b_closed_news=eyJpdiI6IlhlcmVkNVFEVnQwUzFPUFl6eGJ4ZEE9PSIsInZhbHVlIjoiVytwbERwRWNkS3lhOEhKUXRyWU9yVkdKRTF1Q0lNdnl4Q0kxaE9qamdDRG9SNXNUdUlXU0I4ZmEwMk0vN3U3Z3hxWXp4YmNlQllKRGMwQWVGdXlCbnc9PSIsIm1hYyI6IjdkNGQ4YmQwNjRjOTRhYTY5OTBmNGNlNWNmNzQ3NDVjODRmYWU5MTc5YzE0NDA2MTE0ZThjOWQ4ODFmNzFmZDEifQ%3D%3D; v_style=eyJpdiI6IkRhTUhjc1NaZVQrMTByai9GNi9wa2c9PSIsInZhbHVlIjoiS3VJN0R1WGR3V3hTaERmZ1RTc0xNMnphTUF2RVNsU2dvaE50b3ZyTVY3OWRXVGJUWk5pVUFvZ2FianZ4b3NFSyIsIm1hYyI6ImRiYTJlMmI4MzNlZTdiNmE4MDZjZDA3M2M5ZjFmNWZhNDBlYWVjZGU2NzRhMDY1YjI4MTEzY2IwOTE4M2Y2MmIifQ%3D%3D; product_viewed=eyJpdiI6IllTdWlvQkxnQVlOcFN5cDE4MFBRWlE9PSIsInZhbHVlIjoiS2x1bEY2NUkyQWZWbVhFWnpkQjVXNFVlK0RxYStrYjJtYjBPMWNXZGNsellWYW5sSXJ5UmQ0clZHWTdVV2loWkt5SWV2SEpTcm1lb0phVzhNa3NCdkVEWmxtSEpLMnV6V1Q5N1lYU2VvdWxEc3VwOHVuWHBLdUpGWVR4ekVKZlp3UWtQb05nc3ZQeUtzTW9KWVpzOVZKYkZ6V2w5MW1pYWNQSFNVbVF5dkVEZ1dqK0FHelNXMVY0OXduOUtqK09MUDY2Y1hYak5oRi94bFVoYS9paFl1NmdoeklCcG1RR2piRUI3SzdzOG9OR1B1RHNkb0VGTnZVaThJUG4vZ28zV2dGUkNrZG1ZaUt5U0FVRVN3TktOWHoxSnRTVWJ5emhtU0QzTFVoM0JkbFFtS1NnNE5zNnMxME5PWkV4dW1uaGVPRjlsR2wvSXdkZmc3ZjNGMU9UMWpJTk4wZi95V0N3MzBhbHkrMDBSZWt6NmZpeEZQMmlQbkxwM21QMDIvSTk5VTBIdWY5V2J0eTdnQWQ3NXFiQXNvTVhvYkJMZENIYWRvZnNyM1M2S01SSWozcnprQlJSZWxMc0kzb08yYmlhazlDU2FTcVhtc1VZZW13S0tYV3pYR3J5eDNxZk5KQ1FvcWlXbkFPWlBzcjQ9IiwibWFjIjoiZTdmMWRlNjdjMWI2MzUxMzlmMmZkYjQyM2Q1YzkyZGM0Yjk3YTAyMTA3NGMxYmQzNTQ3ODdkYTFkZGUzYjEzMiJ9; _ga=GA1.1.2074209682.1692779382; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6Iitwb3Y4RFpRMHJEZDRxcXYvdFczdHc9PSIsInZhbHVlIjoiUzNJa08za0w1ekZ4N09hcVNCdm1mZjJPRTVnV3RKeEw4aEpCdGVpcFBEdnc2RDc5N21ORFdoeXhqdWdUbTdQblQwc0hnaGgyTndKWEd0L0k2eEljeEhreTgzZmcvUmF1SDJaN0dYUE5PV1JZbmdDOTJ5UjdxZktST09WZFA4UzBZalFYaU85ZHozSVJUak9BY3BTRDdPd1BFR2g2dUtoeUdXOTFwR3AyRVAyb0NnblhCVTFTVG9ZcThqd2FoQlp1dEZ6TENvV0RGNW9mWXZRbHhuQnBCRGFOdndNYWRLTEZBYlduS3VLSHlsaz0iLCJtYWMiOiI5OTQ5MTM5MWQzNmE1NzM1MGM4YTk4ODBlZDVjYjEwNjY1NDFiYTQwZmQxMTlkNDlhNGEyM2I3MTZhM2E5ODZmIn0%3D; _ga_DY0XVSV4WZ=GS1.1.1700187410.51.0.1700187410.60.0.0; _EXPL_SID_=tajimaya-oroshi/243C5F6DDEA006168AA00CF6288899AE.node2goya&; _EXPL_TAJIMAYA-OROSHI_=Z1703_UicRlZ9O3HdEVzEm5_N._Sw-AvXasFZskWdC4h2B7USa.2tomatoYtQCR_V39988YtQCR_N0_Syju0bKIrlf8SX7N4MMRxWZ.2tomatoYtQmy_V39988YtQmy_V39988YtQol_V39988YtQov_V39988YtQpI_V39988YtQq0_V39988YtQqg_V39988YtQrL_V39988YtQty_N1_SxUFcK9xWa1RvAEWFSa3WyV.2tomatoYtX.o_V40110YtX.o_V40109YtX.z_V39982YtX0F_V5078YtXAm_N2_SwqCcKS0fnafEBujUMH2Kz4.2tomatoYteLt_V38619YtePP_N3_SzNTvvTaczYVVSJsTqlyCAz.2tomatoYu0S9_N4_SxU2.nCMqlKJmMfDk10kdCR.2shrimpZ3V.X_V35669Z3V3B_V35669Z3V3a_N5_SxRt8RhvYkvJgMt9H2A1r1z.2tomatoZ4c-x_V35669Z4c-x_V5806Z4c.M_V5806Z4cvq_V5806Z4cwZ_V911Z4cxx_V16354Z4d-D_N6_SxRt8RhvYkvJgMt9H2A1r1z.2tomatoZ4fYl_V16354Z4fYl_V16354Z4fwb_V27914Z4fwn_N7_Sx6Nm0gw0UuRwx1Mwpk2Wil.2tomatoZ4wx9_N8_Swv9Pf3cizpYiqIOfb6Z1eD.2goyaZ4x1O_V4620Z4x4u_N9_Sxz6I7y7Qy9wYm5fRdiQzel.2goyaZ58ua_NA_SzVzn-8WQVlHFVIWe3ETZIs.2goyaZ5fAE_NB_Sxgim298u0klYymVK6a6POW.2goyaZ5qtS_NC_SwsnF4CUzCW03UrIIF5hFfO.2tomatoZ5ulv_ND_Szdy2-w72auXsEQ8tyYHT5O.2tomatoZ6Dcq_NE_SxMyBybuH4XCXSA7ieH3vzH.2shrimpZ6TTI_NF_SwyLehODzDWTIYePVOsQqQf.2goyaZ7oxa_NG_SwSVJmDHHHkH6eY34xmG9PN.2goyaZ7p0l_NH_Sw9j46318b43y8bnlG4XZEz.2goyaZ7sXd_NI_Sz6fb6b.CGKFq5Rc2hHf-hZ.2goyaZ8A7B_NJ_SytZVsZ0bLCr0wLMZdF-R-6.2shrimpZ9ai0_NK_Sy3Y5sirttxYTjRrsPRQaXR.2shrimpZ9mWF_V911Z9uHn_V911Z9uN7_V911Z9uY3_V937Z9ufY_NL_SwusZHLhTOYVaQguBhu5DHa.2goyaZA9CX_NM_SzTYw0CZxIGJIumfTY35458.2shrimpZCcor_NN_Sw57Uh1w0caZl-NwVxX8f8B.2shrimpZCqjt_NO_SzCUGA2OPrxS.9ThzSgRTog.2tomatoZECvO_NP_Swj8HVxz8zEKK2ly2tKbYLs.2tomatoZEGrw_NQ_Sz989DA8vEfQZNOY6.EsRdO.2tomatoZF8Jw_NR_SyYuwxF.1zDCuV.r.kC0TUd.2goyaZGOH5_NS_SzELfRo.iobFD4IlhcOir30.2shrimpZHB8k_NT_SxJX1vFWh6C6atKEHiwUVs-.2shrimpZHTU-_NV-_Sy5.IWAgeunBao67jitq47d.2tomatoZI5bU_NV._Sz50e3B7bIxE6POuMkjx3I1.2goyaZIKNh_NV0_SyZgqLfq6ayLmzLLzMCsjum.2goyaZJeHg; XSRF-TOKEN=eyJpdiI6Ii9jMUFJNkZha0ZqWmpENFBJUzJVdHc9PSIsInZhbHVlIjoiWVVnWkVoOGgrUWhmT0s0YUdzTkY2SFZTbTJFVlA2VUZYZjlCQ1pHSjI4aDQ4cGtnc25kS0QxQ3FXMWkxQU10b2JQWWNjb3JMcXNDcXlaZ1pXMEl0U1JPY1ozazNhYml2MEd0WWI5QWttazEyU0Z4UktJeDJtbFg2MG93WTVlVjEiLCJtYWMiOiJjNjhmMTU0ODNiNzExMTEzM2E3NGNlYTI1ZGZhNjQzYTQ4MmRiOGRlMDMwNDgxZTQyMjFhODc0MzkzYjRhNDhhIn0%3D; b_ses=eyJpdiI6InpYZEMybUtlY0tHWVB0SGV3dDM4amc9PSIsInZhbHVlIjoiWFpZUUd1bHlqUzNaYTlCNDV0amJHWUZEM0JSdkk3bHJDVlovbllxajRsQ2dqeGxFQklSOVJSZ1ZXYXRuU1p6WGQ4MTV5N0lyWTBONm9udkUyR2oxZXlBWHZxTGVmQUp0TFoyMDluRWQ2QWxaa29YWlRGRUcyMTdiRG44aVMvbEwiLCJtYWMiOiJhYzY3MjcwNTQ2YWE4YjY5ZmNmZWQ5M2ZmZGJiOWUyODhkZjY0MTEwYjFjNzk2MTNkMjEyZWVjNTlkOWJhM2M5In0%3D; _EXPL_TIME_=tajimaya-oroshi/1700187651140&'
        }

    def scrape_item(self, source_url, data, result):
        resp = requests.get(
            headers=self.headers,
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        item_detail = dom.find('section', attrs={'class': '__information'})
        data['jan'] = item_detail.find('div', attrs={'class': '__spec'}).table.tr.td.text
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        data['price'] = int(float(dom.find('span', attrs={'class': 'c-tax-price __tax-price __is-none'}).text.split('円')[0].replace(',', '')))
        data['count_set'] = int(dom.find('span', attrs={'class': '__quantity'}).text)
        data['quantity'] = 20 # TODO
        data['title'] = f'{data["title"]} {data["count_set"]}個セット'
        photos = item_detail.find('div', attrs={'class': '__photo'}).find('div', attrs={'class': '__main'}).find_all('a')
        for photo in photos:
            url = photo['href']
            data['photos'].append(
                {
                    'url': url
                }
            )
        
        result.append(data)
    
    def scrape_item_list(self, source_url):
        response = requests.get(
            headers=self.headers,
            url=source_url
        )
        dom = bs(response.text, "html.parser")

        # Get Products
        result = []
        temp = dom.find('ul', attrs={'class': '__product'}).contents
        items = [item for item in temp if isinstance(item, str) is False]
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=len(items))

        for item in items:
            try:
                item_url = item.a['href']
                data = {}
                data['title'] = convert_text(item.find('h2', attrs={'class': '__title'}).text)
                data['title'] = convert_product_name(data['title'])
                data['source_url'] = item_url
                data['description'] = data['title']
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass

        pool.shutdown(wait=True)
        return result
    