import json
import logging

from django.conf import settings
from requests import Session


class ZPSession(object):
    def __init__(self, login_data=None):
        if login_data is None:
            try:
                self.login_data = {"username": settings.ZP_USERNAME, "password": settings.ZP_PASSWORD, "login": "Login"}
            except Exception as e:
                logging.error(f"ZP login_data Needed.\n {e}")
                raise e
        else:
            self.login_data = login_data
        # self.zp_url = settings.ZP_URL
        self.session = None
        # User Agent required or will be blocked at some apis
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"

    def check_status(self):
        if self.session is None:
            return False
        else:
            r = self.session.get("https://zwiftpower.com")
            status_code = r.status_code == 200
            login_required = "Login Required" in r.text
            if status_code and not login_required:
                return True
            else:
                return False

    def login(self):
        self.session = Session()
        self.session.headers.update({"User-Agent": self.user_agent})
        r = self.session.get(self.zp_url)
        logging.info(r.cookies.get("phpbb3_lswlk_sid"))
        self.login_data["sid"] = r.cookies.get("phpbb3_lswlk_sid")
        # print(self.login_data)
        try:
            self.session.post(self.zp_url, data=self.login_data)
            verify_status = self.session.get(f"{self.zp_url}/events.php").text
            logging.info(f"Profile in VS: {'Profile' in verify_status}")
            logging.info(f"Login Required in VS: {'Login Required' in verify_status}")
            # assert "Profile" in verify_status
            # assert "Login Required" not in verify_status
            logging.info("ZP Login successful")
        except Exception as e:
            logging.error(f"ZP Failed to login: {e}")
            return self.session
            # self.session = None

    def get_session(self):
        if self.check_status():
            return self.session
        else:
            try:
                self.login()
                return self.session
            except Exception as e:
                logging.error(f"Failed to login to ZP: {e}")
                return None

    def get_api(self, id: int, api: str) -> json:
        """
        the Api(s) to fetch are based on matching the api to the key in the dict
        """
        if self.get_session():
            self.apis = dict(
                team_riders=f"{self.zp_url}/api3.php?do=team_riders&id={id}",
                team_pending=f"{self.zp_url}/api3.php?do=team_pending&id={id}",
                team_results=f"{self.zp_url}/api3.php?do=team_results&id={id}",
                profile_profile=f"{self.zp_url}/cache3/profile/{id}_all.json",
                profile_victims=f"{self.zp_url}/cache3/profile/{id}_rider_compare_victims.json",
                profile_signups=f"{self.zp_url}/cache3/profile/{id}_signups.json",
                all_results=f"{self.zp_url}/cache3/lists/0_zwift_event_list_results_3.json",
                event_results_view=f"{self.zp_url}/cache3/results/{id}_view.json",
                event_results_zwift=f"{self.zp_url}/cache3/results/{id}_zwift.json",
            )
            data_set = dict()
            for k, v in self.apis.items():
                if api in k:
                    logging.info(f"Get {k} data from: {v}")
                    try:
                        raw = self.session.get(v)
                        data = json.loads(raw.text)
                        assert "data" in data.keys()
                        data_set[k] = data
                    except Exception as e:
                        logging.error(f"Failed to get data from ZP: {e}\n {raw.text}")
                        data_set[k] = None
            return data_set


def flatten_row(row: dict) -> dict:
    update_row = {}
    for k, v in row.items():
        try:
            if isinstance(v, list) and len(v) == 2:
                update_row[f"{k}"] = v[0]
                update_row[f"{k}_1"] = v[1]
        except:
            print(k, v)
    return update_row


for row in COALITION_who_raced:
    row.update(flatten_row(row))
