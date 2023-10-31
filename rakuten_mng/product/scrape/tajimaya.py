import concurrent.futures
import requests
from bs4 import BeautifulSoup as bs

from rakuten_mng.utils.convertext import convert_text, convert_product_name


class ScrapingEngine:
    def scrape_item(self, source_url, data, result):
        resp = requests.get(
            url=source_url
        )
        dom = bs(resp.content, "html.parser")

        item_detail = dom.find('section', attrs={'class': '__information'})
        data['jan'] = item_detail.find('div', attrs={'class': '__spec'}).table.tr.td.text
        # data['description'] = convert_text(item_detail.find('div', attrs={'class': '__description'}).text)
        data['quantity'] = 20 # TODO
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
        headers = {
            'Cookie': '_gcl_au=1.1.125596646.1692779382; b_closed_news=eyJpdiI6IlhlcmVkNVFEVnQwUzFPUFl6eGJ4ZEE9PSIsInZhbHVlIjoiVytwbERwRWNkS3lhOEhKUXRyWU9yVkdKRTF1Q0lNdnl4Q0kxaE9qamdDRG9SNXNUdUlXU0I4ZmEwMk0vN3U3Z3hxWXp4YmNlQllKRGMwQWVGdXlCbnc9PSIsIm1hYyI6IjdkNGQ4YmQwNjRjOTRhYTY5OTBmNGNlNWNmNzQ3NDVjODRmYWU5MTc5YzE0NDA2MTE0ZThjOWQ4ODFmNzFmZDEifQ%3D%3D; _ga=GA1.1.2074209682.1692779382; _EXPL_SID_=tajimaya-oroshi/3507A7960CDD4F63D437FAE744B4FF50.node2shrimp&; remember_customer_59ba36addc2b2f9401580f014c7f58ea4e30989d=eyJpdiI6IjhpOEhJVzhYcjQwMmZRdEs5QUNRWXc9PSIsInZhbHVlIjoiRDJDUjBNZXQ0aGhLUWdIcEM5Y3ZaRjdmZUJXb2Ntdm5BOGNNZTljYldKdHNyT2dVdjBpemc0SjdZeXJyYlJYQlpVanBLTzhzbEx4MVRlZkNseGJwYjBuaW5OWEprZzl3Rit5b1dHaVVmMFRRSDdpT25VVFFabEpOdTkxM2ZZNittcjVna0QwVUdpMXQ5T0svSjljU1BpaVZRTzEwTUkxeGI2UzlpU2FjTmhWNzVuTW5iY0lZUnZnOXdNUld5cVI1M0N4cnp6M0M5aUxsUW0yVW1OQ0NIblBjeUxyTDRsZGJUQU55aG5zWHZpRT0iLCJtYWMiOiI1OGZiOTI5NjgxMzljM2UyMWIyY2E2MmE0OTE1ZWIyYTNmZGExZTUzNTExOWQ5NGU4MWFjNTkzYTAzMjQ2N2I1In0%3D; product_viewed=eyJpdiI6IlJkRXcwbEMzTUVVM0N5T2NXaVY4NVE9PSIsInZhbHVlIjoiVW5DVTEwYTY5NGFvd3VDNGFxK25DZThxV2dyUEpTbzhLKzI5Szd1L0dUcEhkdHRJT08rM0VOTElud0trRU9TYkQ5eFFaaFI4U1R0RDFFTUxHeWhCbm1qVHVLbWlubDM2aXhOU0NCOGdSLzQ5bXAybjI1K0tzcG4xT0dpVWFEQTZhUlU3bjRJWk1pb0pkZkkrdDNhR05SU1doZVAzN3kvWWswbjJ1VU5ia0dRbVRSNlE4TWp2YzJuYVh0bUNoUmpyV2I4L3E5ZmwyWmZDL3Y2UkV6RCtDdVU3Z0xvTWRiblhIOXpLamZuajl1VW1SaTdDSmtLRzM4YzI1WlJnTmV2M2kweFFkWFFYT3JZdjI3SXF5Sjd0MlpndHhnMTl2bnBXcXpFYzBkeTZQbGpPbkYrcERmRzBCclIyZCsxaGRzUEo2d3E3b2p5b05ZVHdCNjE1MTUzbXR3QVEzM01LT0JaRlRMVXc4YnNLSlUzSWNaYitMdCtIUzNYd29Gd0t2anZvL0lOZDRoczIxTmRuVmNobU5SYmRuK2x5N0pQcE9iRlFWUkYzeGJCNmdLOFM0THRFbG4yUkJHcFBLeEdXc2lpdUdCSHp6eldNVU02MThNNXprNWczWmc9PSIsIm1hYyI6IjIyOTc4NjhiMmVjOWMzNzMyMGQ4Zjk4M2ZkZTg0MGQ0MjE5NDUyZWJkYzZkY2UxZWQ0ZWY1ZDE0ZjZjOTExNjkifQ%3D%3D; _EXPL_TAJIMAYA-OROSHI_=Z1703_UicRlZ9O3HdEVzEm5_N._Sw-AvXasFZskWdC4h2B7USa.2tomatoYtQCR_V39988YtQCR_N0_Syju0bKIrlf8SX7N4MMRxWZ.2tomatoYtQmy_V39988YtQmy_V39988YtQol_V39988YtQov_V39988YtQpI_V39988YtQq0_V39988YtQqg_V39988YtQrL_V39988YtQty_N1_SxUFcK9xWa1RvAEWFSa3WyV.2tomatoYtX.o_V40110YtX.o_V40109YtX.z_V39982YtX0F_V5078YtXAm_N2_SwqCcKS0fnafEBujUMH2Kz4.2tomatoYteLt_V38619YtePP_N3_SzNTvvTaczYVVSJsTqlyCAz.2tomatoYu0S9_N4_SxU2.nCMqlKJmMfDk10kdCR.2shrimpZ3V.X_V35669Z3V3B_V35669Z3V3a_N5_SxRt8RhvYkvJgMt9H2A1r1z.2tomatoZ4c-x_V35669Z4c-x_V5806Z4c.M_V5806Z4cvq_V5806Z4cwZ_V911Z4cxx_V16354Z4d-D_N6_SxRt8RhvYkvJgMt9H2A1r1z.2tomatoZ4fYl_V16354Z4fYl_V16354Z4fwb_V27914Z4fwn_N7_Sx6Nm0gw0UuRwx1Mwpk2Wil.2tomatoZ4wx9_N8_Swv9Pf3cizpYiqIOfb6Z1eD.2goyaZ4x1O_V4620Z4x4u_N9_Sxz6I7y7Qy9wYm5fRdiQzel.2goyaZ58ua_NA_SzVzn-8WQVlHFVIWe3ETZIs.2goyaZ5fAE_NB_Sxgim298u0klYymVK6a6POW.2goyaZ5qtS_NC_SwsnF4CUzCW03UrIIF5hFfO.2tomatoZ5ulv_ND_Szdy2-w72auXsEQ8tyYHT5O.2tomatoZ6Dcq_NE_SxMyBybuH4XCXSA7ieH3vzH.2shrimpZ6TTI_NF_SwyLehODzDWTIYePVOsQqQf.2goyaZ7oxa_NG_SwSVJmDHHHkH6eY34xmG9PN.2goyaZ7p0l_NH_Sw9j46318b43y8bnlG4XZEz.2goyaZ7sXd_NI_Sz6fb6b.CGKFq5Rc2hHf-hZ.2goyaZ8A7B_NJ_SytZVsZ0bLCr0wLMZdF-R-6.2shrimpZ9ai0_NK_Sy3Y5sirttxYTjRrsPRQaXR.2shrimpZ9mWF_V911Z9uHn_V911Z9uN7_V911Z9uY3; v_style=eyJpdiI6IkRhTUhjc1NaZVQrMTByai9GNi9wa2c9PSIsInZhbHVlIjoiS3VJN0R1WGR3V3hTaERmZ1RTc0xNMnphTUF2RVNsU2dvaE50b3ZyTVY3OWRXVGJUWk5pVUFvZ2FianZ4b3NFSyIsIm1hYyI6ImRiYTJlMmI4MzNlZTdiNmE4MDZjZDA3M2M5ZjFmNWZhNDBlYWVjZGU2NzRhMDY1YjI4MTEzY2IwOTE4M2Y2MmIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6IkZGSUtXQWRxQlBpc01tR1FsWWRTNUE9PSIsInZhbHVlIjoieUlzcGtpTno0NTI5L3lZdWYzaWs1elNwS3JFeERHaExCOEhscXo1RWQwVFdrNHJ2YjNoUEc4RHpDR3MrT0Qva1M3WGlFakVhMzhoUnJDYzQzdkVhNGYvQUk0cmFpN0liRHgzaUdRa0xBU0FVZ1R3M3pPSFVtb0lkTWI3bWEwa2ciLCJtYWMiOiI2YzBmYmRkOGEyZTZkNmIzOGEyZjVhMDRjMDcyN2IwMmYwZDI3ZmJhMjg2ODBkZTQwOWY4ZTY4ZjVkYzRiY2FhIn0%3D; b_ses=eyJpdiI6InJtYmE5cllBUytFQzR1a1V3a2JSdWc9PSIsInZhbHVlIjoiQ3U3TDhoWDFrUTVyelE0ZldzMnk0V1I1T0J3V0F3NFQ2bWkvc3FlMERIWjdUZXIwbk9pU0dpTktaMCtuZGlzS0RtSjZsZ2JSWERnaEpGKzRRZHR6MzJ6QTZ6TXRaWUx2THRJVUdqYng2M3pnVDBpUlNIU0dVOFBaVWpWdHZXdEwiLCJtYWMiOiIwMTY5MGY4NzI0OGY1ZGZhMTBmNWMyMjY1MWVlYWQ3MjBjNTU5MDRmZDhhOWI3YzU5N2FiODZjMDAwNTY5OGYzIn0%3D; _ga_DY0XVSV4WZ=GS1.1.1697620895.34.1.1697622218.33.0.0; _EXPL_TIME_=tajimaya-oroshi/1697622227333&'
        }
        response = requests.get(
            headers=headers,
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
                data['price'] = int(float(item.find('span', attrs={'class': '__unit-price'}).text.split('円')[0]))
                data['count_set'] = int(item.find('span', attrs={'class': '__quantity'}).text)
                data['title'] = f'{data["title"]} {data["count_set"]}個セット'
                data['photos'] = []
                pool.submit(self.scrape_item, source_url=item_url, data=data, result=result)
            except Exception:
                # raise ValueError(convert_text(item.find('h2', attrs={'class': '__title'}).text))
                pass

        pool.shutdown(wait=True)
        return result
    